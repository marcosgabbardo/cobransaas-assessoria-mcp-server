"""PIX API - PIX payment management."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def get_pix_qrcode(pix_id: str) -> bytes:
    """Get PIX QR Code image.

    Args:
        pix_id: The PIX ID.

    Returns:
        PNG image bytes.
    """
    client = get_client()
    return await client.get_raw(f"/pix/{pix_id}.png")


async def registrar_pix(pix_id: str) -> dict[str, Any]:
    """Register a PIX by ID.

    Args:
        pix_id: The PIX ID.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post(f"/pix/{pix_id}/registrar")


async def registrar_pix_lista(pix_ids: list[str]) -> dict[str, Any]:
    """Register a list of PIX.

    Args:
        pix_ids: List of PIX IDs.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post("/pix/registrar", json_data={"pixs": pix_ids})


async def registrar_parcela_acordo_pix(parcela_id: str) -> dict[str, Any]:
    """Register a PIX for an agreement installment.

    Args:
        parcela_id: The agreement installment ID.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post(f"/pix/acordos/{parcela_id}/registrar")


async def registrar_parcelas_acordo_pix(parcela_ids: list[str]) -> dict[str, Any]:
    """Register PIX for a list of agreement installments.

    Args:
        parcela_ids: List of agreement installment IDs.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post("/pix/acordos/registrar", json_data={"parcelas": parcela_ids})
