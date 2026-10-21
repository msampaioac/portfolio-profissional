/*
===============================================================================
Projeto : COVID-19 Brasil Analytics
Arquivo : 03_infraestrutura_vs_obitos.sql

Descrição
-------------------------------------------------------------------------------
Analisa a relação entre infraestrutura hospitalar municipal e óbitos por
SRAG/COVID-19.

===============================================================================
*/

WITH infraestrutura AS (

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

obitos AS (

    SELECT
        id_municipio_residencia AS id_municipio,
        COUNT(*) AS obitos_covid

    FROM
        `basedosdados.br_ms_sinan.microdados_influenza_srag`

    WHERE
        id_municipio_residencia IS NOT NULL
        AND LOWER(classificacao_final) LIKE '%covid%'
        AND LOWER(evolucao_caso) LIKE '%óbito%'

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
        ano = 2020

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

    p.populacao,

    COALESCE(i.leitos_urgencia, 0) AS leitos_urgencia,
    COALESCE(o.obitos_covid, 0) AS obitos_covid,

    ROUND(SAFE_DIVIDE(i.leitos_urgencia, p.populacao) * 100000, 2) AS leitos_por_100_mil_hab,
    ROUND(SAFE_DIVIDE(o.obitos_covid, p.populacao) * 100000, 2) AS obitos_por_100_mil_hab,

    NTILE(5) OVER (
        ORDER BY SAFE_DIVIDE(i.leitos_urgencia, p.populacao)
    ) AS quintil_infraestrutura

FROM
    populacao p

LEFT JOIN infraestrutura i
    ON p.id_municipio = i.id_municipio

LEFT JOIN obitos o
    ON p.id_municipio = o.id_municipio

LEFT JOIN municipios m
    ON p.id_municipio = m.id_municipio

WHERE
    p.populacao > 0

ORDER BY
    obitos_por_100_mil_hab DESC;
