# Consolidação do portfólio

**Consolidação e limpeza: 21/10/2026 · Entrada principal: `msampaioac/portfolio-profissional`**

[Voltar ao portfólio](README.md)

## Estrutura adotada

Atualmente, os dois portfólios estão organizados em `analise-dados/` e `gestao-negocios/`. A pasta de gestão foi originalmente incorporada como `gestao-estrategica-projetos/` e renomeada para `gestao-negocios/` em 21/10/2026. Os nomes internos dos projetos e a organização da GENA por empresa e projeto foram preservados. Após verificação de redundância e confirmação do proprietário, os dois repositórios de origem foram excluídos.

| Pasta no portfólio único | Repositório de origem excluído | Referência originalmente incorporada |
|:---|:---|:---|
| [analise-dados](analise-dados/README.md) | `msampaioac/data-analytics-portfolio` | [ad0c4dd](https://github.com/msampaioac/portfolio-profissional/commit/ad0c4dd66755bdf07ff549dc43c96830b1bb5e18) — 65 arquivos e 36 commits no histórico principal à época da importação |
| [gestao-negocios](gestao-negocios/README.md) | `msampaioac/gestao-estrategica-projetos-portfolio` | [fe692b7](https://github.com/msampaioac/portfolio-profissional/commit/fe692b7f1137a1400ac5449cfdaefff53a0d7318) — 37 arquivos e 14 commits no histórico principal à época da importação |

## Conteúdo e histórico

A incorporação utiliza `git subtree` sem compactar os históricos principais. Cada commit originalmente importado permanece ancestral da consolidação. As adaptações de navegação e comandos estão registradas separadamente, sem reescrita das autorias importadas.

Antes da exclusão, uma nova comparação confirmou que não havia arquivos ausentes no portfólio único. As diferenças eram os avisos históricos nos originais e as adaptações de documentação e caminhos feitas na consolidação. SQL, notebooks, imagens, modelos de Power BI e dados fictícios da GENA foram preservados.

Os snapshots finais, incluindo os avisos de transição, também foram conservados:

| Origem | Tag histórica neste repositório | Último snapshot |
|:---|:---|:---|
| Análise de Dados | `origem/analise-dados-2026-10-21` | [a47a957](https://github.com/msampaioac/portfolio-profissional/commit/a47a9574ff70ce002fd1cf1f2a3739954173b6c8) |
| Gestão Estratégica e de Projetos | `origem/gestao-estrategica-projetos-2026-10-21` | [2aa4138](https://github.com/msampaioac/portfolio-profissional/commit/2aa41387c6f50befad63e2543350efe4f41752e3) |

Essas tags guardam as árvores antigas para consulta histórica; não são pastas de trabalho adicionais. O desenvolvimento corrente ocorre nas duas pastas da branch `main`.

## Auditoria e exclusão dos redundantes

A auditoria verificou, em cada origem, uma única branch (`main`) e ausência de tags adicionais, issues, pull requests, releases, forks e estrelas. Não havia discussões habilitadas. Foi criado e validado um backup em bundles Git de todas as referências disponíveis, acompanhado dos metadados públicos consultados, antes de executar a exclusão.

Com confirmação explícita, foram removidos somente `data-analytics-portfolio` e `gestao-negocios-portfolio`. O repositório principal e os demais projetos da conta não foram excluídos. Os endereços antigos deixam de funcionar; as referências de navegação desta documentação apontam para o portfólio único ou para commits preservados nele.

O backup Git permite reconstruir cópias locais, mas não recria a identidade dos repositórios excluídos no GitHub, seus links externos ou configurações de conta.

## Ajustes aplicados na consolidação

- Criar o índice único e links entre os dois portfólios.
- Corrigir a navegação de Perfil dos Estudantes Brasileiros para o diretório existente `(2015-ano-corrente)`.
- Adaptar comandos executados a partir da raiz para incluir `gestao-negocios/`.
- Atualizar a geração das instruções de reprodução da Retenção EAD para reconhecer a raiz consolidada.
- Verificar links, imagens locais, âncoras e os testes de Retenção EAD e Governança.
- Atualizar o guia e este registro após a exclusão dos redundantes, sem deixar links ativos para os endereços removidos.

As alterações de caminhos e a limpeza dos repositórios não modificam a versão da configuração, os dados, as premissas ou os indicadores fictícios da GENA.

## Evolução a partir desta consolidação

Todo o trabalho corrente deve ser publicado em `portfolio-profissional`. Atualizações futuras devem manter consistentes os índices, os links e os artefatos do projeto correspondente, sem recriar os repositórios redundantes.
