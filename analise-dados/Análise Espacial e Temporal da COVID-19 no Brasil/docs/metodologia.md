# Metodologia

## 1. Problema e unidade de análise

As perguntas são respondidas em diferentes níveis: dia e UF para velocidade de vacinação; município para cobertura, infraestrutura e pressão hospitalar; faixa etária para distribuição de doses. Cada consulta explicita seu nível de agregação para reduzir interpretações indevidas.

## 2. Preparação e integração

As fontes são consultadas na Base dos Dados usando BigQuery. As consultas filtram o período relevante, agregam fatos, integram população e território e aplicam `SAFE_DIVIDE` para gerar indicadores proporcionais.

## 3. Transformações

- vacinação diária, acumulada e média móvel de sete dias;
- cobertura por município e ranking territorial;
- leitos e casos/óbitos em denominadores populacionais;
- classificação por faixa etária;
- tratamento de nulos com `COALESCE` quando a regra do indicador permite.

## 4. Validação

Antes do consumo em BI, recomenda-se conferir: duplicidade de chaves, cobertura de datas, população positiva, proporções entre 0 e 100, municípios sem correspondência territorial e totais agregados contra a fonte oficial.

## 5. Interpretação

Os resultados são descritivos e exploratórios. Uma taxa ou ranking pode indicar prioridade de investigação, mas não prova que vacinação ou infraestrutura causou determinado resultado de mortalidade.
