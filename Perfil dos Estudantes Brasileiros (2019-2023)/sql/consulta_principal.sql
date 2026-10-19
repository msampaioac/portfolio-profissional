/*==============================================================================
PROJETO
------------------------------------------------------------------------------
Perfil dos Estudantes Brasileiros (2015–ano corrente)

OBJETIVO
------------------------------------------------------------------------------
Construir uma base analítica consolidada sobre o perfil dos estudantes
brasileiros dos ensinos Fundamental, Médio e Superior, utilizando dados públicos
do INEP disponibilizados na Base dos Dados e consultados no Google BigQuery.

DESCRIÇÃO DA SOLUÇÃO
------------------------------------------------------------------------------
Este script integra dados do Censo Escolar, Censo da Educação Superior e
Diretório de Municípios, criando uma visão única para análise demográfica,
geográfica, institucional, social e de infraestrutura escolar.

FONTES DE DADOS
------------------------------------------------------------------------------
1. basedosdados.br_inep_censo_escolar.matricula
2. basedosdados.br_inep_censo_escolar.escola
3. basedosdados.br_inep_censo_educacao_superior.curso
4. basedosdados.br_inep_censo_educacao_superior.ies
5. basedosdados.br_bd_diretorios_brasil.municipio

JANELA TEMPORAL
------------------------------------------------------------------------------
2015 até o ano corrente no momento da execução.

A janela final é dinâmica e usa EXTRACT(YEAR FROM CURRENT_DATE()).

==============================================================================*/

DECLARE ano_inicio INT64 DEFAULT 2015;
DECLARE ano_fim INT64 DEFAULT EXTRACT(YEAR FROM CURRENT_DATE());

