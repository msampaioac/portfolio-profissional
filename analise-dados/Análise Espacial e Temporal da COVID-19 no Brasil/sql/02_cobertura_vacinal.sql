/*
===============================================================================
Projeto : COVID-19 Brasil Analytics
Arquivo : 02_cobertura_vacinal.sql

Descrição
-------------------------------------------------------------------------------
Calcula cobertura vacinal por município, UF e região, cruzando vacinação com
população municipal do IBGE.

===============================================================================
*/

WITH vacinacao_municipio AS (

    SELECT
        id_municipio_estabelecimento AS id_municipio,
        COUNT(*) AS total_doses,

        COUNTIF(REGEXP_CONTAINS(LOWER(dose_vacina), r'1|primeira')) AS primeira_dose,
        COUNTIF(REGEXP_CONTAINS(LOWER(dose_vacina), r'2|segunda')) AS segunda_dose,
        COUNTIF(REGEXP_CONTAINS(LOWER(dose_vacina), r'refor')) AS dose_reforco

    FROM
        `basedosdados.br_ms_vacinacao_covid19.microdados`

    WHERE
        id_municipio_estabelecimento IS NOT NULL

    GROUP BY
        id_municipio

),

populacao AS (

    SELECT
        id_municipio,
        populacao

    FROM
        `basedosdados.br_ibge_populacao.municipio`

    WHERE
        ano = 2021

),

municipios AS (

    SELECT
        id_municipio,
        nome AS municipio,
        sigla_uf,
        nome_regiao AS regiao

    FROM
        `basedosdados.br_bd_diretorios_brasil.municipio`

)

SELECT
    m.regiao,
    m.sigla_uf,
    m.municipio,
    v.id_municipio,

    p.populacao,

    v.total_doses,
    v.primeira_dose,
    v.segunda_dose,
    v.dose_reforco,

    ROUND(SAFE_DIVIDE(v.primeira_dose, p.populacao) * 100, 2) AS cobertura_primeira_dose_pct,
    ROUND(SAFE_DIVIDE(v.segunda_dose, p.populacao) * 100, 2) AS cobertura_segunda_dose_pct,
    ROUND(SAFE_DIVIDE(v.dose_reforco, p.populacao) * 100, 2) AS cobertura_reforco_pct,

    RANK() OVER (
        PARTITION BY m.sigla_uf
        ORDER BY SAFE_DIVIDE(v.segunda_dose, p.populacao) DESC
    ) AS ranking_municipal_uf

FROM
    vacinacao_municipio v

LEFT JOIN populacao p
    ON v.id_municipio = p.id_municipio

LEFT JOIN municipios m
    ON v.id_municipio = m.id_municipio

WHERE
    p.populacao > 0

ORDER BY
    cobertura_segunda_dose_pct DESC;-- SQL 2
