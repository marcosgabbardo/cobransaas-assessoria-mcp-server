"""Configuration settings for CobranSaaS MCP Server."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="COBRANSAAS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Configuration
    host: str = "https://dsv04.dsv.cobransaas.com.br"

    # OAuth2 Client Credentials
    client_id: str  # Código do aplicativo (obrigatório)
    client_secret: str  # Token/Secret do aplicativo (obrigatório)

    # HTTP Client Settings
    timeout: int = 30
    max_retries: int = 3

    @property
    def base_url(self) -> str:
        """Return the base URL for API calls."""
        return f"{self.host}/api/assessorias"

    @property
    def oauth2_url(self) -> str:
        """Return the OAuth2 token URL."""
        return f"{self.host}/oauth/token"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
