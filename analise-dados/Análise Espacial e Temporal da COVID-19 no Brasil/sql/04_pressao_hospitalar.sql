/*
===============================================================================
Projeto : COVID-19 Brasil Analytics
Arquivo : 04_pressao_hospitalar.sql

Descrição
-------------------------------------------------------------------------------
Calcula pressão hospitalar municipal a partir da relação entre internações,
óbitos e leitos disponíveis.

===============================================================================
*/

WITH casos_graves AS (

    SELECT
        id_municipio_residencia AS id_municipio,

        COUNT(*) AS internacoes_srag_covid,

        COUNTIF(
            LOWER(evolucao_caso) LIKE '%óbito%'
        ) AS obitos_srag_covid

    FROM
        `basedosdados.br_ms_sinan.microdados_influenza_srag`

    WHERE
        id_municipio_residencia IS NOT NULL
        AND LOWER(classificacao_final) LIKE '%covid%'

    GROUP BY
        id_municipio

),

leitos AS (

    SELECT
        id_municipio,

        SUM(
            COALESCE(quantidade_leito_repouso_feminino_urgencia, 0) +
            COALESCE(quantidade_leito_repouso_masculino_urgencia, 0) +
            COALESCE(quantidade_leito_repouso_indiferenciado_urgencia, 0)
        ) AS leitos_urgencia

    FROM
        `basedosdados.br_ms_cnes.estabelecimento`

    WHERE
        ano = 2020
        AND id_municipio IS NOT NULL

    GROUP BY
        id_municipio

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

    c.internacoes_srag_covid,
    c.obitos_srag_covid,

    l.leitos_urgencia,

    ROUND(SAFE_DIVIDE(c.internacoes_srag_covid, l.leitos_urgencia), 2) AS internacoes_por_leito,
    ROUND(SAFE_DIVIDE(c.obitos_srag_covid, l.leitos_urgencia), 2) AS obitos_por_leito,

    RANK() OVER (
        ORDER BY SAFE_DIVIDE(c.internacoes_srag_covid, l.leitos_urgencia) DESC
    ) AS ranking_pressao_hospitalar

FROM
    casos_graves c

LEFT JOIN leitos l
    ON c.id_municipio = l.id_municipio

LEFT JOIN municipios m
    ON c.id_municipio = m.id_municipio

WHERE
    l.leitos_urgencia > 0

ORDER BY
    ranking_pressao_hospitalar;
