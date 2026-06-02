# BI Logistico de Turnos

Dashboard simples em Python para acompanhar viagens logisticas por horario,
turno, destino e veiculo.

A ideia do projeto foi transformar uma base CSV em uma visao mais facil de
consultar, com filtros, indicadores e graficos. A base publicada aqui e
ficticia, criada apenas para demonstracao.

## O que o dashboard mostra

- viagens por turno;
- horarios de saida;
- origem e destino;
- quantidade de veiculos;
- pedidos e peso transportado;
- agenda filtrada por turno, destino, veiculo e CPT.

## Turnos considerados

```text
T1: 05:20 ate 13:40
T2: 13:20 ate 21:40
T3: 22:00 ate 05:40
```

## Tecnologias

- Python
- Pandas
- Streamlit
- Plotly
- OpenPyXL

## Como rodar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Inicie o dashboard:

```bash
streamlit run app.py
```

## Arquivos principais

```text
app.py                         dashboard em Streamlit
data/dados_ficticios.csv       base usada na demonstracao
src/logistics_bi.py            tratamento dos dados e regras de turno
src/security.py                validacoes simples de entrada e exportacao
scripts/gerar_dados_ficticios.py
scripts/gerar_planilha_bi.py
```

## Dados

Este repositorio usa somente dados ficticios. Nomes, veiculos, rotas e volumes
foram criados para demonstracao e nao representam uma operacao real.

Arquivos locais com dados reais, CSVs exportados e planilhas `.xlsx` ficam fora
do Git pelo `.gitignore`.

## O que pratiquei neste projeto

- leitura e tratamento de CSV com Pandas;
- criacao de KPIs;
- classificacao de horarios por turno;
- construcao de dashboard com Streamlit;
- visualizacoes com Plotly;
- cuidado para publicar apenas dados ficticios.
