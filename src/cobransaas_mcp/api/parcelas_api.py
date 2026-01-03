"""Parcelas API - Contract installments (debts)."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_parcelas(
    cliente: str | None = None,
    contrato: str | None = None,
) -> list[dict[str, Any]]:
    """List installments (debts) distributed to the advisory.

    Args:
        cliente: Filter by client ID.
        contrato: Filter by contract ID.

    Returns:
        List of installment dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if cliente:
        params["cliente"] = cliente
    if contrato:
        params["contrato"] = contrato

    return await client.get_paginated("/parcelas", params=params)


async def get_parcela(parcela_id: str) -> dict[str, Any]:
    """Get a specific installment by ID.

    Args:
        parcela_id: The installment ID.

    Returns:
        Installment details dictionary.
    """
    client = get_client()
    return await client.get(f"/parcelas/{parcela_id}")


async def get_parcela_boleto(parcela_id: str) -> dict[str, Any]:
    """Get boleto details for an installment.

    Args:
        parcela_id: The installment ID.

    Returns:
        Boleto details dictionary.
    """
    client = get_client()
    return await client.get(f"/parcelas/{parcela_id}/boleto")


async def get_parcela_boleto_pdf(parcela_id: str) -> bytes:
    """Get boleto PDF for an installment.

    Args:
        parcela_id: The installment ID.

    Returns:
        PDF file bytes.
    """
    client = get_client()
    return await client.get_raw(f"/parcelas/{parcela_id}/boleto.pdf")


async def registrar_parcela_boleto(parcela_id: str) -> dict[str, Any]:
    """Register a boleto for an installment.

    Args:
        parcela_id: The installment ID.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post(f"/parcelas/{parcela_id}/boleto/registrar")
