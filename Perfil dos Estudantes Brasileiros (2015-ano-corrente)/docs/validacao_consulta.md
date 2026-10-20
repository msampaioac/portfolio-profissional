# Validação da consulta analítica

A consulta principal deve ser validada antes do consumo no Power BI ou no notebook. Como ela retorna uma base agregada, os testes abaixo verificam a consistência da saída e não tentam validar registros individuais.

## Como executar

1. Execute `sql/consulta_principal.sql` no BigQuery.
2. Para executar os testes abaixo, salve o resultado em uma tabela temporária ou substitua `projeto.dataset.perfil_estudantes_2015_atual` pelo nome da tabela criada.
3. Registre a data da execução, o período consultado e a estimativa de bytes processados.

## Evidência da última execução registrada

O notebook executado e versionado apresentou **4.582.798 linhas**, **54 colunas** e anos de **2015 a 2024**. A tabela de cobertura mostrou a seguinte quantidade agregada de estudantes por ano:

| Ano | Linhas | Estudantes | Municípios |
|---:|---:|---:|---:|
| 2015 | 704.689 | 42.856.884 | 5.570 |
| 2016 | 708.667 | 43.404.552 | 5.570 |
| 2017 | 711.621 | 43.434.265 | 5.570 |
| 2018 | 712.265 | 43.321.783 | 5.570 |
| 2019 | 702.502 | 42.994.147 | 5.570 |
| 2020 | 695.492 | 42.950.528 | 5.570 |
| 2021 | 72.429 | 8.987.120 | 3.042 |
| 2022 | 84.989 | 9.444.116 | 3.310 |
| 2023 | 93.533 | 9.977.217 | 3.495 |
| 2024 | 96.611 | 10.227.266 | 3.551 |

A redução de cobertura observada a partir de 2021 deve ser investigada antes de comparações temporais nacionais. Ela pode refletir diferenças de disponibilidade, granularidade ou atualização das fontes integradas; não deve ser interpretada automaticamente como queda real de matrículas.

Além disso, o indicador `perc_em_escola_com_internet` utilizado na visualização ponderada da Educação Básica apresentou dados até 2020 nesta execução. A cobertura de cada indicador deve ser verificada separadamente, e não apenas pelo `MIN(ano)` e `MAX(ano)` da base integrada.

## Testes recomendados

### Cobertura do período e dos níveis

```sql
SELECT
  MIN(ano) AS menor_ano,
  MAX(ano) AS maior_ano,
  COUNT(DISTINCT ano) AS quantidade_anos,
  ARRAY_AGG(DISTINCT nivel_ensino ORDER BY nivel_ensino) AS niveis
FROM `projeto.dataset.perfil_estudantes_2015_atual`;
```

Resultado esperado: `menor_ano = 2015`, `maior_ano` igual ao último ano disponível na fonte e os níveis `ENSINO_FUNDAMENTAL`, `ENSINO_MEDIO` e `ENSINO_SUPERIOR`.

### Percentuais fora do intervalo

```sql
SELECT COUNT(*) AS linhas_invalidas
FROM `projeto.dataset.perfil_estudantes_2015_atual`
WHERE perc_com_deficiencia < 0 OR perc_com_deficiencia > 100
   OR perc_usa_transporte_publico < 0 OR perc_usa_transporte_publico > 100
   OR perc_em_escola_com_internet < 0 OR perc_em_escola_com_internet > 100
   OR perc_em_escola_com_agua_potavel < 0 OR perc_em_escola_com_agua_potavel > 100
   OR perc_em_escola_com_energia_rede_publica < 0 OR perc_em_escola_com_energia_rede_publica > 100
   OR perc_em_escola_com_esgoto_rede_publica < 0 OR perc_em_escola_com_esgoto_rede_publica > 100
   OR perc_financiamento < 0 OR perc_financiamento > 100;
```

Resultado esperado: `linhas_invalidas = 0`. Percentuais não aplicáveis ao Ensino Superior devem permanecer nulos, e não ser convertidos artificialmente em zero.

### Contagens negativas ou inválidas

```sql
SELECT COUNT(*) AS linhas_invalidas
FROM `projeto.dataset.perfil_estudantes_2015_atual`
WHERE qtd_estudantes < 0
   OR qtd_com_deficiencia < 0
   OR qtd_usa_transporte_publico < 0
   OR qtd_financiamento < 0;
```

Resultado esperado: `linhas_invalidas = 0`.

### Consistência das dimensões específicas

```sql
SELECT
  COUNTIF(fonte = 'CENSO_SUPERIOR' AND tipo_localizacao IS NOT NULL) AS superior_com_localizacao,
  COUNTIF(fonte = 'CENSO_ESCOLAR' AND tipo_modalidade_ensino IS NOT NULL) AS basica_com_modalidade_superior,
  COUNTIF(fonte = 'CENSO_SUPERIOR' AND qtd_em_escola_com_internet IS NOT NULL) AS superior_com_internet_escolar
FROM `projeto.dataset.perfil_estudantes_2015_atual`;
```

Resultado esperado: os três contadores devem ser zero, salvo se a fonte ou a regra de modelagem for alterada.

### Duplicidade na granularidade declarada

A combinação abaixo representa a granularidade documentada da saída. Caso o resultado retorne linhas, existe uma dimensão não documentada ou uma duplicidade que precisa ser investigada.

```sql
SELECT
  ano, fonte, nivel_ensino, sigla_uf, id_municipio, nome_municipio,
  sexo, raca_cor, faixa_etaria, nacionalidade, rede,
  tipo_localizacao, tipo_localizacao_diferenciada,
  tipo_modalidade_ensino, tipo_grau_academico,
  tipo_organizacao_academica, tipo_organizacao_administrativa,
  area_conhecimento,
  COUNT(*) AS quantidade_linhas
FROM `projeto.dataset.perfil_estudantes_2015_atual`
GROUP BY ALL
HAVING quantidade_linhas > 1;
```

## Interpretação

Os testes não comprovam que os dados de origem estão corretos. Eles verificam se a transformação preservou regras básicas de período, faixa de valores, aplicabilidade dos indicadores e granularidade. A comparação com totais publicados pelo INEP deve continuar sendo feita para cada ano e nível de ensino.
