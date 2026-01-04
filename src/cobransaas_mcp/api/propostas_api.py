"""Propostas API - Proposal management."""

from typing import Any

from cobransaas_mcp.api.client import get_client


def _ensure_parcela_defaults(parcela: dict[str, Any]) -> dict[str, Any]:
    """Ensure a parcela has all required discount fields with defaults."""
    defaults = {
        "valorDesconto": 0,
        "descontoMora": 0,
        "descontoJuros": 0,
        "descontoMulta": 0,
        "descontoOutros": 0,
        "descontoPrincipal": 0,
        "descontoPermanencia": 0,
    }
    return {**defaults, **parcela}


def _process_parcelamentos(parcelamentos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Process parcelamentos to ensure each parcela has required fields.

    For proposals, each parcelamento contains its own 'parcelas' array.
    This function ensures all parcelas have the required discount fields.
    """
    processed = []
    for parcelamento in parcelamentos:
        parcelamento_copy = dict(parcelamento)

        # Process parcelas inside this parcelamento
        if "parcelas" in parcelamento_copy and parcelamento_copy["parcelas"]:
            parcelamento_copy["parcelas"] = [
                _ensure_parcela_defaults(p) for p in parcelamento_copy["parcelas"]
            ]

        processed.append(parcelamento_copy)

    return processed


async def efetivar_proposta(
    cliente: str,
    negociacao: str,
    meio_pagamento: str,
    data_vigencia: str,
    parcelamentos: list[dict[str, Any]],
) -> dict[str, Any]:
    """Execute/confirm a proposal.

    For proposals, each parcelamento option must contain its own 'parcelas' array
    with all the installments and their discount values. This is different from
    agreements where parcelas is a top-level field.

    Args:
        cliente: Client ID.
        negociacao: Negotiation modality ID.
        meio_pagamento: Payment method ID.
        data_vigencia: Proposal validity date (YYYY-MM-DD).
        parcelamentos: List of payment plan options. Each parcelamento must contain:
            - parcelas: List of installments, each with 'parcela' (ID) and discount fields
            - Other parcelamento fields from simulation (valorTotal, numeroParcelas, etc.)

    Returns:
        Created proposal details dictionary.
    """
    client = get_client()

    # Process parcelamentos to add default values to parcelas
    processed_parcelamentos = _process_parcelamentos(parcelamentos)

    data: dict[str, Any] = {
        "cliente": cliente,
        "negociacao": negociacao,
        "meioPagamento": meio_pagamento,
        "dataVigencia": data_vigencia,
        "parcelamentos": processed_parcelamentos,
    }

    return await client.post("/propostas/efetivar", json_data=data)
