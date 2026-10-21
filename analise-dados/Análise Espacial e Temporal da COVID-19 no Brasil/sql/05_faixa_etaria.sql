/*
===============================================================================
Projeto : COVID-19 Brasil Analytics
Arquivo : 05_faixa_etaria.sql

Descrição
-------------------------------------------------------------------------------
Analisa cobertura vacinal por faixa etária e sexo.

===============================================================================
*/

WITH vacinacao AS (

    SELECT
        id_municipio_estabelecimento AS id_municipio,
        sexo_paciente AS sexo,

        CASE
            WHEN idade_paciente BETWEEN 0 AND 4 THEN '00-04'
            WHEN idade_paciente BETWEEN 5 AND 9 THEN '05-09'
            WHEN idade_paciente BETWEEN 10 AND 14 THEN '10-14'
            WHEN idade_paciente BETWEEN 15 AND 19 THEN '15-19'
            WHEN idade_paciente BETWEEN 20 AND 29 THEN '20-29'
            WHEN idade_paciente BETWEEN 30 AND 39 THEN '30-39'
            WHEN idade_paciente BETWEEN 40 AND 49 THEN '40-49'
            WHEN idade_paciente BETWEEN 50 AND 59 THEN '50-59'
            WHEN idade_paciente BETWEEN 60 AND 69 THEN '60-69'
            WHEN idade_paciente BETWEEN 70 AND 79 THEN '70-79'
            WHEN idade_paciente >= 80 THEN '80+'
            ELSE 'Ignorado'
        END AS faixa_etaria,

        COUNTIF(REGEXP_CONTAINS(LOWER(dose_vacina), r'1|primeira')) AS primeira_dose,
        COUNTIF(REGEXP_CONTAINS(LOWER(dose_vacina), r'2|segunda')) AS segunda_dose,
        COUNTIF(REGEXP_CONTAINS(LOWER(dose_vacina), r'refor')) AS dose_reforco

    FROM
        `basedosdados.br_ms_vacinacao_covid19.microdados`

    WHERE
        idade_paciente IS NOT NULL
        AND sexo_paciente IN ('M', 'F')

    GROUP BY
        id_municipio,
        sexo,
        faixa_etaria

),

resultado AS (

    SELECT
        sexo,
        faixa_etaria,

        SUM(primeira_dose) AS primeira_dose,
        SUM(segunda_dose) AS segunda_dose,
        SUM(dose_reforco) AS dose_reforco,

        SUM(primeira_dose + segunda_dose + dose_reforco) AS total_doses

    FROM
        vacinacao

    GROUP BY
        sexo,
        faixa_etaria

)

SELECT
    sexo,
    faixa_etaria,

    primeira_dose,
    segunda_dose,
    dose_reforco,
    total_doses,

    ROUND(
        SAFE_DIVIDE(segunda_dose, SUM(segunda_dose) OVER (PARTITION BY sexo)) * 100,
        2
    ) AS participacao_segunda_dose_por_sexo_pct,

    DENSE_RANK() OVER (
        PARTITION BY sexo
        ORDER BY segunda_dose DESC
    ) AS ranking_faixa_etaria

FROM
    resultado

ORDER BY
    sexo,
    ranking_faixa_etaria;
