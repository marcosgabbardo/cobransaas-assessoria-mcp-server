"""Clientes API - Clients distributed to the advisory."""

from typing import Any

from cobransaas_mcp.api.client import get_client


async def list_clientes(
    nome: str | None = None,
    cic: str | None = None,
    tipo_pessoa: str | None = None,
    codigo: str | None = None,
    cliente: str | None = None,
    numero_contrato: str | None = None,
    selector: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """List clients distributed to the advisory.

    Args:
        nome: Filter by name (starts with).
        cic: Filter by CPF/CNPJ.
        tipo_pessoa: Filter by person type (FISICA, JURIDICA).
        codigo: Filter by client code.
        cliente: Filter by client ID.
        numero_contrato: Filter by contract number.
        selector: Additional data to include (telefones, emails, enderecos,
                  referencias, informacoesAdicionais, marcadores).
        limit: Maximum number of results to return (default: 50).

    Returns:
        List of client dictionaries.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if nome:
        params["nome"] = nome
    if cic:
        params["cic"] = cic
    if tipo_pessoa:
        params["tipoPessoa"] = tipo_pessoa
    if codigo:
        params["codigo"] = codigo
    if cliente:
        params["cliente"] = cliente
    if numero_contrato:
        params["numeroContrato"] = numero_contrato
    if selector:
        params["selector"] = selector
        params["mode"] = "CONTINUABLE"

    # Use page/size mode for better control
    max_results = limit or 50
    params["page"] = 0
    params["size"] = min(max_results, 100)  # API max is usually 100

    result = await client.get("/clientes", params=params)
    if isinstance(result, list):
        return result[:max_results]
    return result


async def get_cliente(
    cliente_id: str,
    selector: str | None = None,
) -> dict[str, Any]:
    """Get a specific client by ID.

    Args:
        cliente_id: The client ID.
        selector: Additional data to include.

    Returns:
        Client details dictionary.
    """
    client = get_client()
    params: dict[str, Any] = {}

    if selector:
        params["selector"] = selector

    return await client.get(f"/clientes/{cliente_id}", params=params)
