# BI Logistico de Turnos

Projeto de portfolio em Python para transformar uma base CSV de viagens em um
dashboard interativo de acompanhamento logistico por turno, destino e veiculo.

O objetivo e simular um cenario operacional real, mas usando somente dados
ficticios. Assim, o projeto pode ser publicado no GitHub e apresentado no
LinkedIn sem expor informacoes sensiveis.

## Visao geral

O dashboard permite acompanhar:

- Horario de saida dos veiculos.
- Turno operacional de cada viagem.
- Origem e destino das rotas.
- Quantidade de veiculos.
- Motoristas ficticios.
- Volume de pedidos e peso transportado.
- Status operacional.
- Filtros por turno, destino, veiculo e CPT.

Os turnos usados no projeto sao:

```text
T1: 05:20 ate 13:40
T2: 13:20 ate 21:40
T3: 22:00 ate 05:40
```

## Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Plotly
- OpenPyXL
- GitHub Actions
- Dependabot
- Bandit
- pip-audit

## Funcionalidades

- Leitura de CSV com dados ficticios.
- Consolidacao de viagens por origem e destino.
- Classificacao automatica de horarios em T1, T2 e T3.
- KPIs de viagens, veiculos, destinos, pedidos e peso.
- Graficos interativos por turno, destino e horario.
- Agenda operacional filtrada.
- Download de CSV filtrado.
- Geracao opcional de planilha Excel demonstrativa.
- Validacoes de seguranca para reduzir risco de vazamento ou abuso.

## Dados ficticios

Este repositorio nao contem dados reais de operacao, pessoas, veiculos, rotas,
clientes ou empresas.

A base publica fica em:

```text
data/dados_ficticios.csv
```

Os veiculos usam identificadores demonstrativos, como:

```text
VEICULO_DEMO_001
VEICULO_DEMO_002
```

Os motoristas tambem sao ficticios:

```text
Motorista Demo 001
Motorista Demo 002
```

## Como rodar o dashboard

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute o dashboard:

```bash
streamlit run app.py
```

## Como gerar uma nova base ficticia

```bash
python scripts/gerar_dados_ficticios.py
```

## Como gerar a planilha Excel demonstrativa

```bash
python scripts/gerar_planilha_bi.py
```

A planilha sera criada em:

```text
outputs/bi_logistico_ficticio.xlsx
```

## Estrutura do projeto

```text
.
|-- app.py
|-- data/
|   `-- dados_ficticios.csv
|-- docs/
|   |-- post_linkedin.md
|   `-- seguranca_github.md
|-- scripts/
|   |-- gerar_dados_ficticios.py
|   `-- gerar_planilha_bi.py
|-- src/
|   |-- __init__.py
|   |-- logistics_bi.py
|   `-- security.py
|-- .github/
|   |-- CODEOWNERS
|   |-- dependabot.yml
|   |-- pull_request_template.md
|   `-- workflows/security-checks.yml
|-- .streamlit/
|   `-- config.toml
|-- SECURITY.md
|-- requirements.txt
`-- README.md
```

## Como o codigo esta organizado

- `app.py`: interface do dashboard em Streamlit.
- `src/logistics_bi.py`: regras de consolidacao, horarios e turnos.
- `src/security.py`: validacoes de seguranca usadas pelo app e pelos scripts.
- `scripts/gerar_dados_ficticios.py`: cria uma base demonstrativa.
- `scripts/gerar_planilha_bi.py`: cria uma planilha Excel demonstrativa.
- `docs/post_linkedin.md`: sugestao de texto para publicacao no LinkedIn.

## Seguranca e privacidade

O projeto foi preparado para publicacao publica:

- Arquivos CSV reais sao ignorados pelo Git.
- Planilhas reais e arquivos `.xlsx` locais sao ignorados pelo Git.
- A pasta `Planilha Puxada/` fica fora do Git.
- A base publica e apenas `data/dados_ficticios.csv`.
- O app valida colunas obrigatorias antes de processar a base.
- O app limita o tamanho do CSV usado no dashboard.
- O app bloqueia caminhos fora da pasta do projeto.
- Exportacoes CSV e Excel sao sanitizadas contra formula injection.
- O GitHub Actions compila o projeto e executa verificacoes de seguranca.

Mais detalhes estao em:

```text
SECURITY.md
docs/seguranca_github.md
```

## O que este projeto demonstra

Este projeto mostra habilidades em:

- Tratamento de dados com Python.
- Criacao de dashboards interativos.
- Modelagem simples de regras operacionais.
- Organizacao de projeto para GitHub.
- Cuidados com privacidade de dados.
- Automacao de validacoes com GitHub Actions.

## Status

Projeto publicado como portfolio, com dados ficticios e sem dependencia de
informacoes reais.
