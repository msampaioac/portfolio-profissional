/*=============================================================================
PROJETO: Perfil dos Estudantes Brasileiros (2019–2023)
ARQUIVO: 02_base_infraestrutura_municipio_ano.sql

OBJETIVO
-------------------------------------------------------------------------------
Criar uma linha por município e ano para análises territoriais, clusterização e
construção do índice de infraestrutura escolar.

A unidade de análise é município-ano. A métrica qtd_estudantes representa a
contagem de registros de matrícula disponíveis na fonte para o agrupamento.
==============================================================================*/

WITH base_municipio_ano AS (
  SELECT
    m.ano,
    m.id_municipio,
    m.sigla_uf,
    mun.nome AS nome_municipio,
    CASE
      WHEN m.sigla_uf IN ('AC','AP','AM','PA','RO','RR','TO') THEN 'NORTE'
      WHEN m.sigla_uf IN ('AL','BA','CE','MA','PB','PE','PI','RN','SE') THEN 'NORDESTE'
      WHEN m.sigla_uf IN ('DF','GO','MT','MS') THEN 'CENTRO-OESTE'
      WHEN m.sigla_uf IN ('ES','MG','RJ','SP') THEN 'SUDESTE'
      WHEN m.sigla_uf IN ('PR','RS','SC') THEN 'SUL'
      ELSE 'NAO_IDENTIFICADO'
    END AS regiao,

    COUNT(*) AS qtd_estudantes,
    COUNT(DISTINCT m.id_escola) AS qtd_escolas,

    COUNTIF(CAST(e.agua_potavel AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_agua_potavel,
    COUNTIF(CAST(e.energia_rede_publica AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_energia_rede_publica,
    COUNTIF(CAST(e.esgoto_rede_publica AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_esgoto_rede_publica,
    COUNTIF(CAST(e.internet AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_internet,
    COUNTIF(CAST(e.internet_alunos AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_internet_alunos,
    COUNTIF(CAST(e.biblioteca AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_biblioteca,
    COUNTIF(CAST(e.biblioteca_sala_leitura AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_biblioteca_sala_leitura,
    COUNTIF(CAST(e.laboratorio_informatica AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_lab_informatica,
    COUNTIF(CAST(e.laboratorio_ciencias AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_lab_ciencias,
    COUNTIF(CAST(e.quadra_esportes AS STRING) IN ('1','true','TRUE'))
      AS qtd_estudantes_quadra,

    COUNTIF(CAST(m.necessidade_especial AS STRING) IN ('1','true','TRUE'))
      AS qtd_com_deficiencia,
    COUNTIF(CAST(m.transporte_publico AS STRING) IN ('1','true','TRUE'))
      AS qtd_usa_transporte_publico

  FROM `basedosdados.br_inep_censo_escolar.matricula` AS m

  LEFT JOIN `basedosdados.br_inep_censo_escolar.escola` AS e
    ON m.ano = e.ano
   AND m.id_escola = e.id_escola

  LEFT JOIN `basedosdados.br_bd_diretorios_brasil.municipio` AS mun
    ON m.id_municipio = mun.id_municipio

  WHERE m.ano BETWEEN 2019 AND 2023
    AND CAST(m.etapa_ensino AS STRING) IN (
      '14','15','16','17','18','19','20','21','41',
      '25','26','27','28','29','30','31','32',
      '33','34','35','36','37','38'
    )

  GROUP BY
    m.ano,
    m.id_municipio,
    m.sigla_uf,
    nome_municipio,
    regiao
)

SELECT
  ano,
  id_municipio,
  sigla_uf,
  regiao,
  nome_municipio,
  qtd_estudantes,
  qtd_escolas,

  ROUND(SAFE_DIVIDE(qtd_estudantes_agua_potavel, qtd_estudantes) * 100, 2)
    AS perc_agua_potavel,
  ROUND(SAFE_DIVIDE(qtd_estudantes_energia_rede_publica, qtd_estudantes) * 100, 2)
    AS perc_energia_rede_publica,
  ROUND(SAFE_DIVIDE(qtd_estudantes_esgoto_rede_publica, qtd_estudantes) * 100, 2)
    AS perc_esgoto_rede_publica,
  ROUND(SAFE_DIVIDE(qtd_estudantes_internet, qtd_estudantes) * 100, 2)
    AS perc_internet,
  ROUND(SAFE_DIVIDE(qtd_estudantes_internet_alunos, qtd_estudantes) * 100, 2)
    AS perc_internet_alunos,
  ROUND(SAFE_DIVIDE(qtd_estudantes_biblioteca, qtd_estudantes) * 100, 2)
    AS perc_biblioteca,
  ROUND(SAFE_DIVIDE(qtd_estudantes_biblioteca_sala_leitura, qtd_estudantes) * 100, 2)
    AS perc_biblioteca_sala_leitura,
  ROUND(SAFE_DIVIDE(qtd_estudantes_lab_informatica, qtd_estudantes) * 100, 2)
    AS perc_lab_informatica,
  ROUND(SAFE_DIVIDE(qtd_estudantes_lab_ciencias, qtd_estudantes) * 100, 2)
    AS perc_lab_ciencias,
  ROUND(SAFE_DIVIDE(qtd_estudantes_quadra, qtd_estudantes) * 100, 2)
    AS perc_quadra,
  ROUND(SAFE_DIVIDE(qtd_com_deficiencia, qtd_estudantes) * 100, 2)
    AS perc_com_deficiencia,
  ROUND(SAFE_DIVIDE(qtd_usa_transporte_publico, qtd_estudantes) * 100, 2)
    AS perc_usa_transporte_publico

FROM base_municipio_ano

ORDER BY ano, regiao, sigla_uf, nome_municipio;
