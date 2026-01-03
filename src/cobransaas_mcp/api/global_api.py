"""Global API - Data de processamento atual."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def get_global_info() -> dict[str, Any]:
    """Get global information including current processing date.

    Returns:
        Dictionary with global information including dataProcessamentoAtual.
    """
    client = get_client()
    return await client.get("/global")
