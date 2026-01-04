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


def _is_valid_parcela_divida(parcela: dict[str, Any]) -> bool:
    """Check if a parcela dict represents a debt installment (has 'parcela' ID field).

    The 'parcelas' inside parcelamentos should be debt installments with:
    - 'parcela': ID of the original debt installment
    - discount fields (valorDesconto, descontoMora, etc.)

    NOT payment plan installments which have:
    - 'numeroParcela': sequential number
    - 'valorTotal', 'valorJuros', etc.
    """
    return "parcela" in parcela and parcela["parcela"] is not None


class PropostaValidationError(Exception):
    """Raised when proposal data is invalid."""

    pass


def _process_parcelamentos(
    parcelamentos: list[dict[str, Any]],
    parcelas_base: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Process parcelamentos to ensure each has required fields.

    For proposals, each parcelamento must contain 'parcelas' which are the
    ORIGINAL DEBT INSTALLMENTS (with 'parcela' ID and discount fields),
    NOT the payment plan installments.

    If parcelamentos contain payment plan data instead of debt installments,
    this function will use the top-level parcelas_base instead.

    Args:
        parcelamentos: List of parcelamento options.
        parcelas_base: Top-level parcelas list with debt installments.

    Raises:
        PropostaValidationError: If parcelas are invalid and no parcelas_base provided.
    """
    processed = []
    for i, parcelamento in enumerate(parcelamentos):
        # Add parcelamento-level defaults
        parcelamento_copy = _ensure_parcelamento_defaults(dict(parcelamento))

        existing_parcelas = parcelamento_copy.get("parcelas", [])

        # Check if existing parcelas are valid debt installments (have 'parcela' ID)
        # If they don't have 'parcela' field, they're likely payment plan data, not debt installments
        has_valid_parcelas = existing_parcelas and all(
            _is_valid_parcela_divida(p) for p in existing_parcelas
        )

        if has_valid_parcelas:
            # Use existing parcelas, just add defaults
            parcelamento_copy["parcelas"] = [
                _ensure_parcela_defaults(p) for p in existing_parcelas
            ]
        elif parcelas_base:
            # Use top-level parcelas as they contain the debt installment IDs
            parcelamento_copy["parcelas"] = [
                _ensure_parcela_defaults(p) for p in parcelas_base
            ]
        else:
            # CRITICAL ERROR: parcelas inside parcelamentos have wrong structure
            # and no parcelas_base was provided
            wrong_fields = []
            if existing_parcelas:
                sample = existing_parcelas[0]
                if "numeroParcela" in sample:
                    wrong_fields.append("numeroParcela")
                if "valorJuros" in sample and "parcela" not in sample:
                    wrong_fields.append("valorJuros")
                if "parcela" not in sample:
                    wrong_fields.append("MISSING: parcela (ID)")

            raise PropostaValidationError(
                f"ERRO: parcelamentos[{i}].parcelas contém dados do PLANO DE PAGAMENTO, "
                f"não das PARCELAS DA DÍVIDA. "
                f"Campos errados detectados: {wrong_fields}. "
                f"SOLUÇÃO: Você DEVE passar o parâmetro 'parcelas' (top-level) com as parcelas "
                f"da dívida do resultado da simulação. As parcelas da dívida têm o campo 'parcela' "
                f"(ID da parcela) - são as que vêm no nível superior da resposta do simulate_agreement. "
                f"NÃO use as parcelas de dentro dos parcelamentos - essas são do plano de pagamento."
            )

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
