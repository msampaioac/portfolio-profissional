/*=============================================================================
PROJETO: Perfil dos Estudantes Brasileiros (2019–2023)
ARQUIVO: 06_serie_temporal_previsao.sql

OBJETIVO
-------------------------------------------------------------------------------
Gerar uma série anual por UF para previsão no Colab. O índice estadual é uma
média ponderada pelo número de registros/matrículas do município.

Com apenas cinco anos, esta saída deve ser usada inicialmente para validação
descritiva e comparação de baselines. Modelos complexos exigem atualização do
período ou uma série com maior frequência.
==============================================================================*/

SELECT
  ano,
  sigla_uf,
  ANY_VALUE(regiao) AS regiao,
  SUM(qtd_estudantes) AS qtd_estudantes,
  SUM(qtd_escolas) AS qtd_escolas,
  ROUND(
    SAFE_DIVIDE(
      SUM(indice_infraestrutura * qtd_estudantes),
      SUM(qtd_estudantes)
    ),
    2
  ) AS indice_infraestrutura_ponderado,
  ROUND(
    SAFE_DIVIDE(
      SUM(perc_internet * qtd_estudantes),
      SUM(qtd_estudantes)
    ),
    2
  ) AS perc_internet_ponderado,
  ROUND(
    SAFE_DIVIDE(
      SUM(perc_internet_alunos * qtd_estudantes),
      SUM(qtd_estudantes)
    ),
    2
  ) AS perc_internet_alunos_ponderado,
  ROUND(
    SAFE_DIVIDE(
      SUM(perc_com_deficiencia * qtd_estudantes),
      SUM(qtd_estudantes)
    ),
    2
  ) AS perc_com_deficiencia_ponderado

FROM `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano`

WHERE indice_infraestrutura IS NOT NULL
  AND qtd_estudantes > 0

GROUP BY ano, sigla_uf

ORDER BY sigla_uf, ano;
