"""Propostas API - Proposal management."""

from typing import Any

from cobransaas_mcp.api.client import get_client


def _ensure_parcela_defaults(parcela: dict[str, Any]) -> dict[str, Any]:
    """Ensure a parcela has all required discount fields with defaults.

    This handles both missing fields AND fields with None values.
    """
    result = dict(parcela)
    defaults = {
        "valorDesconto": 0,
        "descontoMora": 0,
        "descontoJuros": 0,
        "descontoMulta": 0,
        "descontoOutros": 0,
        "descontoPrincipal": 0,
        "descontoPermanencia": 0,
    }
    for key, default_value in defaults.items():
        if key not in result or result[key] is None:
            result[key] = default_value
    return result


def _ensure_parcelamento_defaults(parcelamento: dict[str, Any]) -> dict[str, Any]:
    """Ensure a parcelamento has all required fields with defaults.

    This handles both missing fields AND fields with None values.
    """
    result = dict(parcelamento)
    defaults = {
        "descontoDivida": 0,
        "descontoTarifa": 0,
        "descontoTarifaParcela": 0,
    }
    for key, default_value in defaults.items():
        if key not in result or result[key] is None:
            result[key] = default_value
    return result


def _process_parcelamentos(
    parcelamentos: list[dict[str, Any]],
    parcelas_base: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Process parcelamentos to ensure each has required fields.

    For proposals, each parcelamento contains its own 'parcelas' array.
    This function ensures all parcelas have the required discount fields.

    Args:
        parcelamentos: List of parcelamento options.
        parcelas_base: Optional base parcelas list to use if parcelamento
                       doesn't have its own parcelas.
    """
    processed = []
    for parcelamento in parcelamentos:
        # Add parcelamento-level defaults
        parcelamento_copy = _ensure_parcelamento_defaults(dict(parcelamento))

        # If parcelamento doesn't have parcelas but we have a base list, use it
        if "parcelas" not in parcelamento_copy or not parcelamento_copy["parcelas"]:
            if parcelas_base:
                parcelamento_copy["parcelas"] = [
                    _ensure_parcela_defaults(p) for p in parcelas_base
                ]
        else:
            # Process existing parcelas to add defaults
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
    parcelas: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Execute/confirm a proposal.

    For proposals, each parcelamento option should contain its own 'parcelas' array
    with all the installments and their discount values.

    Alternatively, you can provide a top-level 'parcelas' list that will be used
    as the base for all parcelamentos that don't have their own parcelas.

    Args:
        cliente: Client ID.
        negociacao: Negotiation modality ID.
        meio_pagamento: Payment method ID.
        data_vigencia: Proposal validity date (YYYY-MM-DD).
        parcelamentos: List of payment plan options. Each parcelamento should contain:
            - parcelas: List of installments, each with 'parcela' (ID) and discount fields
            - Other parcelamento fields from simulation (valorTotal, numeroParcelas, etc.)
        parcelas: Optional top-level parcelas list (used if parcelamentos don't have their own).

    Returns:
        Created proposal details dictionary.
    """
    client = get_client()

    # Process parcelamentos to add default values
    processed_parcelamentos = _process_parcelamentos(parcelamentos, parcelas)

    data: dict[str, Any] = {
        "cliente": cliente,
        "negociacao": negociacao,
        "meioPagamento": meio_pagamento,
        "dataVigencia": data_vigencia,
        "parcelamentos": processed_parcelamentos,
    }

    return await client.post("/propostas/efetivar", json_data=data)
