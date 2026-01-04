"""API client modules for CobranSaaS."""

from cobransaas_mcp.api.client import CobranSaaSClient, get_client, close_client
from cobransaas_mcp.api.global_api import get_global_info
from cobransaas_mcp.api.lotes_api import list_lotes, get_lote, list_lote_registros, list_registros_delta
from cobransaas_mcp.api.clientes_api import list_clientes, get_cliente
from cobransaas_mcp.api.contratos_api import list_contratos, get_contrato
from cobransaas_mcp.api.parcelas_api import (
    list_parcelas,
    get_parcela,
    get_parcela_boleto,
    get_parcela_boleto_pdf,
    registrar_parcela_boleto,
)
from cobransaas_mcp.api.negociacoes_api import list_negociacoes
from cobransaas_mcp.api.acordos_api import (
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
)
from cobransaas_mcp.api.propostas_api import efetivar_proposta, PropostaValidationError
from cobransaas_mcp.api.comissoes_api import list_comissoes
from cobransaas_mcp.api.tabulacoes_api import list_tabulacoes, criar_tabulacao
from cobransaas_mcp.api.pix_api import (
    get_pix_qrcode,
    registrar_pix,
    registrar_pix_lista,
    registrar_parcela_acordo_pix,
    registrar_parcelas_acordo_pix,
)
from cobransaas_mcp.api.boletos_api import (
    list_boletos,
    get_boleto,
    get_boleto_pdf,
)

__all__ = [
    # Client
    "CobranSaaSClient",
    "get_client",
    "close_client",
    # Global
    "get_global_info",
    # Lotes
    "list_lotes",
    "get_lote",
    "list_lote_registros",
    "list_registros_delta",
    # Clientes
    "list_clientes",
    "get_cliente",
    # Contratos
    "list_contratos",
    "get_contrato",
    # Parcelas
    "list_parcelas",
    "get_parcela",
    "get_parcela_boleto",
    "get_parcela_boleto_pdf",
    "registrar_parcela_boleto",
    # Negociacoes
    "list_negociacoes",
    # Acordos
    "list_acordos",
    "get_acordo",
    "simular_acordo",
    "efetivar_acordo",
    "ativar_acordo",
    "cancelar_acordo",
    "integrar_acordo",
    "concluir_acordo",
    "get_acordo_boleto",
    "get_acordo_boleto_pdf",
    "get_acordo_boleto_dados",
    "registrar_acordo_boleto",
    "registrar_acordo_boletos",
    "liquidar_parcela_acordo",
    "estornar_parcela_acordo",
    # Propostas
    "efetivar_proposta",
    "PropostaValidationError",
    # Comissoes
    "list_comissoes",
    # Tabulacoes
    "list_tabulacoes",
    "criar_tabulacao",
    # PIX
    "get_pix_qrcode",
    "registrar_pix",
    "registrar_pix_lista",
    "registrar_parcela_acordo_pix",
    "registrar_parcelas_acordo_pix",
    # Boletos
    "list_boletos",
    "get_boleto",
    "get_boleto_pdf",
]
