"""Acordos API - Agreements, renegotiations, and payments."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_acordos(
    cliente: str | None = None,
    numero_acordo: str | None = None,
    situacao: str | None = None,
    tipo: str | None = None,
    data_inclusao_inicio: str | None = None,
    data_inclusao_fim: str | None = None,
    data_hora_modificacao_inicio: str | None = None,
    data_hora_modificacao_fim: str | None = None,
    selector: str | None = None,
) -> list[dict[str, Any]]:
    """List agreements.

    Args:
        cliente: Filter by client ID.
        numero_acordo: Filter by agreement number.
        situacao: Filter by status (BLOQUEADO, CANCELADO, ABERTO, PARCIAL,
                  PROPOSTA, REMOVIDO, LIQUIDADO, NAO_CUMPRIDO, PENDENTE,
                  INTEGRADO, CONCLUIDO, RENEGOCIADO).
        tipo: Filter by type (ACORDO, FATURAMENTO, PAGAMENTO_AVULSO, PROMESSA,
              RENEGOCIACAO).
        data_inclusao_inicio: Filter by start inclusion date.
        data_inclusao_fim: Filter by end inclusion date.
        data_hora_modificacao_inicio: Filter by start modification datetime.
        data_hora_modificacao_fim: Filter by end modification datetime.
        selector: Additional data to include (parcelas, pagamentos, origens,
                  pendencias, informacoesAdicionais).

    Returns:
        List of agreement dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if cliente:
        params["cliente"] = cliente
    if numero_acordo:
        params["numeroAcordo"] = numero_acordo
    if situacao:
        params["situacao"] = situacao
    if tipo:
        params["tipo"] = tipo
    if data_inclusao_inicio:
        params["dataInclusaoInicio"] = data_inclusao_inicio
    if data_inclusao_fim:
        params["dataInclusaoFim"] = data_inclusao_fim
    if data_hora_modificacao_inicio:
        params["dataHoraModificacaoInicio"] = data_hora_modificacao_inicio
    if data_hora_modificacao_fim:
        params["dataHoraModificacaoFim"] = data_hora_modificacao_fim
    if selector:
        params["selector"] = selector
        params["mode"] = "CONTINUABLE"

    return await client.get_paginated("/acordos", params=params)


async def get_acordo(
    acordo_id: str,
    selector: str | None = None,
) -> dict[str, Any]:
    """Get a specific agreement by ID.

    Args:
        acordo_id: The agreement ID.
        selector: Additional data to include.

    Returns:
        Agreement details dictionary.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if selector:
        params["selector"] = selector

    return await client.get(f"/acordos/{acordo_id}", params=params)


async def simular_acordo(
    cliente: str,
    negociacao: str,
    meio_pagamento: str | None = None,
    parcelas: list[dict[str, Any]] | None = None,
    parcelamentos: list[dict[str, Any]] | None = None,
    calcular_desconto_parcelamento: bool = False,
) -> dict[str, Any]:
    """Simulate an agreement or renegotiation.

    This is a multi-step process:
    - Step 1: Send cliente, negociacao, meioPagamento to get available options
    - Step 2: Send parcelas list to get calculated values
    - Step 3 (optional): Send parcelamentos with custom values

    Args:
        cliente: Client ID.
        negociacao: Negotiation modality ID.
        meio_pagamento: Payment method ID.
        parcelas: List of installments with discount options.
        parcelamentos: List of payment plan options.
        calcular_desconto_parcelamento: Whether to calculate discounts per plan.

    Returns:
        Simulation result dictionary with parcelas, parcelamentos, and limits.
    """
    client = get_client()
    data: dict[str, Any] = {
        "cliente": cliente,
        "negociacao": negociacao,
    }

    if meio_pagamento:
        data["meioPagamento"] = meio_pagamento
    if parcelas:
        data["parcelas"] = parcelas
    if parcelamentos:
        data["parcelamentos"] = parcelamentos
    if calcular_desconto_parcelamento:
        data["calcularDescontoParcelamento"] = calcular_desconto_parcelamento

    return await client.post("/acordos/simular", json_data=data)


async def efetivar_acordo(
    cliente: str,
    negociacao: str,
    meio_pagamento: str,
    parcelas: list[dict[str, Any]],
    parcelamento: dict[str, Any],
    observacao: str | None = None,
    pagamentos: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Execute/confirm an agreement.

    Args:
        cliente: Client ID.
        negociacao: Negotiation modality ID.
        meio_pagamento: Payment method ID.
        parcelas: List of installments with discount values (must include valorDesconto).
        parcelamento: Payment plan object with dates and values (singular, not array).
        observacao: Optional notes about the agreement.
        pagamentos: Optional list of payments already received.

    Returns:
        Created agreement details dictionary.
    """
    client = get_client()

    # Remove 'parcelas' from parcelamento if present - the API calculates
    # installment details automatically and rejects the request if included
    parcelamento_clean = {k: v for k, v in parcelamento.items() if k != "parcelas"}

    data: dict[str, Any] = {
        "cliente": cliente,
        "negociacao": negociacao,
        "meioPagamento": meio_pagamento,
        "parcelas": parcelas,
        "parcelamento": parcelamento_clean,
    }

    if observacao:
        data["observacao"] = observacao
    if pagamentos:
        data["pagamentos"] = pagamentos

    return await client.post("/acordos/efetivar", json_data=data)


