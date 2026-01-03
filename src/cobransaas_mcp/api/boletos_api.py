"""Boletos API - Bank slip (boleto) management."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_boletos(
    cliente: str | None = None,
    contrato: str | None = None,
    parcela: str | None = None,
    situacao: str | None = None,
    data_vencimento_inicio: str | None = None,
    data_vencimento_fim: str | None = None,
    registrado: bool | None = None,
) -> list[dict[str, Any]]:
    """List boletos (bank slips).

    Args:
        cliente: Filter by client ID.
        contrato: Filter by contract ID.
        parcela: Filter by installment ID.
        situacao: Filter by status (ABERTO, LIQUIDADO, CANCELADO).
        data_vencimento_inicio: Filter by start due date.
        data_vencimento_fim: Filter by end due date.
        registrado: Filter by registration status.

    Returns:
        List of boleto dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if cliente:
        params["cliente"] = cliente
    if contrato:
        params["contrato"] = contrato
    if parcela:
        params["parcela"] = parcela
    if situacao:
        params["situacao"] = situacao
    if data_vencimento_inicio:
        params["dataVencimentoInicio"] = data_vencimento_inicio
    if data_vencimento_fim:
        params["dataVencimentoFim"] = data_vencimento_fim
    if registrado is not None:
        params["registrado"] = str(registrado).lower()

    return await client.get_paginated("/boletos", params=params)


async def get_boleto(boleto_id: str) -> dict[str, Any]:
    """Get a specific boleto by ID.

    Args:
        boleto_id: The boleto ID.

    Returns:
        Boleto details dictionary.
    """
    client = get_client()
    return await client.get(f"/boletos/{boleto_id}")


async def get_boleto_pdf(boleto_id: str) -> bytes:
    """Get boleto PDF.

    Args:
        boleto_id: The boleto ID.

    Returns:
        PDF file bytes.
    """
    client = get_client()
    return await client.get_raw(f"/boletos/{boleto_id}.pdf")


async def registrar_boleto(boleto_id: str) -> dict[str, Any]:
    """Register a boleto.

    Args:
        boleto_id: The boleto ID.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post(f"/boletos/{boleto_id}/registrar")


async def registrar_boletos(boleto_ids: list[str]) -> dict[str, Any]:
    """Register multiple boletos in batch.

    Args:
        boleto_ids: List of boleto IDs.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post("/boletos/registrar", json_data={"boletos": boleto_ids})
