/*
===============================================================================
Projeto : COVID-19 Brasil Analytics
Arquivo : 01_velocidade_vacinacao.sql
Autor   : Marcelo Sampaio

Descrição
-------------------------------------------------------------------------------
Analisa a evolução diária da vacinação por Unidade Federativa (UF),
calculando:

• Total de doses aplicadas por dia
• Acumulado de doses
• Média móvel de 7 dias
• Variação diária da média móvel
• Crescimento percentual da vacinação

Conceitos utilizados

✓ CTEs
✓ Window Functions
✓ SUM() OVER
✓ AVG() OVER
✓ LAG()
✓ SAFE_DIVIDE()
✓ ROUND()

===============================================================================
*/

--------------------------------------------------------------------------------
-- ETAPA 1: Total de doses aplicadas por UF e por dia
--------------------------------------------------------------------------------
WITH vacinas_diarias AS (
    SELECT
        sigla_uf,
        DATE(data_aplicacao_vacina) AS data_vacinacao,
        COUNT(*) AS doses_aplicadas
    FROM
        `basedosdados.br_ms_vacinacao_covid19.microdados`
    WHERE
        data_aplicacao_vacina IS NOT NULL
        AND sigla_uf IS NOT NULL
    GROUP BY
        sigla_uf,
        data_vacinacao
),

--------------------------------------------------------------------------------
-- ETAPA 2: Acumulado e média móvel
--------------------------------------------------------------------------------
serie_temporal AS (
    SELECT
        sigla_uf,
        data_vacinacao,
        doses_aplicadas,
        -- Total acumulado
        SUM(doses_aplicadas) OVER (
            PARTITION BY sigla_uf
            ORDER BY data_vacinacao
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS doses_acumuladas,
        -- Média móvel de sete dias
        AVG(doses_aplicadas) OVER (
            PARTITION BY sigla_uf
            ORDER BY data_vacinacao
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS media_movel_7d
    FROM 
        vacinas_diarias
),

--------------------------------------------------------------------------------
-- ETAPA 3: Recupera valores do dia anterior
--------------------------------------------------------------------------------
comparativo AS (
    SELECT
        *,
        LAG(doses_aplicadas) OVER (
            PARTITION BY sigla_uf
            ORDER BY data_vacinacao
        ) AS doses_dia_anterior,
        LAG(media_movel_7d) OVER (
            PARTITION BY sigla_uf
            ORDER BY data_vacinacao
        ) AS media_movel_anterior
    FROM 
        serie_temporal
)

--------------------------------------------------------------------------------
-- RESULTADO FINAL
--------------------------------------------------------------------------------
SELECT
    sigla_uf,
    data_vacinacao,
    doses_aplicadas,
    doses_acumuladas,
    ROUND(media_movel_7d, 2) AS media_movel_7_dias,
    ROUND(media_movel_7d - media_movel_anterior, 2) AS variacao_media_movel,
    ROUND(
        SAFE_DIVIDE(
            doses_aplicadas - doses_dia_anterior, 
            doses_dia_anterior
        ) * 100, 
        2
    ) AS crescimento_percentual_diario
FROM 
    comparativo
ORDER BY
    sigla_uf,
    data_vacinacao;
