/*=============================================================================
PROJETO: Perfil dos Estudantes Brasileiros (2015–ano corrente)
ARQUIVO: 05_base_modelagem_classificacao.sql

OBJETIVO
-------------------------------------------------------------------------------
Preparar features no ano t para classificar o quartil de infraestrutura do
município no ano t+1. O último ano disponível não pode ser usado como treino,
pois não possui rótulo futuro.

A classificação é relativa ao ano seguinte: CRITICA representa o primeiro
quartil do índice futuro e CONSOLIDADA representa o quarto quartil.
==============================================================================*/

WITH base AS (
  SELECT
    *
  FROM `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano`
  WHERE indice_infraestrutura IS NOT NULL
    AND qtd_indicadores_disponiveis >= 6
    AND qtd_estudantes > 0
),

rotulos_futuros AS (
  SELECT
    ano,
    id_municipio,
    NTILE(4) OVER (
      PARTITION BY ano
      ORDER BY indice_infraestrutura
    ) AS quartil_infraestrutura_futuro,
    indice_infraestrutura AS indice_infraestrutura_futuro
  FROM base
),

features AS (
  SELECT
    atual.ano,
    atual.id_municipio,
    atual.nome_municipio,
    atual.sigla_uf,
    atual.regiao,
    atual.qtd_estudantes,
    atual.qtd_escolas,
    atual.indice_infraestrutura,
    atual.perc_agua_potavel,
    atual.perc_energia_rede_publica,
    atual.perc_esgoto_rede_publica,
    atual.perc_internet,
    atual.perc_internet_alunos,
    atual.perc_biblioteca,
    atual.perc_biblioteca_sala_leitura,
    atual.perc_lab_informatica,
    atual.perc_lab_ciencias,
    atual.perc_quadra,
    atual.perc_com_deficiencia,
    atual.perc_usa_transporte_publico,
    futuro.indice_infraestrutura_futuro,
    futuro.quartil_infraestrutura_futuro

  FROM base AS atual
  INNER JOIN rotulos_futuros AS futuro
    ON atual.id_municipio = futuro.id_municipio
   AND atual.ano + 1 = futuro.ano
)

SELECT
  *,
  CASE quartil_infraestrutura_futuro
    WHEN 1 THEN 'CRITICA'
    WHEN 2 THEN 'BAIXA'
    WHEN 3 THEN 'MEDIA'
    WHEN 4 THEN 'CONSOLIDADA'
    ELSE NULL
  END AS classe_infraestrutura_futura

FROM features;
