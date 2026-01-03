"""Negociações API - Negotiation modalities and payment methods."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_negociacoes(
    cliente: str | None = None,
    situacao: str | None = None,
    tipo_modalidade: str | None = None,
) -> list[dict[str, Any]]:
    """List available negotiation modalities and payment methods.

    Args:
        cliente: Filter by client ID (recommended to get client-specific options).
        situacao: Filter by status (ATIVO recommended).
        tipo_modalidade: Filter by modality type (ACORDO, PAGAMENTO_AVULSO,
                         PROMESSA, RENEGOCIACAO).

    Returns:
        List of negotiation modality dictionaries with payment methods.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if cliente:
        params["cliente"] = cliente
    if situacao:
        params["situacao"] = situacao
    if tipo_modalidade:
        params["tipoModalidade"] = tipo_modalidade

    return await client.get_paginated("/negociacoes", params=params)