/*==============================================================================
CTE: educacao_basica
------------------------------------------------------------------------------
Consolida dados da Educação Básica: Ensino Fundamental e Ensino Médio.
==============================================================================*/
WITH educacao_basica AS (
  SELECT
    m.ano,
    'CENSO_ESCOLAR' AS fonte,

    -- Classificação das etapas de ensino.
    CASE
      WHEN CAST(m.etapa_ensino AS STRING) IN ('14','15','16','17','18','19','20','21','41') THEN 'ENSINO_FUNDAMENTAL'
      WHEN CAST(m.etapa_ensino AS STRING) IN ('25','26','27','28','29','30','31','32','33','34','35','36','37','38') THEN 'ENSINO_MEDIO'
      ELSE 'OUTRA_ETAPA'
    END AS nivel_ensino,

    m.sigla_uf,
    m.id_municipio,
    mun.nome AS nome_municipio,

    CAST(m.id_escola AS STRING) AS id_unidade_ensino,
    CAST(NULL AS STRING) AS nome_unidade_ensino,
    CAST(NULL AS STRING) AS id_curso,
    CAST(NULL AS STRING) AS nome_curso,
    CAST(NULL AS STRING) AS area_conhecimento,

    m.sexo,
    m.raca_cor,
    m.idade,
    m.nacionalidade,

    -- Tradução do código da rede de ensino da Educação Básica.
    CASE
      WHEN CAST(m.rede AS STRING) = '1' THEN 'Federal'
      WHEN CAST(m.rede AS STRING) = '2' THEN 'Estadual'
      WHEN CAST(m.rede AS STRING) = '3' THEN 'Municipal'
      WHEN CAST(m.rede AS STRING) = '4' THEN 'Privada'
      ELSE 'Não Informado'
    END AS rede,

    e.tipo_localizacao,
    e.tipo_localizacao_diferenciada,

    CAST(NULL AS STRING) AS tipo_modalidade_ensino,
    CAST(NULL AS STRING) AS tipo_grau_academico,
    CAST(NULL AS STRING) AS tipo_organizacao_academica,
    CAST(NULL AS STRING) AS tipo_organizacao_administrativa,

    -- Métrica principal da Educação Básica.
    COUNT(*) AS qtd_estudantes,

    -- Indicadores de inclusão e transporte.
    COUNTIF(CAST(m.necessidade_especial AS STRING) IN ('1','true','TRUE')) AS qtd_com_deficiencia,
    COUNTIF(CAST(m.transporte_publico AS STRING) IN ('1','true','TRUE')) AS qtd_usa_transporte_publico,

    -- Indicadores de infraestrutura escolar.
    COUNTIF(CAST(e.agua_potavel AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_agua_potavel,
    COUNTIF(CAST(e.energia_rede_publica AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_energia_rede_publica,
    COUNTIF(CAST(e.esgoto_rede_publica AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_esgoto_rede_publica,
    COUNTIF(CAST(e.internet AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_internet,
    COUNTIF(CAST(e.internet_alunos AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_internet_alunos,
    COUNTIF(CAST(e.biblioteca AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_biblioteca,
    COUNTIF(CAST(e.biblioteca_sala_leitura AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_biblioteca_sala_leitura,
    COUNTIF(CAST(e.laboratorio_informatica AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_lab_informatica,
    COUNTIF(CAST(e.laboratorio_ciencias AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_lab_ciencias,
    COUNTIF(CAST(e.quadra_esportes AS STRING) IN ('1','true','TRUE')) AS qtd_em_escola_com_quadra,

    -- Campos exclusivos do Ensino Superior.
    CAST(NULL AS INT64) AS qtd_financiamento,
    CAST(NULL AS INT64) AS qtd_reserva_vaga,
    CAST(NULL AS INT64) AS qtd_apoio_social,
    CAST(NULL AS INT64) AS qtd_atividade_extracurricular,
    CAST(NULL AS INT64) AS qtd_mobilidade_academica

  FROM `basedosdados.br_inep_censo_escolar.matricula` AS m

  LEFT JOIN `basedosdados.br_inep_censo_escolar.escola` AS e
    ON m.ano = e.ano
   AND m.id_escola = e.id_escola

  LEFT JOIN `basedosdados.br_bd_diretorios_brasil.municipio` AS mun
    ON m.id_municipio = mun.id_municipio

  WHERE m.ano BETWEEN ano_inicio AND ano_fim
    AND CAST(m.etapa_ensino AS STRING) IN (
      '14','15','16','17','18','19','20','21','41',
      '25','26','27','28','29','30','31','32','33','34','35','36','37','38'
    )

  GROUP BY
    m.ano,
    nivel_ensino,
    m.sigla_uf,
    m.id_municipio,
    nome_municipio,
    id_unidade_ensino,
    m.sexo,
    m.raca_cor,
    m.idade,
    m.nacionalidade,
    rede,
    e.tipo_localizacao,
    e.tipo_localizacao_diferenciada
),


/*==============================================================================
CTE: educacao_superior
------------------------------------------------------------------------------
Consolida dados do Ensino Superior.
==============================================================================*/
educacao_superior AS (
  SELECT
    c.ano,
    'CENSO_SUPERIOR' AS fonte,
    'ENSINO_SUPERIOR' AS nivel_ensino,

    c.sigla_uf,
    c.id_municipio,
    mun.nome AS nome_municipio,

    CAST(c.id_ies AS STRING) AS id_unidade_ensino,
    i.nome AS nome_unidade_ensino,
    CAST(c.id_curso AS STRING) AS id_curso,
    c.nome_curso,
    c.nome_area_geral AS area_conhecimento,

    -- Campos demográficos agregados no Ensino Superior.
    'AGREGADO' AS sexo,
    'AGREGADO' AS raca_cor,
    CAST(NULL AS INT64) AS idade,
    'AGREGADO' AS nacionalidade,

    -- Tradução do código da rede de ensino do Ensino Superior.
    CASE
      WHEN CAST(c.rede AS STRING) = '1' THEN 'Pública'
      WHEN CAST(c.rede AS STRING) = '2' THEN 'Privada'
      ELSE 'Não Informado'
    END AS rede,

    CAST(NULL AS STRING) AS tipo_localizacao,
    CAST(NULL AS STRING) AS tipo_localizacao_diferenciada,

    c.tipo_modalidade_ensino,
    c.tipo_grau_academico,
    c.tipo_organizacao_academica,
    c.tipo_organizacao_administrativa,

    -- Métrica principal do Ensino Superior.
    -- COALESCE evita que uma célula nula anule o total do agrupamento.
    COALESCE(SUM(c.quantidade_matriculas), 0) AS qtd_estudantes,

    -- Indicador de inclusão no Ensino Superior.
    COALESCE(SUM(c.quantidade_matriculas_deficiencia), 0) AS qtd_com_deficiencia,

    CAST(NULL AS INT64) AS qtd_usa_transporte_publico,

    -- Campos de infraestrutura aplicáveis apenas à Educação Básica.
    CAST(NULL AS INT64) AS qtd_em_escola_com_agua_potavel,
    CAST(NULL AS INT64) AS qtd_em_escola_com_energia_rede_publica,
    CAST(NULL AS INT64) AS qtd_em_escola_com_esgoto_rede_publica,
    CAST(NULL AS INT64) AS qtd_em_escola_com_internet,
    CAST(NULL AS INT64) AS qtd_em_escola_com_internet_alunos,
    CAST(NULL AS INT64) AS qtd_em_escola_com_biblioteca,
    CAST(NULL AS INT64) AS qtd_em_escola_com_biblioteca_sala_leitura,
    CAST(NULL AS INT64) AS qtd_em_escola_com_lab_informatica,
    CAST(NULL AS INT64) AS qtd_em_escola_com_lab_ciencias,
    CAST(NULL AS INT64) AS qtd_em_escola_com_quadra,

    -- Indicadores específicos do Ensino Superior.
    COALESCE(SUM(c.quantidade_matriculas_financiamento), 0) AS qtd_financiamento,
    COALESCE(SUM(c.quantidade_matriculas_reserva_vaga), 0) AS qtd_reserva_vaga,
    COALESCE(SUM(c.quantidade_matriculas_apoio_social), 0) AS qtd_apoio_social,
    COALESCE(SUM(c.quantidade_matriculas_atividade_extracurricular), 0) AS qtd_atividade_extracurricular,
    COALESCE(SUM(c.quantidade_matriculas_mobilidade_academica), 0) AS qtd_mobilidade_academica

  FROM `basedosdados.br_inep_censo_educacao_superior.curso` AS c

  LEFT JOIN `basedosdados.br_inep_censo_educacao_superior.ies` AS i
    ON c.ano = i.ano
   AND c.id_ies = i.id_ies

  LEFT JOIN `basedosdados.br_bd_diretorios_brasil.municipio` AS mun
    ON c.id_municipio = mun.id_municipio

  WHERE c.ano BETWEEN ano_inicio AND ano_fim

  GROUP BY
    c.ano,
    c.sigla_uf,
    c.id_municipio,
    nome_municipio,
    id_unidade_ensino,
    nome_unidade_ensino,
    id_curso,
    c.nome_curso,
    area_conhecimento,
    rede,
    c.tipo_modalidade_ensino,
    c.tipo_grau_academico,
    c.tipo_organizacao_academica,
    c.tipo_organizacao_administrativa
),


/*==============================================================================
CTE: base_unificada
------------------------------------------------------------------------------
Une os dados da Educação Básica e do Ensino Superior.
==============================================================================*/
base_unificada AS (
  SELECT * FROM educacao_basica
  UNION ALL
  SELECT * FROM educacao_superior
)


/*==============================================================================
RESULTADO FINAL COMPLETO (Todos os Níveis de Ensino)
------------------------------------------------------------------------------
Retorna a tabela analítica unificada com todas as quebras originais.
==============================================================================*/
SELECT
  ano,
  fonte,
  nivel_ensino,
  sigla_uf,
  id_municipio,
  nome_municipio,

  -- Classificação da região geográfica.
  CASE
    WHEN sigla_uf IN ('AC','AP','AM','PA','RO','RR','TO') THEN 'NORTE'
    WHEN sigla_uf IN ('AL','BA','CE','MA','PB','PE','PI','RN','SE') THEN 'NORDESTE'
    WHEN sigla_uf IN ('DF','GO','MT','MS') THEN 'CENTRO-OESTE'
    WHEN sigla_uf IN ('ES','MG','RJ','SP') THEN 'SUDESTE'
    WHEN sigla_uf IN ('PR','RS','SC') THEN 'SUL'
    ELSE 'NAO_IDENTIFICADO'
  END AS regiao,

  sexo,
  raca_cor,

  -- Criação de faixas etárias.
  CASE
    WHEN idade IS NULL THEN 'AGREGADO_SUPERIOR'
    WHEN idade BETWEEN 0 AND 5 THEN '00 A 05'
    WHEN idade BETWEEN 6 AND 10 THEN '06 A 10'
    WHEN idade BETWEEN 11 AND 14 THEN '11 A 14'
    WHEN idade BETWEEN 15 AND 17 THEN '15 A 17'
    WHEN idade BETWEEN 18 AND 24 THEN '18 A 24'
    WHEN idade BETWEEN 25 AND 29 THEN '25 A 29'
    WHEN idade BETWEEN 30 AND 34 THEN '30 A 34'
    WHEN idade BETWEEN 35 AND 39 THEN '35 A 39'
    WHEN idade BETWEEN 40 AND 49 THEN '40 A 49'
    WHEN idade BETWEEN 50 AND 59 THEN '50 A 59'
    WHEN idade >= 60 THEN '60+'
    ELSE 'NAO_INFORMADO'
  END AS faixa_etaria,

  nacionalidade,
  rede,
  tipo_localizacao,
  tipo_localizacao_diferenciada,
  tipo_modalidade_ensino,
  tipo_grau_academico,
  tipo_organizacao_academica,
  tipo_organizacao_administrativa,
  area_conhecimento,

  -- Métricas principais.
  SUM(qtd_estudantes) AS qtd_estudantes,
  SUM(qtd_com_deficiencia) AS qtd_com_deficiencia,
  SUM(qtd_usa_transporte_publico) AS qtd_usa_transporte_publico,

  -- Métricas de infraestrutura escolar.
  SUM(qtd_em_escola_com_agua_potavel) AS qtd_em_escola_com_agua_potavel,
  SUM(qtd_em_escola_com_energia_rede_publica) AS qtd_em_escola_com_energia_rede_publica,
  SUM(qtd_em_escola_com_esgoto_rede_publica) AS qtd_em_escola_com_esgoto_rede_publica,
  SUM(qtd_em_escola_com_internet) AS qtd_em_escola_com_internet,
  SUM(qtd_em_escola_com_internet_alunos) AS qtd_em_escola_com_internet_alunos,
  SUM(qtd_em_escola_com_biblioteca) AS qtd_em_escola_com_biblioteca,
  SUM(qtd_em_escola_com_biblioteca_sala_leitura) AS qtd_em_escola_com_biblioteca_sala_leitura,
  SUM(qtd_em_escola_com_lab_informatica) AS qtd_em_escola_com_lab_informatica,
  SUM(qtd_em_escola_com_lab_ciencias) AS qtd_em_escola_com_lab_ciencias,
  SUM(qtd_em_escola_com_quadra) AS qtd_em_escola_com_quadra,

  -- Métricas específicas do Ensino Superior.
  SUM(qtd_financiamento) AS qtd_financiamento,
  SUM(qtd_reserva_vaga) AS qtd_reserva_vaga,
  SUM(qtd_apoio_social) AS qtd_apoio_social,
  SUM(qtd_atividade_extracurricular) AS qtd_atividade_extracurricular,
  SUM(qtd_mobilidade_academica) AS qtd_mobilidade_academica,

  -- Indicadores percentuais.
  ROUND(SAFE_DIVIDE(SUM(qtd_com_deficiencia), SUM(qtd_estudantes)) * 100, 2) AS perc_com_deficiencia,
  ROUND(SAFE_DIVIDE(SUM(qtd_usa_transporte_publico), SUM(qtd_estudantes)) * 100, 2) AS perc_usa_transporte_publico,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_agua_potavel), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_agua_potavel,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_energia_rede_publica), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_energia_rede_publica,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_esgoto_rede_publica), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_esgoto_rede_publica,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_internet), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_internet,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_internet_alunos), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_internet_alunos,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_biblioteca), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_biblioteca,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_biblioteca_sala_leitura), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_biblioteca_sala_leitura,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_lab_informatica), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_lab_informatica,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_lab_ciencias), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_lab_ciencias,
  ROUND(SAFE_DIVIDE(SUM(qtd_em_escola_com_quadra), SUM(qtd_estudantes)) * 100, 2) AS perc_em_escola_com_quadra,
  ROUND(SAFE_DIVIDE(SUM(qtd_financiamento), SUM(qtd_estudantes)) * 100, 2) AS perc_financiamento,
  ROUND(SAFE_DIVIDE(SUM(qtd_reserva_vaga), SUM(qtd_estudantes)) * 100, 2) AS perc_reserva_vaga,
  ROUND(SAFE_DIVIDE(SUM(qtd_apoio_social), SUM(qtd_estudantes)) * 100, 2) AS perc_apoio_social,
  ROUND(SAFE_DIVIDE(SUM(qtd_atividade_extracurricular), SUM(qtd_estudantes)) * 100, 2) AS perc_atividade_extracurricular,
  ROUND(SAFE_DIVIDE(SUM(qtd_mobilidade_academica), SUM(qtd_estudantes)) * 100, 2) AS perc_mobilidade_academica

FROM base_unificada

GROUP BY
  ano,
  fonte,
  nivel_ensino,
  sigla_uf,
  id_municipio,
  nome_municipio,
  regiao,
  sexo,
  raca_cor,
  faixa_etaria,
  nacionalidade,
  rede,
  tipo_localizacao,
  tipo_localizacao_diferenciada,
  tipo_modalidade_ensino,
  tipo_grau_academico,
  tipo_organizacao_academica,
  tipo_organizacao_administrativa,
  area_conhecimento

ORDER BY
  ano,
  regiao,
  sigla_uf,
  nome_municipio,
  nivel_ensino,
  qtd_estudantes DESC
