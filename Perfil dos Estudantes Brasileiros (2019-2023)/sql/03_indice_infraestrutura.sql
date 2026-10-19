/*=============================================================================
PROJETO: Perfil dos Estudantes Brasileiros (2019–2023)
ARQUIVO: 03_indice_infraestrutura.sql

OBJETIVO
-------------------------------------------------------------------------------
Calcular um índice de infraestrutura escolar de 0 a 100 a partir da base
municipal-anual produzida em 02_base_infraestrutura_municipio_ano.sql.

SUBSTITUA o nome da tabela abaixo pela tabela criada no seu projeto BigQuery.
Valores nulos são tratados como não disponíveis, não como zero. O índice só é
produzido quando pelo menos seis dos dez indicadores de infraestrutura estão
disponíveis.
==============================================================================*/

WITH indicadores AS (
  SELECT
    * EXCEPT(
      perc_agua_potavel,
      perc_energia_rede_publica,
      perc_esgoto_rede_publica,
      perc_internet,
      perc_internet_alunos,
      perc_biblioteca,
      perc_biblioteca_sala_leitura,
      perc_lab_informatica,
      perc_lab_ciencias,
      perc_quadra
    ),

    (
      IF(perc_agua_potavel IS NOT NULL, 1, 0)
      + IF(perc_energia_rede_publica IS NOT NULL, 1, 0)
      + IF(perc_esgoto_rede_publica IS NOT NULL, 1, 0)
      + IF(perc_internet IS NOT NULL, 1, 0)
      + IF(perc_internet_alunos IS NOT NULL, 1, 0)
      + IF(perc_biblioteca IS NOT NULL, 1, 0)
      + IF(perc_biblioteca_sala_leitura IS NOT NULL, 1, 0)
      + IF(perc_lab_informatica IS NOT NULL, 1, 0)
      + IF(perc_lab_ciencias IS NOT NULL, 1, 0)
      + IF(perc_quadra IS NOT NULL, 1, 0)
    ) AS qtd_indicadores_disponiveis,

    (
      COALESCE(perc_agua_potavel, 0)
      + COALESCE(perc_energia_rede_publica, 0)
      + COALESCE(perc_esgoto_rede_publica, 0)
      + COALESCE(perc_internet, 0)
      + COALESCE(perc_internet_alunos, 0)
      + COALESCE(perc_biblioteca, 0)
      + COALESCE(perc_biblioteca_sala_leitura, 0)
      + COALESCE(perc_lab_informatica, 0)
      + COALESCE(perc_lab_ciencias, 0)
      + COALESCE(perc_quadra, 0)
    ) AS soma_indicadores

  FROM `seu_projeto.seu_dataset.base_infraestrutura_municipio_ano`
)

SELECT
  *,
  CASE
    WHEN qtd_indicadores_disponiveis >= 6
    THEN ROUND(
      SAFE_DIVIDE(soma_indicadores, qtd_indicadores_disponiveis),
      2
    )
    ELSE NULL
  END AS indice_infraestrutura,
  CASE
    WHEN qtd_indicadores_disponiveis >= 8 THEN 'ALTA'
    WHEN qtd_indicadores_disponiveis >= 6 THEN 'MEDIA'
    ELSE 'INSUFICIENTE'
  END AS qualidade_cobertura_indicadores

FROM indicadores;
