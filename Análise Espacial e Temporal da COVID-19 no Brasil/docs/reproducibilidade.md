# Reprodução

## Pré-requisitos

- Conta Google Cloud com um projeto próprio para cobrança/quota do BigQuery;
- acesso ao Google BigQuery;
- acesso aos datasets públicos da Base dos Dados;
- SQL configurado como GoogleSQL.

## Execução

1. Abra uma consulta em branco no BigQuery.
2. Copie uma consulta da pasta `sql/`.
3. Confirme os nomes das tabelas públicas e ajuste o período se necessário.
4. Execute a consulta, depois compare o resultado com os totais da fonte e faça as validações descritas em `docs/metodologia.md`.
5. Exporte o resultado para uma camada analítica ou conecte-o a uma ferramenta de BI.

## Cuidados

As consultas podem processar grandes volumes. Use filtros de período, selecione apenas as colunas necessárias e confira a estimativa de bytes antes de executar. Nenhuma credencial deve ser versionada no repositório.
