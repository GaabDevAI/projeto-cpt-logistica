# Politica de seguranca

Este projeto foi preparado para portfolio e usa apenas dados ficticios.
Nenhum repositorio publico deve ser tratado como impossivel de modificar por
terceiros, mas as protecoes abaixo reduzem risco de vazamento, abuso e alteracao
sem revisao.

## Dados sensiveis

- Nao publique arquivos reais de operacao, clientes, pessoas, placas ou rotas.
- Arquivos CSV reais, planilhas `.xlsx` e a pasta `Planilha Puxada/` estao no
  `.gitignore`.
- Use apenas `data/dados_ficticios.csv` no repositorio publico.

## Protecoes implementadas no codigo

- Validacao de colunas obrigatorias do CSV.
- Limite maximo de linhas para evitar arquivos gigantes.
- Bloqueio de caminhos fora da pasta do projeto.
- Sanitizacao de textos exportados para CSV/Excel contra formula injection.
- Dados de demonstracao sem nomes, placas ou rotas reais.
- Auditoria de dependencias com `pip-audit` no GitHub Actions.
- Analise estatica de seguranca com `bandit` no GitHub Actions.

## Recomendacoes para GitHub

Ative estas opcoes no repositorio:

- Branch protection na branch `main`.
- Exigir pull request antes de merge.
- Exigir revisao do Code Owner `@GaabDevAI`.
- Exigir status checks do GitHub Actions.
- Ativar Dependabot alerts.
- Ativar Dependabot security updates.
- Ativar secret scanning.
- Ativar push protection.
- Nao commitar arquivos `.xlsx`, `.csv` reais ou credenciais.

Veja tambem `docs/seguranca_github.md`.

## Reportar problema

Se encontrar algum dado real ou falha de seguranca, abra uma issue privada ou
remova o arquivo antes de publicar o repositorio.
