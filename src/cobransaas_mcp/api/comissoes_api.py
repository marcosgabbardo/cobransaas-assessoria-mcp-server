"""Comissões API - Commission management."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_comissoes(
    produto: str | None = None,
    situacao: str | None = None,
    cliente: str | None = None,
    contrato: str | None = None,
    numero_acordo: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
) -> list[dict[str, Any]]:
    """List commissions.

    Args:
        produto: Filter by product ID.
        situacao: Filter by status (ATIVO, PRIVADO, CONCLUIDO, ESTORNADO, REMOVIDO).
        cliente: Filter by client ID.
        contrato: Filter by contract ID.
        numero_acordo: Filter by agreement number.
        data_inicio: Filter by start date.
        data_fim: Filter by end date.

    Returns:
        List of commission dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if produto:
        params["produto"] = produto
    if situacao:
        params["situacao"] = situacao
    if cliente:
        params["cliente"] = cliente
    if contrato:
        params["contrato"] = contrato
    if numero_acordo:
        params["numeroAcordo"] = numero_acordo
    if data_inicio:
        params["dataInicio"] = data_inicio
    if data_fim:
        params["dataFim"] = data_fim

    return await client.get_paginated("/comissoes", params=params)
