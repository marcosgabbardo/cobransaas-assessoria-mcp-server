"""Propostas API - Proposal management."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def efetivar_proposta(
    cliente: str,
    negociacao: str,
    meio_pagamento: str,
    data_vigencia: str,
    parcelas: list[dict[str, Any]],
    parcelamentos: list[dict[str, Any]],
) -> dict[str, Any]:
    """Execute/confirm a proposal.

    Args:
        cliente: Client ID.
        negociacao: Negotiation modality ID.
        meio_pagamento: Payment method ID.
        data_vigencia: Proposal validity date.
        parcelas: List of installments with discount values.
        parcelamentos: List of payment plan options.

    Returns:
        Created proposal details dictionary.
    """
    client = get_client()
    data: dict[str, Any] = {
        "cliente": cliente,
        "negociacao": negociacao,
        "meioPagamento": meio_pagamento,
        "dataVigencia": data_vigencia,
        "parcelas": parcelas,
        "parcelamentos": parcelamentos,
    }

    return await client.post("/propostas/efetivar", json_data=data)
