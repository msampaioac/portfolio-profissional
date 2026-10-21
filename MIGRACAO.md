# Consolidação do portfólio

**Data: 21/10/2026 · Entrada principal: `msampaioac/portfolio-profissional`**

[Voltar ao portfólio](README.md)

## Estrutura adotada

Os dois portfólios públicos foram incorporados às pastas `analise-dados/` e `gestao-estrategica-projetos/`. Os nomes internos de projetos e a organização da GENA por empresa e projeto foram preservados.

| Pasta no portfólio único | Repositório de origem | Referência incorporada |
|:---|:---|:---|
| `analise-dados/` | [data-analytics-portfolio](https://github.com/msampaioac/data-analytics-portfolio) | `ad0c4dd66755bdf07ff549dc43c96830b1bb5e18` — 65 arquivos e 36 commits no histórico principal |
| `gestao-estrategica-projetos/` | [gestao-estrategica-projetos-portfolio](https://github.com/msampaioac/gestao-estrategica-projetos-portfolio) | `fe692b7f1137a1400ac5449cfdaefff53a0d7318` — 37 arquivos e 14 commits no histórico principal |

## Conteúdo e histórico

A incorporação usa `git subtree` sem compactar os históricos principais. Cada commit de origem permanece ancestral da versão consolidada; os commits de importação registram os respectivos prefixos. Não houve reescrita das autorias dos históricos importados.

Os arquivos nos commits de importação foram comparados byte a byte com as versões de origem. Depois disso, as adaptações de navegação e comandos ficam registradas em um commit próprio, separado da importação.

Não foram importados conteúdos de repositórios privados ou de outros projetos da conta. Os repositórios de origem não foram apagados, renomeados nem arquivados; seus READMEs indicam o novo ponto de entrada para preservar links e a consulta ao histórico.

## Ajustes necessários

- Criar o índice único e links entre os dois portfólios.
- Corrigir a navegação de Perfil dos Estudantes Brasileiros para o diretório existente `(2015-ano-corrente)`.
- Adaptar comandos executados a partir da raiz para incluir `gestao-estrategica-projetos/`.
- Atualizar a geração das instruções de reprodução da Retenção EAD para reconhecer a raiz consolidada.
- Verificar links, imagens locais, âncoras e os testes de Retenção EAD e Governança.

As alterações de caminhos não modificam a versão da configuração, os dados, as premissas ou os indicadores fictícios da GENA. Os projetos de dados conservam seus SQL, notebooks, imagens e artefatos de Power BI.

## Evolução a partir desta consolidação

O trabalho corrente deve ser publicado neste repositório. Os originais permanecem como referências históricas; não há sincronização automática entre eles e esta estrutura. Atualizações futuras devem manter consistentes os índices, os links e os artefatos do projeto correspondente.
