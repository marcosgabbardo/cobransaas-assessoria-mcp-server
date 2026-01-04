"""CobranSaaS MCP Server - Main server module."""

import asyncio
import base64
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent

from cobransaas_mcp.api import (
    close_client,
    # Global
    get_global_info,
    # Lotes
    list_lotes,
    get_lote,
    list_lote_registros,
    list_registros_delta,
    # Clientes
    list_clientes,
    get_cliente,
    # Contratos
    list_contratos,
    get_contrato,
    # Parcelas
    list_parcelas,
    get_parcela,
    get_parcela_boleto,
    get_parcela_boleto_pdf,
    registrar_parcela_boleto,
    # Negociacoes
    list_negociacoes,
    # Acordos
    list_acordos,
    get_acordo,
    simular_acordo,
    efetivar_acordo,
    ativar_acordo,
    cancelar_acordo,
    integrar_acordo,
    concluir_acordo,
    get_acordo_boleto,
    get_acordo_boleto_pdf,
    get_acordo_boleto_dados,
    registrar_acordo_boleto,
    registrar_acordo_boletos,
    liquidar_parcela_acordo,
    estornar_parcela_acordo,
    # Propostas
    efetivar_proposta,
    # Comissoes
    list_comissoes,
    # Tabulacoes
    list_tabulacoes,
    criar_tabulacao,
    # PIX
    get_pix_qrcode,
    registrar_pix,
    registrar_pix_lista,
    registrar_parcela_acordo_pix,
    registrar_parcelas_acordo_pix,
    # Boletos
    list_boletos,
    get_boleto,
    get_boleto_pdf,
)

# Create server instance
server = Server("cobransaas-mcp")


