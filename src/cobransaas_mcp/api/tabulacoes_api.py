"""Tabulações API - Contact history (tabulations)."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_tabulacoes() -> list[dict[str, Any]]:
    """List available tabulation types.

    Returns:
        List of tabulation type dictionaries.
    """
    client = get_client()
    return await client.get_paginated("/tabulacoes")


async def criar_tabulacao(
    cliente: str,
    contrato: str | None = None,
    parcela: str | None = None,
    tabulacao: str | None = None,
    telefone: str | None = None,
    observacao: str | None = None,
) -> dict[str, Any]:
    """Create a new tabulation (contact record).

    Args:
        cliente: Client ID.
        contrato: Optional contract ID.
        parcela: Optional installment ID.
        tabulacao: Tabulation type ID.
        telefone: Phone number used in contact.
        observacao: Contact notes/observation.

    Returns:
        Created tabulation dictionary.
    """
    client = get_client()
    data: dict[str, Any] = {"cliente": cliente}

    if contrato:
        data["contrato"] = contrato
    if parcela:
        data["parcela"] = parcela
    if tabulacao:
        data["tabulacao"] = tabulacao
    if telefone:
        data["telefone"] = telefone
    if observacao:
        data["observacao"] = observacao

    return await client.post("/tabulacoes", json_data=data)
