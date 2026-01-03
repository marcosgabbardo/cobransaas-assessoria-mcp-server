# CobranSaaS Assessoria MCP Server

MCP (Model Context Protocol) Server para integração com as APIs do CobranSaaS exclusivas para assessorias de cobrança.

Este servidor permite que assistentes de IA interajam com o sistema CobranSaaS através de linguagem natural, possibilitando consultas, negociações e operações com PIX.

> **AVISO IMPORTANTE**: Este é um projeto independente e de código aberto, desenvolvido pela comunidade. A empresa CobranSaaS **NÃO** é responsável pela manutenção, suporte ou correção de bugs deste projeto. Para questões relacionadas a este MCP Server, utilize as [Issues do GitHub](https://github.com/marcosgabbardo/cobransaas-assessoria-mcp-server/issues). Para suporte oficial do sistema CobranSaaS, entre em contato diretamente com a empresa através dos canais oficiais.

## Funcionalidades

### Consultas
- **Clientes**: Listar e buscar clientes distribuídos para a assessoria
- **Contratos**: Listar e buscar contratos (dívidas) dos clientes
- **Parcelas**: Listar e buscar parcelas de dívidas, obter boletos
- **Lotes**: Listar lotes de dívidas e seus registros
- **Data de Processamento**: Obter a data de processamento atual do CobranSaaS

### Negociações
- **Modalidades**: Listar modalidades de negociação disponíveis
- **Acordos**: Simular, efetivar, ativar, cancelar, integrar e concluir acordos
- **Propostas**: Efetivar propostas de acordo
- **Comissões**: Consultar comissões geradas
- **Liquidação**: Liquidar e estornar parcelas de acordos
- **Boletos de Acordo**: Obter e registrar boletos de parcelas de acordos

### Boletos
- **Listar**: Listar boletos com filtros diversos
- **Detalhes**: Obter detalhes e PDF de boletos
- **Registro**: Registrar boletos individual ou em lote

### PIX
- **QR Code**: Obter imagem do QR Code PIX
- **Registro**: Registrar PIX individual ou em lote
- **Parcelas de Acordo**: Registrar PIX para parcelas de acordos

### Tabulações
- **Histórico de Contatos**: Registrar tabulações de contato com clientes

## Instalação

### Via Git

```bash
# Clone o repositório
git clone https://github.com/marcosgabbardo/cobransaas-assessoria-mcp-server.git
cd cobransaas-assessoria-mcp-server

# Crie um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instale em modo desenvolvimento
pip install -e .
```

### Via pip (diretamente do GitHub)

```bash
pip install git+https://github.com/marcosgabbardo/cobransaas-assessoria-mcp-server.git
```

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (ou configure as variáveis de ambiente):

```env
# Host da API (obrigatório) - URL do tenant do CobranSaaS
# Cada cliente/assessoria possui uma URL específica fornecida pelo CobranSaaS
# Exemplos: https://empresa.cobransaas.com.br, https://assessoria.cobransaas.com.br
COBRANSAAS_HOST=https://seu-tenant.cobransaas.com.br

# OAuth2 Client Credentials (obrigatório)
# Credenciais fornecidas pelo CobranSaaS para acesso à API
COBRANSAAS_CLIENT_ID=seu_codigo
COBRANSAAS_CLIENT_SECRET=seu_token

# Configurações opcionais
COBRANSAAS_TIMEOUT=30
COBRANSAAS_MAX_RETRIES=3
```

> **Importante**: A URL do host (`COBRANSAAS_HOST`) é específica para cada tenant/cliente do CobranSaaS. Entre em contato com o suporte do CobranSaaS para obter a URL correta do seu ambiente.

### Configuração no Claude Desktop

Adicione ao arquivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cobransaas": {
      "command": "python",
      "args": ["-m", "cobransaas_mcp"],
      "env": {
        "COBRANSAAS_HOST": "https://seu-tenant.cobransaas.com.br",
        "COBRANSAAS_CLIENT_ID": "seu_codigo",
        "COBRANSAAS_CLIENT_SECRET": "seu_token"
      }
    }
  }
}
```

### Configuração no VSCode

Adicione ao arquivo `.vscode/mcp.json`:

```json
{
  "servers": {
    "cobransaas": {
      "command": "python",
      "args": ["-m", "cobransaas_mcp"],
      "env": {
        "COBRANSAAS_HOST": "https://seu-tenant.cobransaas.com.br",
        "COBRANSAAS_CLIENT_ID": "seu_codigo",
        "COBRANSAAS_CLIENT_SECRET": "seu_token"
      }
    }
  }
}
```

## Tools Disponíveis (43 tools)

### Consulta

| Tool | Descrição |
|------|-----------|
| `get_processing_date` | Obtém a data de processamento atual |
| `list_batches` | Lista lotes de dívidas |
| `get_batch` | Obtém detalhes de um lote |
| `list_batch_records` | Lista registros de um lote |
| `list_batch_records_delta` | Lista registros delta (incluídos/excluídos) |
| `list_clients` | Lista clientes |
| `get_client` | Obtém detalhes de um cliente |
| `list_contracts` | Lista contratos |
| `get_contract` | Obtém detalhes de um contrato |
| `list_installments` | Lista parcelas |
| `get_installment` | Obtém detalhes de uma parcela |
| `get_installment_boleto` | Obtém detalhes do boleto de uma parcela |
| `get_installment_boleto_pdf` | Obtém PDF do boleto de uma parcela |
| `register_installment_boleto` | Registra boleto de uma parcela |

### Negociação

| Tool | Descrição |
|------|-----------|
| `list_negotiation_types` | Lista modalidades de negociação |
| `list_agreements` | Lista acordos existentes |
| `get_agreement` | Obtém detalhes de um acordo |
| `simulate_agreement` | Simula acordo/renegociação |
| `execute_agreement` | Efetiva acordo/renegociação |
| `activate_agreement` | Ativa acordo pendente |
| `cancel_agreement` | Cancela um acordo |
| `integrate_agreement` | Marca acordo como integrado |
| `conclude_agreement` | Marca acordo como concluído |
| `get_agreement_boleto` | Obtém detalhes do boleto de parcela de acordo |
| `get_agreement_boleto_pdf` | Obtém PDF do boleto de parcela de acordo |
| `register_agreement_boleto` | Registra boleto de parcela de acordo |
| `register_agreement_boletos` | Registra boletos de acordo em lote |
| `settle_agreement_installment` | Liquida (baixa) parcela de acordo |
| `reverse_agreement_payment` | Estorna pagamento de parcela de acordo |
| `execute_proposal` | Efetiva proposta de acordo |
| `list_commissions` | Lista comissões |

### Tabulação

| Tool | Descrição |
|------|-----------|
| `list_tabulations` | Lista tipos de tabulação |
| `create_tabulation` | Registra nova tabulação |

### PIX

| Tool | Descrição |
|------|-----------|
| `get_pix_qrcode` | Obtém imagem do QR Code |
| `register_pix` | Registra PIX |
| `register_pix_batch` | Registra lista de PIX |
| `register_agreement_pix` | Registra PIX de parcela de acordo |
| `register_agreement_pix_batch` | Registra PIX de parcelas de acordo |

### Boletos

| Tool | Descrição |
|------|-----------|
| `list_boletos` | Lista boletos |
| `get_boleto` | Obtém detalhes de um boleto |
| `get_boleto_pdf` | Obtém PDF de um boleto |
| `register_boleto` | Registra um boleto |
| `register_boletos_batch` | Registra lista de boletos |

## Exemplos de Uso

### Consultar clientes

```
"Liste os clientes distribuídos para a assessoria"
```

### Buscar cliente por CPF

```
"Busque o cliente com CPF 12345678900"
```

### Simular acordo

```
"Simule um acordo para o cliente 123456 usando a negociação 789"
```

### Listar acordos pendentes

```
"Liste todos os acordos com situação PENDENTE"
```

### Ativar um acordo

```
"Ative o acordo com ID 123456789"
```

### Liquidar parcela de acordo

```
"Liquide a parcela 123 do acordo com valor de R$ 500,00"
```

## Desenvolvimento

### Requisitos

- Python 3.11+
- Dependências listadas no `pyproject.toml`

### Instalação para desenvolvimento

```bash
pip install -e ".[dev]"
```

### Executar testes

```bash
pytest
```

### Lint e formatação

```bash
ruff check .
ruff format .
mypy src/
```

## Arquitetura

```
src/cobransaas_mcp/
├── __init__.py          # Pacote principal
├── __main__.py          # Entry point
├── server.py            # MCP Server com 43 tools
├── config/
│   ├── __init__.py
│   └── settings.py      # Configurações (Pydantic Settings)
├── api/
│   ├── __init__.py
│   ├── client.py        # Cliente HTTP com OAuth2
│   ├── global_api.py    # Global API
│   ├── lotes_api.py     # Lotes API
│   ├── clientes_api.py  # Clientes API
│   ├── contratos_api.py # Contratos API
│   ├── parcelas_api.py  # Parcelas API
│   ├── negociacoes_api.py # Negociações API
│   ├── acordos_api.py   # Acordos API
│   ├── propostas_api.py # Propostas API
│   ├── comissoes_api.py # Comissões API
│   ├── tabulacoes_api.py # Tabulações API
│   ├── pix_api.py       # PIX API
│   └── boletos_api.py   # Boletos API
├── models/              # Modelos Pydantic (futuro)
└── tools/               # Tools organizados por categoria (futuro)
```

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Aviso Legal

Este projeto é uma iniciativa independente e open-source. Não possui qualquer vínculo oficial com a empresa CobranSaaS. O uso deste software é por conta e risco do usuário. Os desenvolvedores não se responsabilizam por quaisquer danos decorrentes do uso deste software.

## Autor

Marcos Gabbardo

## Links

- [CobranSaaS](https://cobransaas.com.br)
- [MCP Protocol](https://modelcontextprotocol.io)
