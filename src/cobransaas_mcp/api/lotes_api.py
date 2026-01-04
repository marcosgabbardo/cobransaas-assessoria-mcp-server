"""Lotes API - Lotes e registros de dívidas."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_lotes(
    situacao: str | None = None,
) -> list[dict[str, Any]]:
    """List debt batches.

    Args:
        situacao: Filter by status (ATIVO, INATIVO).

    Returns:
        List of batch dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if situacao:
        params["situacao"] = situacao

    return await client.get_paginated("/lotes", params=params)


async def get_lote(lote_id: str) -> dict[str, Any]:
    """Get a specific batch by ID.

    Args:
        lote_id: The batch ID.

    Returns:
        Batch details dictionary.
    """
    client = get_client()
    return await client.get(f"/lotes/{lote_id}")


async def list_lote_registros(
    lote_id: str,
    selector: str | None = None,
    size: int = 10,
    continuable: str | None = None,
) -> dict[str, Any]:
    """List records (debts) from a specific batch with pagination.

    Args:
        lote_id: The batch ID.
        selector: Additional data to include (telefones, emails, enderecos,
                  referencias, participantes, informacoesAdicionais, marcadores,
                  parcelamentos).
        size: Number of records per page (default 10).
        continuable: Continuation token for next page (from previous response).

    Returns:
        Dictionary with 'data' (list of records), 'has_next' (boolean),
        'continuable' (token for next page), and 'current_size'.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if selector:
        params["selector"] = selector

    return await client.get_page(
        f"/lotes/{lote_id}/registros",
        params=params,
        size=size,
        continuable=continuable,
    )


async def list_registros_delta(
    data_inclusao: str | None = None,
    data_exclusao: str | None = None,
    selector: str | None = None,
) -> list[dict[str, Any]]:
    """List records added or removed from the active batch.

    Args:
        data_inclusao: Filter by inclusion date (returns new records).
        data_exclusao: Filter by exclusion date (returns removed records).
        selector: Additional data to include.

    Returns:
        List of record dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {"mode": "CONTINUABLE"}

    if data_inclusao:
        params["dataInclusao"] = data_inclusao
    if data_exclusao:
        params["dataExclusao"] = data_exclusao
    if selector:
        params["selector"] = selector

    return await client.get_paginated("/lotes/registros", params=params)