async def ativar_acordo(acordo_id: str) -> dict[str, Any]:
    """Activate a pending agreement.

    Args:
        acordo_id: The agreement ID.

    Returns:
        Activation result dictionary.
    """
    client = get_client()
    return await client.post(f"/acordos/{acordo_id}/ativar")


async def cancelar_acordo(
    acordo_id: str,
    motivo: str | None = None,
) -> dict[str, Any]:
    """Cancel an agreement.

    Args:
        acordo_id: The agreement ID.
        motivo: Cancellation reason.

    Returns:
        Cancellation result dictionary.
    """
    client = get_client()
    data: dict[str, Any] = {}
    if motivo:
        data["motivo"] = motivo
    return await client.post(f"/acordos/{acordo_id}/cancelar", json_data=data if data else None)


async def integrar_acordo(acordo_id: str) -> dict[str, Any]:
    """Mark an agreement as integrated.

    Args:
        acordo_id: The agreement ID.

    Returns:
        Integration result dictionary.
    """
    client = get_client()
    return await client.post(f"/acordos/{acordo_id}/integrar")


async def concluir_acordo(acordo_id: str) -> dict[str, Any]:
    """Mark an agreement as concluded.

    Args:
        acordo_id: The agreement ID.

    Returns:
        Conclusion result dictionary.
    """
    client = get_client()
    return await client.post(f"/acordos/{acordo_id}/concluir")


async def get_acordo_boleto(
    acordo_id: str,
    parcela: str,
) -> dict[str, Any]:
    """Get boleto details for an agreement installment.

    Args:
        acordo_id: The agreement ID.
        parcela: The installment number.

    Returns:
        Boleto details dictionary.
    """
    client = get_client()
    return await client.get(f"/acordos/{acordo_id}/boletos/{parcela}")


async def get_acordo_boleto_pdf(
    acordo_id: str,
    parcela: str,
) -> bytes:
    """Get boleto PDF for an agreement installment.

    Args:
        acordo_id: The agreement ID.
        parcela: The installment number.

    Returns:
        PDF file bytes.
    """
    client = get_client()
    return await client.get_raw(f"/acordos/{acordo_id}/boletos/{parcela}.pdf")


async def registrar_acordo_boleto(
    acordo_id: str,
    parcela: str,
) -> dict[str, Any]:
    """Register a boleto for an agreement installment.

    Args:
        acordo_id: The agreement ID.
        parcela: The installment number.

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    return await client.post(f"/acordos/{acordo_id}/boletos/{parcela}/registrar")


async def registrar_acordo_boletos(
    acordo_id: str,
    parcelas: list[str] | None = None,
) -> dict[str, Any]:
    """Register boletos for agreement installments in batch.

    Args:
        acordo_id: The agreement ID.
        parcelas: List of installment numbers (optional, registers all if not provided).

    Returns:
        Registration result dictionary.
    """
    client = get_client()
    data: dict[str, Any] = {}
    if parcelas:
        data["parcelas"] = parcelas
    return await client.post(f"/acordos/{acordo_id}/boletos/registrar", json_data=data if data else None)


async def liquidar_parcela_acordo(
    parcela_id: str,
    data_liquidacao: str,
    valor_recebido: str,
    data_credito: str | None = None,
    forma_liquidacao: str | None = None,
) -> dict[str, Any]:
    """Settle an agreement installment.

    Args:
        parcela_id: The agreement installment ID.
        data_liquidacao: Settlement date.
        valor_recebido: Amount received.
        data_credito: Credit date.
        forma_liquidacao: Settlement method (MANUAL, ARQUIVO, WEBSERVICE).

    Returns:
        Settlement result dictionary.
    """
    client = get_client()
    data: dict[str, Any] = {
        "dataLiquidacao": data_liquidacao,
        "valorRecebido": valor_recebido,
    }
    if data_credito:
        data["dataCredito"] = data_credito
    if forma_liquidacao:
        data["formaLiquidacao"] = forma_liquidacao
    return await client.post(f"/acordos/{parcela_id}/liquidar", json_data=data)


async def estornar_parcela_acordo(
    parcela_id: str,
    pagamento_id: str,
) -> dict[str, Any]:
    """Reverse a payment for an agreement installment.

    Args:
        parcela_id: The agreement installment ID.
        pagamento_id: The payment ID to reverse.

    Returns:
        Reversal result dictionary.
    """
    client = get_client()
    data: dict[str, Any] = {"pagamento": pagamento_id}
    return await client.post(f"/acordos/{parcela_id}/estornar", json_data=data)
