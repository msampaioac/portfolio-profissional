# Reprodução

## Pré-requisitos

- conta Google Cloud com um projeto próprio para cobrança/quota;
- acesso ao BigQuery e aos datasets públicos da Base dos Dados;
- Python 3.10+ ou Google Colab;
- bibliotecas `basedosdados`, `google-cloud-bigquery`, `pandas`, `matplotlib` e `seaborn`.

## SQL

1. Abra `sql/consulta_principal.sql` no BigQuery usando GoogleSQL.
2. Confirme que o período está entre 2019 e 2023.
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

- anos presentes: 2019, 2020, 2021, 2022 e 2023;
- níveis de ensino esperados: Fundamental, Médio e Superior;
- percentuais entre 0 e 100;
- campos de infraestrutura nulos para registros do Ensino Superior quando não aplicáveis;
- nenhuma soma direta de percentuais entre agrupamentos.
- `qtd_estudantes` interpretado como contagem agregada de registros ou matrículas, não como uma linha individual por estudante.
