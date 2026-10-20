# Reprodução

## Pré-requisitos

- conta Google Cloud com um projeto próprio para cobrança/quota;
- acesso ao BigQuery e aos datasets públicos da Base dos Dados;
- Python 3.10+ ou Google Colab;
- bibliotecas `basedosdados`, `google-cloud-bigquery`, `pandas`, `matplotlib` e `seaborn`.

## Snapshot validado da execução mais recente

A versão executada e incorporada ao repositório em 20/10/2026 apresentou:

- **4.582.798 linhas** e **54 colunas**;
- cobertura de **2015 a 2024**;
- níveis `ENSINO_FUNDAMENTAL`, `ENSINO_MEDIO` e `ENSINO_SUPERIOR`;
- fontes `CENSO_ESCOLAR` e `CENSO_SUPERIOR`;
- saídas gráficas atualizadas em `docs/assets/analise_01.png` a `analise_04.png`.

O indicador de conectividade da Educação Básica utilizado no gráfico ponderado apresentou cobertura até 2020 nesta execução, embora a base integrada contenha registros até 2024. Essa diferença de cobertura deve ser registrada antes de comparar todos os indicadores no mesmo horizonte temporal.

Esses números são um registro da execução, não valores fixos da consulta. Uma nova execução pode ampliar o ano final ou alterar a cobertura conforme a atualização das fontes.

## SQL

1. Abra `sql/consulta_principal.sql` no BigQuery usando GoogleSQL.
2. Confirme que o período retornado começa em 2015 e termina no maior ano disponível no momento da execução.
3. Execute a consulta e valide a existência das colunas descritas no dicionário de dados.
4. Para evitar custos inesperados, confira a estimativa de bytes processados e use filtros de ano durante a exploração.

5. Execute os testes de [`docs/validacao_consulta.md`](validacao_consulta.md) antes de atualizar o notebook ou o Power BI.

## Notebook

1. Abra `python/Perfil_Estudantes_Brasileiros.ipynb` no Colab ou Jupyter.
2. Instale as dependências da primeira célula.
3. Substitua `project_id` pelo seu próprio projeto Google Cloud; não use credenciais de terceiros.
4. Execute as células em ordem.
5. Confira os anos encontrados, o formato do DataFrame e os nulos esperados antes de interpretar os gráficos.

## Validações mínimas

- ano inicial esperado: 2015;
- ano final esperado: maior ano disponível na fonte no momento da execução;
- níveis de ensino esperados: Fundamental, Médio e Superior;
- percentuais entre 0 e 100;
- campos de infraestrutura nulos para registros do Ensino Superior quando não aplicáveis;
- nenhuma soma direta de percentuais entre agrupamentos.
- `qtd_estudantes` interpretado como contagem agregada de registros ou matrículas, não como uma linha individual por estudante.
