# Como proteger o repositorio no GitHub

O codigo deste projeto ja tem validacoes e arquivos de apoio, mas a protecao
contra alteracoes indevidas depende tambem das configuracoes do GitHub.

## Branch protection

No GitHub, acesse `Settings > Branches > Add branch protection rule` e use:

- Branch name pattern: `main`
- Require a pull request before merging
- Require approvals
- Require review from Code Owners
- Require status checks to pass before merging
- Status check: `validate-project`
- Do not allow bypassing the above settings

## Seguranca do repositorio

Em `Settings > Code security and analysis`, ative:

- Dependabot alerts
- Dependabot security updates
- Secret scanning
- Push protection

## Regra de ouro

Nunca envie para o GitHub arquivos reais de operacao, placas, nomes, rotas,
planilhas internas, tokens ou senhas. Use apenas os dados ficticios do projeto.
