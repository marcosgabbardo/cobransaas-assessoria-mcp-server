"""Contratos API - Client contracts (debts)."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_contratos(
    cliente: str | None = None,
    situacao: str | None = None,
    selector: str | None = None,
) -> list[dict[str, Any]]:
    """List contracts distributed to the advisory.

    Args:
        cliente: Filter by client ID.
        situacao: Filter by status.
        selector: Additional data to include (parcelas, garantias, participantes,
                  liquidacoes, informacoesAdicionais, marcadores, parcelamentos,
                  notasFiscais).

    Returns:
        List of contract dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if cliente:
        params["cliente"] = cliente
    if situacao:
        params["situacao"] = situacao
    if selector:
        params["selector"] = selector
        params["mode"] = "CONTINUABLE"

    return await client.get_paginated("/contratos", params=params)


async def get_contrato(
    contrato_id: str,
    selector: str | None = None,
) -> dict[str, Any]:
    """Get a specific contract by ID.

    Args:
        contrato_id: The contract ID.
        selector: Additional data to include.

    Returns:
        Contract details dictionary.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if selector:
        params["selector"] = selector

    return await client.get(f"/contratos/{contrato_id}", params=params)
