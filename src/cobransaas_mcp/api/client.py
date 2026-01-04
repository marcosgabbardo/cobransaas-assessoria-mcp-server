"""HTTP Client for CobranSaaS API with OAuth2 authentication."""

import asyncio
import time
from collections import deque
from typing import Any

import httpx

from cobransaas_mcp.config import get_settings


class RateLimiter:
    """Sliding window rate limiter.

    Limits requests to a maximum number per time window.
    Default: 10 requests per second (as per CobranSaaS API limit).
    """

    def __init__(self, max_requests: int = 10, window_seconds: float = 1.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request can be made within the rate limit."""
        async with self._lock:
            now = time.monotonic()

            # Remove timestamps outside the current window
            while self._timestamps and now - self._timestamps[0] >= self.window_seconds:
                self._timestamps.popleft()

            # If at capacity, wait until the oldest request expires
            if len(self._timestamps) >= self.max_requests:
                oldest = self._timestamps[0]
                wait_time = self.window_seconds - (now - oldest)
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                    # Remove the expired timestamp after waiting
                    if self._timestamps:
                        self._timestamps.popleft()

            # Record this request
            self._timestamps.append(time.monotonic())


class OAuth2Token:
    """OAuth2 token container with expiration tracking."""

    def __init__(self, access_token: str, expires_in: int, token_type: str = "Bearer"):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_at = time.time() + expires_in - 60  # 60s buffer

    @property
    def is_expired(self) -> bool:
        """Check if token is expired or about to expire."""
        return time.time() >= self.expires_at

    @property
    def authorization_header(self) -> str:
        """Return the authorization header value."""
        return f"{self.token_type} {self.access_token}"


class CobranSaaSClient:
    """Async HTTP client for CobranSaaS API."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._token: OAuth2Token | None = None
        self._token_lock = asyncio.Lock()
        self._client: httpx.AsyncClient | None = None
        self._rate_limiter = RateLimiter(max_requests=10, window_seconds=1.0)

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.settings.timeout),
                follow_redirects=True,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _get_token(self) -> OAuth2Token:
        """Get valid OAuth2 token, refreshing if necessary."""
        async with self._token_lock:
            if self._token is None or self._token.is_expired:
                self._token = await self._fetch_token()
            return self._token

    async def _fetch_token(self) -> OAuth2Token:
        """Fetch new OAuth2 token using client credentials with Basic Auth."""
        client = await self._get_client()

        # OAuth2 endpoint uses Basic Auth with client_id:client_secret
        response = await client.post(
            f"{self.settings.oauth2_url}?grant_type=client_credentials",
            auth=(self.settings.client_id, self.settings.client_secret),
        )

        response.raise_for_status()
        data = response.json()

        return OAuth2Token(
            access_token=data["access_token"],
            expires_in=data.get("expires_in", 3600),
            token_type=data.get("token_type", "Bearer"),
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        retry_count: int = 0,
    ) -> httpx.Response:
        """Make authenticated request to API."""
        # Apply rate limiting before each request
        await self._rate_limiter.acquire()

        client = await self._get_client()
        token = await self._get_token()

        url = f"{self.settings.base_url}{endpoint}"
        headers = {"Authorization": token.authorization_header}

        try:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers,
            )

            # Handle token expiration
            if response.status_code == 401 and retry_count < 1:
                self._token = None  # Force token refresh
                return await self._request(
                    method, endpoint, params, json_data, retry_count + 1
                )

            response.raise_for_status()
            return response

        except httpx.HTTPStatusError:
            raise
        except httpx.RequestError as e:
            if retry_count < self.settings.max_retries:
                await asyncio.sleep(2**retry_count)  # Exponential backoff
                return await self._request(
                    method, endpoint, params, json_data, retry_count + 1
                )
            raise e

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make GET request."""
        response = await self._request("GET", endpoint, params=params)
        return response.json()

    async def post(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make POST request."""
        response = await self._request("POST", endpoint, params=params, json_data=json_data)
        return response.json()

    async def get_raw(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """Make GET request and return raw bytes (for images)."""
        response = await self._request("GET", endpoint, params=params)
        return response.content

    async def get_paginated(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        mode: str = "CONTINUABLE",
        max_pages: int = 100,
    ) -> list[Any]:
        """Make paginated GET request and return all results."""
        if params is None:
            params = {}

        params["mode"] = mode
        all_results: list[Any] = []
        page_count = 0

        while page_count < max_pages:
            response = await self._request("GET", endpoint, params=params)
            data = response.json()

            if isinstance(data, list):
                all_results.extend(data)
            else:
                all_results.append(data)

            # Check pagination headers
            has_next = response.headers.get("x-meta-has-next", "false").lower() == "true"
            continuable = response.headers.get("x-meta-continuable")

            if not has_next or not continuable:
                break

            params["continuable"] = continuable
            page_count += 1

        return all_results

    async def get_page(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        size: int = 10,
        continuable: str | None = None,
    ) -> dict[str, Any]:
        """Make single page GET request with CONTINUABLE pagination.

        Args:
            endpoint: API endpoint.
            params: Query parameters.
            size: Page size (default 10).
            continuable: Continuation token from previous page.

        Returns:
            Dictionary with 'data', 'has_next', and 'continuable' keys.
        """
        if params is None:
            params = {}

        params["mode"] = "CONTINUABLE"
        params["size"] = size
        if continuable:
            params["continuable"] = continuable

        response = await self._request("GET", endpoint, params=params)
        data = response.json()

        return {
            "data": data,
            "has_next": response.headers.get("x-meta-has-next", "false").lower() == "true",
            "continuable": response.headers.get("x-meta-continuable"),
            "current_size": response.headers.get("x-meta-current-size"),
        }


# Global client instance
_client: CobranSaaSClient | None = None


def get_client() -> CobranSaaSClient:
    """Get or create global client instance."""
    global _client
    if _client is None:
        _client = CobranSaaSClient()
    return _client


async def close_client() -> None:
    """Close global client instance."""
    global _client
    if _client is not None:
        await _client.close()
        _client = None
