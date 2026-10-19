/*=============================================================================
PROJETO: Perfil dos Estudantes Brasileiros (2019–2023)
ARQUIVO: 04_base_modelagem_cluster.sql

OBJETIVO
-------------------------------------------------------------------------------
Preparar uma linha por município e ano para consumo no Colab/K-Means.
A normalização das variáveis, a escolha de k e a avaliação por silhouette score
serão realizadas no Python.
==============================================================================*/

SELECT
  ano,
  id_municipio,
  nome_municipio,
  sigla_uf,
  regiao,
  qtd_estudantes,
  qtd_escolas,
  indice_infraestrutura,
  qtd_indicadores_disponiveis,
  perc_agua_potavel,
  perc_energia_rede_publica,
  perc_esgoto_rede_publica,
  perc_internet,
  perc_internet_alunos,
  perc_biblioteca,
  perc_biblioteca_sala_leitura,
  perc_lab_informatica,
  perc_lab_ciencias,
  perc_quadra,
  perc_com_deficiencia,
  perc_usa_transporte_publico,
  LN(1 + qtd_estudantes) AS log_qtd_estudantes,
  LN(1 + qtd_escolas) AS log_qtd_escolas

FROM `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano`

WHERE indice_infraestrutura IS NOT NULL
  AND qtd_indicadores_disponiveis >= 6
  AND qtd_estudantes > 0;