def _format_response(data: Any) -> str:
    """Format API response as JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


# ============================================================================
# Tool Definitions
# ============================================================================

TOOLS = [
    # ==========================================================================
    # Global API
    # ==========================================================================
    Tool(
        name="get_processing_date",
        description="Obtém a data de processamento atual do CobranSaaS e informações globais.",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    # ==========================================================================
    # Lotes API
    # ==========================================================================
    Tool(
        name="list_batches",
        description="Lista os lotes de dívidas distribuídos para a assessoria.",
        inputSchema={
            "type": "object",
            "properties": {
                "situacao": {
                    "type": "string",
                    "enum": ["ATIVO", "INATIVO"],
                    "description": "Filtrar por situação do lote",
                }
            },
            "required": [],
        },
    ),
    Tool(
        name="get_batch",
        description="Obtém os detalhes de um lote específico.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do lote"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="list_batch_records",
        description="Lista os registros (dívidas) de um lote específico com paginação. Retorna os dados, indicador de próxima página e token de continuação.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do lote"},
                "selector": {
                    "type": "string",
                    "description": "Dados adicionais a incluir (telefones, emails, enderecos, referencias, participantes, informacoesAdicionais, marcadores, parcelamentos)",
                },
                "size": {
                    "type": "integer",
                    "description": "Quantidade de registros por página (padrão: 10)",
                },
                "continuable": {
                    "type": "string",
                    "description": "Token de continuação para buscar a próxima página (obtido da resposta anterior)",
                },
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="list_batch_records_delta",
        description="Lista registros incluídos ou excluídos do lote ativo (delta).",
        inputSchema={
            "type": "object",
            "properties": {
                "data_inclusao": {
                    "type": "string",
                    "description": "Filtrar por data de inclusão (retorna novos registros)",
                },
                "data_exclusao": {
                    "type": "string",
                    "description": "Filtrar por data de exclusão (retorna registros removidos)",
                },
                "selector": {"type": "string", "description": "Dados adicionais a incluir"},
            },
            "required": [],
        },
    ),
    # ==========================================================================
    # Clientes API
    # ==========================================================================
    Tool(
        name="list_clients",
        description="Lista os clientes distribuídos para a assessoria. Por padrão retorna até 50 registros.",
        inputSchema={
            "type": "object",
            "properties": {
                "nome": {"type": "string", "description": "Filtrar por nome (começa com)"},
                "cic": {"type": "string", "description": "Filtrar por CPF/CNPJ"},
                "tipo_pessoa": {
                    "type": "string",
                    "enum": ["FISICA", "JURIDICA"],
                    "description": "Filtrar por tipo de pessoa",
                },
                "codigo": {"type": "string", "description": "Filtrar por código do cliente"},
                "numero_contrato": {"type": "string", "description": "Filtrar por número de contrato"},
                "selector": {
                    "type": "string",
                    "description": "Dados adicionais a incluir (telefones, emails, enderecos, referencias, informacoesAdicionais, marcadores)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Número máximo de resultados (padrão: 50, máx: 100)",
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="get_client",
        description="Obtém os detalhes de um cliente específico.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do cliente"},
                "selector": {"type": "string", "description": "Dados adicionais a incluir"},
            },
            "required": ["id"],
        },
    ),
    # ==========================================================================
    # Contratos API
    # ==========================================================================
    Tool(
        name="list_contracts",
        description="Lista os contratos (dívidas) distribuídos para a assessoria.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Filtrar por ID do cliente"},
                "situacao": {"type": "string", "description": "Filtrar por situação"},
                "selector": {
                    "type": "string",
                    "description": "Dados adicionais a incluir (parcelas, garantias, participantes, liquidacoes, informacoesAdicionais, marcadores, parcelamentos, notasFiscais)",
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="get_contract",
        description="Obtém os detalhes de um contrato específico.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do contrato"},
                "selector": {"type": "string", "description": "Dados adicionais a incluir"},
            },
            "required": ["id"],
        },
    ),
    # ==========================================================================
    # Parcelas API
    # ==========================================================================
    Tool(
        name="list_installments",
        description="Lista as parcelas de dívidas distribuídas para a assessoria.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Filtrar por ID do cliente"},
                "contrato": {"type": "string", "description": "Filtrar por ID do contrato"},
            },
            "required": [],
        },
    ),
    Tool(
        name="get_installment",
        description="Obtém os detalhes de uma parcela específica.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da parcela"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="get_installment_boleto",
        description="Obtém os detalhes do boleto de uma parcela.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da parcela"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="get_installment_boleto_pdf",
        description="Obtém o PDF do boleto de uma parcela.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da parcela"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="register_installment_boleto",
        description="Registra o boleto de uma parcela.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da parcela"},
            },
            "required": ["id"],
        },
    ),
    # ==========================================================================
    # Negociações API
    # ==========================================================================
    Tool(
        name="list_negotiation_types",
        description="Lista as modalidades de negociação e meios de pagamento disponíveis.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {
                    "type": "string",
                    "description": "ID do cliente (recomendado para obter opções específicas)",
                },
                "situacao": {
                    "type": "string",
                    "enum": ["ATIVO", "INATIVO"],
                    "description": "Filtrar por situação (ATIVO recomendado)",
                },
                "tipo_modalidade": {
                    "type": "string",
                    "enum": ["ACORDO", "PAGAMENTO_AVULSO", "PROMESSA", "RENEGOCIACAO"],
                    "description": "Filtrar por tipo de modalidade",
                },
            },
            "required": [],
        },
    ),
    # ==========================================================================
    # Acordos API
    # ==========================================================================
    Tool(
        name="list_agreements",
        description="Lista os acordos existentes.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Filtrar por ID do cliente"},
                "numero_acordo": {"type": "string", "description": "Filtrar por número do acordo"},
                "situacao": {
                    "type": "string",
                    "description": "Filtrar por situação (BLOQUEADO, CANCELADO, ABERTO, PARCIAL, PROPOSTA, REMOVIDO, LIQUIDADO, NAO_CUMPRIDO, PENDENTE, INTEGRADO, CONCLUIDO, RENEGOCIADO)",
                },
                "tipo": {
                    "type": "string",
                    "description": "Filtrar por tipo (ACORDO, FATURAMENTO, PAGAMENTO_AVULSO, PROMESSA, RENEGOCIACAO)",
                },
                "data_inicio": {"type": "string", "description": "Data de inclusão inicial"},
                "data_fim": {"type": "string", "description": "Data de inclusão final"},
                "selector": {
                    "type": "string",
                    "description": "Dados adicionais (parcelas, pagamentos, origens, pendencias, informacoesAdicionais)",
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="get_agreement",
        description="Obtém os detalhes de um acordo específico.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do acordo"},
                "selector": {"type": "string", "description": "Dados adicionais a incluir"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="simulate_agreement",
        description="Simula um acordo ou renegociação. Processo multi-etapa: 1) Envie cliente e negociacao para obter opções, 2) Envie parcelas para calcular valores, 3) Opcionalmente envie parcelamentos com valores customizados.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "ID do cliente"},
                "negociacao": {"type": "string", "description": "ID da modalidade de negociação"},
                "meio_pagamento": {"type": "string", "description": "ID do meio de pagamento"},
                "parcelas": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Lista de parcelas com opções de desconto",
                },
                "parcelamentos": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Lista de opções de parcelamento",
                },
                "calcular_desconto_parcelamento": {
                    "type": "boolean",
                    "description": "Se deve calcular descontos por plano",
                },
            },
            "required": ["cliente", "negociacao"],
        },
    ),
    Tool(
        name="execute_agreement",
        description="Efetiva um acordo, renegociação ou promessa de pagamento.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "ID do cliente"},
                "negociacao": {"type": "string", "description": "ID da modalidade de negociação"},
                "meio_pagamento": {"type": "string", "description": "ID do meio de pagamento"},
                "parcelas": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Lista de parcelas com valores de desconto. Cada parcela DEVE incluir: parcela (ID), valorDesconto, descontoMora, descontoJuros, descontoMulta, descontoOutros, descontoPrincipal, descontoPermanencia",
                },
                "parcelamento": {
                    "type": "object",
                    "description": "Objeto (singular) do plano de parcelamento com datas e valores. Deve incluir os campos retornados pela simulação (valorTotal, valorPrincipal, valorJuros, dataVencimento, numeroParcelas, etc.)",
                },
                "observacao": {"type": "string", "description": "Observações sobre o acordo"},
            },
            "required": ["cliente", "negociacao", "meio_pagamento", "parcelas", "parcelamento"],
        },
    ),
    Tool(
        name="activate_agreement",
        description="Ativa um acordo que está com situação PENDENTE.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do acordo"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="cancel_agreement",
        description="Cancela um acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do acordo"},
                "motivo": {"type": "string", "description": "Motivo do cancelamento"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="integrate_agreement",
        description="Marca um acordo como integrado.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do acordo"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="conclude_agreement",
        description="Marca um acordo como concluído.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do acordo"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="get_agreement_boleto",
        description="Obtém os detalhes do boleto de uma parcela de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "acordo_id": {"type": "string", "description": "ID do acordo"},
                "parcela": {"type": "string", "description": "Número da parcela"},
            },
            "required": ["acordo_id", "parcela"],
        },
    ),
    Tool(
        name="get_agreement_boleto_pdf",
        description="Obtém o PDF do boleto de uma parcela de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "acordo_id": {"type": "string", "description": "ID do acordo"},
                "parcela": {"type": "string", "description": "Número da parcela"},
            },
            "required": ["acordo_id", "parcela"],
        },
    ),
    Tool(
        name="get_agreement_boleto_data",
        description="Obtém os dados do boleto de uma parcela de acordo, incluindo linha digitável, código de barras, valor, vencimento e situação.",
        inputSchema={
            "type": "object",
            "properties": {
                "parcela_id": {"type": "string", "description": "ID da parcela do acordo"},
            },
            "required": ["parcela_id"],
        },
    ),
    Tool(
        name="register_agreement_boleto",
        description="Registra o boleto de uma parcela de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "acordo_id": {"type": "string", "description": "ID do acordo"},
                "parcela": {"type": "string", "description": "Número da parcela"},
            },
            "required": ["acordo_id", "parcela"],
        },
    ),
    Tool(
        name="register_agreement_boletos",
        description="Registra os boletos de um acordo em lote.",
        inputSchema={
            "type": "object",
            "properties": {
                "acordo_id": {"type": "string", "description": "ID do acordo"},
                "parcelas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de números de parcelas (opcional, registra todas se não informado)",
                },
            },
            "required": ["acordo_id"],
        },
    ),
    Tool(
        name="settle_agreement_installment",
        description="Liquida (baixa) uma parcela de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "parcela_id": {"type": "string", "description": "ID da parcela do acordo"},
                "data_liquidacao": {"type": "string", "description": "Data da liquidação (YYYY-MM-DD)"},
                "valor_recebido": {"type": "string", "description": "Valor recebido"},
                "data_credito": {"type": "string", "description": "Data do crédito (opcional)"},
                "forma_liquidacao": {
                    "type": "string",
                    "enum": ["MANUAL", "ARQUIVO", "WEBSERVICE"],
                    "description": "Forma de liquidação",
                },
            },
            "required": ["parcela_id", "data_liquidacao", "valor_recebido"],
        },
    ),
    Tool(
        name="reverse_agreement_payment",
        description="Estorna um pagamento de uma parcela de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "parcela_id": {"type": "string", "description": "ID da parcela do acordo"},
                "pagamento_id": {"type": "string", "description": "ID do pagamento a estornar"},
            },
            "required": ["parcela_id", "pagamento_id"],
        },
    ),
    Tool(
        name="execute_proposal",
        description="Efetiva uma proposta de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "ID do cliente"},
                "negociacao": {"type": "string", "description": "ID da modalidade de negociação"},
                "meio_pagamento": {"type": "string", "description": "ID do meio de pagamento"},
                "data_vigencia": {"type": "string", "description": "Data limite de vigência da proposta"},
                "parcelas": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Lista de parcelas com valores de desconto",
                },
                "parcelamentos": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Lista de opções de parcelamento",
                },
            },
            "required": ["cliente", "negociacao", "meio_pagamento", "data_vigencia", "parcelas", "parcelamentos"],
        },
    ),
    # ==========================================================================
    # Comissões API
    # ==========================================================================
    Tool(
        name="list_commissions",
        description="Lista as comissões da assessoria.",
        inputSchema={
            "type": "object",
            "properties": {
                "produto": {"type": "string", "description": "Filtrar por ID do produto"},
                "situacao": {
                    "type": "string",
                    "enum": ["ATIVO", "PRIVADO", "CONCLUIDO", "ESTORNADO", "REMOVIDO"],
                    "description": "Filtrar por situação",
                },
                "cliente": {"type": "string", "description": "Filtrar por ID do cliente"},
                "contrato": {"type": "string", "description": "Filtrar por ID do contrato"},
                "numero_acordo": {"type": "string", "description": "Filtrar por número do acordo"},
                "data_inicio": {"type": "string", "description": "Data inicial do período"},
                "data_fim": {"type": "string", "description": "Data final do período"},
            },
            "required": [],
        },
    ),
    # ==========================================================================
    # Tabulações API
    # ==========================================================================
    Tool(
        name="list_tabulations",
        description="Lista os tipos de tabulação (histórico de contatos) disponíveis.",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="create_tabulation",
        description="Registra uma nova tabulação (registro de contato com cliente).",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "ID do cliente"},
                "contrato": {"type": "string", "description": "ID do contrato (opcional)"},
                "parcela": {"type": "string", "description": "ID da parcela (opcional)"},
                "tabulacao": {"type": "string", "description": "ID do tipo de tabulação"},
                "telefone": {"type": "string", "description": "Telefone utilizado no contato"},
                "observacao": {"type": "string", "description": "Observações do contato"},
            },
            "required": ["cliente"],
        },
    ),
    # ==========================================================================
    # PIX API
    # ==========================================================================
    Tool(
        name="get_pix_qrcode",
        description="Obtém a imagem do QR Code PIX.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do PIX"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="register_pix",
        description="Registra um PIX por ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do PIX"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="register_pix_batch",
        description="Registra uma lista de PIX.",
        inputSchema={
            "type": "object",
            "properties": {
                "ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de IDs de PIX",
                },
            },
            "required": ["ids"],
        },
    ),
    Tool(
        name="register_agreement_pix",
        description="Registra PIX para uma parcela de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "id_parcela": {"type": "string", "description": "ID da parcela do acordo"},
            },
            "required": ["id_parcela"],
        },
    ),
    Tool(
        name="register_agreement_pix_batch",
        description="Registra PIX para uma lista de parcelas de acordo.",
        inputSchema={
            "type": "object",
            "properties": {
                "ids_parcelas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de IDs das parcelas do acordo",
                },
            },
            "required": ["ids_parcelas"],
        },
    ),
    # ==========================================================================
    # Boletos API
    # ==========================================================================
    Tool(
        name="list_boletos",
        description="Lista os boletos.",
        inputSchema={
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Filtrar por ID do cliente"},
                "contrato": {"type": "string", "description": "Filtrar por ID do contrato"},
                "parcela": {"type": "string", "description": "Filtrar por ID da parcela"},
                "situacao": {
                    "type": "string",
                    "enum": ["ABERTO", "LIQUIDADO", "CANCELADO"],
                    "description": "Filtrar por situação",
                },
                "data_vencimento_inicio": {"type": "string", "description": "Data de vencimento inicial"},
                "data_vencimento_fim": {"type": "string", "description": "Data de vencimento final"},
                "registrado": {"type": "boolean", "description": "Filtrar por status de registro"},
            },
            "required": [],
        },
    ),
    Tool(
        name="get_boleto",
        description="Obtém os detalhes de um boleto específico.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do boleto"},
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="get_boleto_pdf",
        description="Obtém o PDF de um boleto.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do boleto"},
            },
            "required": ["id"],
        },
    ),
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent]:
    """Handle tool calls."""
    try:
        result: Any = None

        # ======================================================================
        # Global API
        # ======================================================================
        if name == "get_processing_date":
            result = await get_global_info()

        # ======================================================================
        # Lotes API
        # ======================================================================
        elif name == "list_batches":
            result = await list_lotes(situacao=arguments.get("situacao"))
        elif name == "get_batch":
            result = await get_lote(arguments["id"])
        elif name == "list_batch_records":
            result = await list_lote_registros(
                lote_id=arguments["id"],
                selector=arguments.get("selector"),
                size=arguments.get("size", 10),
                continuable=arguments.get("continuable"),
            )
        elif name == "list_batch_records_delta":
            result = await list_registros_delta(
                data_inclusao=arguments.get("data_inclusao"),
                data_exclusao=arguments.get("data_exclusao"),
                selector=arguments.get("selector"),
            )

        # ======================================================================
        # Clientes API
        # ======================================================================
        elif name == "list_clients":
            result = await list_clientes(
                nome=arguments.get("nome"),
                cic=arguments.get("cic"),
                tipo_pessoa=arguments.get("tipo_pessoa"),
                codigo=arguments.get("codigo"),
                numero_contrato=arguments.get("numero_contrato"),
                selector=arguments.get("selector"),
                limit=arguments.get("limit"),
            )
        elif name == "get_client":
            result = await get_cliente(
                cliente_id=arguments["id"],
                selector=arguments.get("selector"),
            )

        # ======================================================================
        # Contratos API
        # ======================================================================
        elif name == "list_contracts":
            result = await list_contratos(
                cliente=arguments.get("cliente"),
                situacao=arguments.get("situacao"),
                selector=arguments.get("selector"),
            )
        elif name == "get_contract":
            result = await get_contrato(
                contrato_id=arguments["id"],
                selector=arguments.get("selector"),
            )

        # ======================================================================
        # Parcelas API
        # ======================================================================
        elif name == "list_installments":
            result = await list_parcelas(
                cliente=arguments.get("cliente"),
                contrato=arguments.get("contrato"),
            )
        elif name == "get_installment":
            result = await get_parcela(arguments["id"])
        elif name == "get_installment_boleto":
            result = await get_parcela_boleto(arguments["id"])
        elif name == "get_installment_boleto_pdf":
            pdf_bytes = await get_parcela_boleto_pdf(arguments["id"])
            return [
                TextContent(
                    type="text",
                    text=f"PDF do boleto (base64): {base64.b64encode(pdf_bytes).decode('utf-8')}",
                )
            ]
        elif name == "register_installment_boleto":
            result = await registrar_parcela_boleto(arguments["id"])

        # ======================================================================
        # Negociações API
        # ======================================================================
        elif name == "list_negotiation_types":
            result = await list_negociacoes(
                cliente=arguments.get("cliente"),
                situacao=arguments.get("situacao"),
                tipo_modalidade=arguments.get("tipo_modalidade"),
            )

        # ======================================================================
        # Acordos API
        # ======================================================================
        elif name == "list_agreements":
            result = await list_acordos(
                cliente=arguments.get("cliente"),
                numero_acordo=arguments.get("numero_acordo"),
                situacao=arguments.get("situacao"),
                tipo=arguments.get("tipo"),
                data_inclusao_inicio=arguments.get("data_inicio"),
                data_inclusao_fim=arguments.get("data_fim"),
                selector=arguments.get("selector"),
            )
        elif name == "get_agreement":
            result = await get_acordo(
                acordo_id=arguments["id"],
                selector=arguments.get("selector"),
            )
        elif name == "simulate_agreement":
            result = await simular_acordo(
                cliente=arguments["cliente"],
                negociacao=arguments["negociacao"],
                meio_pagamento=arguments.get("meio_pagamento"),
                parcelas=arguments.get("parcelas"),
                parcelamentos=arguments.get("parcelamentos"),
                calcular_desconto_parcelamento=arguments.get("calcular_desconto_parcelamento", False),
            )
        elif name == "execute_agreement":
            result = await efetivar_acordo(
                cliente=arguments["cliente"],
                negociacao=arguments["negociacao"],
                meio_pagamento=arguments["meio_pagamento"],
                parcelas=arguments["parcelas"],
                parcelamento=arguments["parcelamento"],
                observacao=arguments.get("observacao"),
            )
        elif name == "activate_agreement":
            result = await ativar_acordo(arguments["id"])
        elif name == "cancel_agreement":
            result = await cancelar_acordo(
                acordo_id=arguments["id"],
                motivo=arguments.get("motivo"),
            )
        elif name == "integrate_agreement":
            result = await integrar_acordo(arguments["id"])
        elif name == "conclude_agreement":
            result = await concluir_acordo(arguments["id"])
        elif name == "get_agreement_boleto":
            result = await get_acordo_boleto(
                acordo_id=arguments["acordo_id"],
                parcela=arguments["parcela"],
            )
        elif name == "get_agreement_boleto_pdf":
            pdf_bytes = await get_acordo_boleto_pdf(
                acordo_id=arguments["acordo_id"],
                parcela=arguments["parcela"],
            )
            return [
                TextContent(
                    type="text",
                    text=f"PDF do boleto (base64): {base64.b64encode(pdf_bytes).decode('utf-8')}",
                )
            ]
        elif name == "get_agreement_boleto_data":
            result = await get_acordo_boleto_dados(arguments["parcela_id"])
        elif name == "register_agreement_boleto":
            result = await registrar_acordo_boleto(
                acordo_id=arguments["acordo_id"],
                parcela=arguments["parcela"],
            )
        elif name == "register_agreement_boletos":
            result = await registrar_acordo_boletos(
                acordo_id=arguments["acordo_id"],
                parcelas=arguments.get("parcelas"),
            )
        elif name == "settle_agreement_installment":
            result = await liquidar_parcela_acordo(
                parcela_id=arguments["parcela_id"],
                data_liquidacao=arguments["data_liquidacao"],
                valor_recebido=arguments["valor_recebido"],
                data_credito=arguments.get("data_credito"),
                forma_liquidacao=arguments.get("forma_liquidacao"),
            )
        elif name == "reverse_agreement_payment":
            result = await estornar_parcela_acordo(
                parcela_id=arguments["parcela_id"],
                pagamento_id=arguments["pagamento_id"],
            )
        elif name == "execute_proposal":
            result = await efetivar_proposta(
                cliente=arguments["cliente"],
                negociacao=arguments["negociacao"],
                meio_pagamento=arguments["meio_pagamento"],
                data_vigencia=arguments["data_vigencia"],
                parcelas=arguments["parcelas"],
                parcelamentos=arguments["parcelamentos"],
            )

        # ======================================================================
        # Comissões API
        # ======================================================================
        elif name == "list_commissions":
            result = await list_comissoes(
                produto=arguments.get("produto"),
                situacao=arguments.get("situacao"),
                cliente=arguments.get("cliente"),
                contrato=arguments.get("contrato"),
                numero_acordo=arguments.get("numero_acordo"),
                data_inicio=arguments.get("data_inicio"),
                data_fim=arguments.get("data_fim"),
            )

        # ======================================================================
        # Tabulações API
        # ======================================================================
        elif name == "list_tabulations":
            result = await list_tabulacoes()
        elif name == "create_tabulation":
            result = await criar_tabulacao(
                cliente=arguments["cliente"],
                contrato=arguments.get("contrato"),
                parcela=arguments.get("parcela"),
                tabulacao=arguments.get("tabulacao"),
                telefone=arguments.get("telefone"),
                observacao=arguments.get("observacao"),
            )

        # ======================================================================
        # PIX API
        # ======================================================================
        elif name == "get_pix_qrcode":
            image_bytes = await get_pix_qrcode(arguments["id"])
            return [
                ImageContent(
                    type="image",
                    data=base64.b64encode(image_bytes).decode("utf-8"),
                    mimeType="image/png",
                )
            ]
        elif name == "register_pix":
            result = await registrar_pix(arguments["id"])
        elif name == "register_pix_batch":
            result = await registrar_pix_lista(arguments["ids"])
        elif name == "register_agreement_pix":
            result = await registrar_parcela_acordo_pix(arguments["id_parcela"])
        elif name == "register_agreement_pix_batch":
            result = await registrar_parcelas_acordo_pix(arguments["ids_parcelas"])

        # ======================================================================
        # Boletos API
        # ======================================================================
        elif name == "list_boletos":
            result = await list_boletos(
                cliente=arguments.get("cliente"),
                contrato=arguments.get("contrato"),
                parcela=arguments.get("parcela"),
                situacao=arguments.get("situacao"),
                data_vencimento_inicio=arguments.get("data_vencimento_inicio"),
                data_vencimento_fim=arguments.get("data_vencimento_fim"),
                registrado=arguments.get("registrado"),
            )
        elif name == "get_boleto":
            result = await get_boleto(arguments["id"])
        elif name == "get_boleto_pdf":
            pdf_bytes = await get_boleto_pdf(arguments["id"])
            return [
                TextContent(
                    type="text",
                    text=f"PDF do boleto (base64): {base64.b64encode(pdf_bytes).decode('utf-8')}",
                )
            ]

        else:
            return [TextContent(type="text", text=f"Tool '{name}' not found.")]

        return [TextContent(type="text", text=_format_response(result))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run_server() -> None:
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """Main entry point."""
    try:
        asyncio.run(run_server())
    finally:
        asyncio.run(close_client())


if __name__ == "__main__":
    main()
