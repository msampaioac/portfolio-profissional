/*=============================================================================
PROJETO: Perfil dos Estudantes Brasileiros (2019–2023)
ARQUIVO: 07_validacoes_modelagem.sql

SUBSTITUA `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano` pela
tabela criada a partir de 03_indice_infraestrutura.sql.
==============================================================================*/

-- 1. Uma linha por município e ano.
SELECT
  ano,
  id_municipio,
  COUNT(*) AS quantidade_linhas
FROM `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano`
GROUP BY ano, id_municipio
HAVING quantidade_linhas > 1;

-- 2. Índice e percentuais dentro do intervalo esperado.
SELECT COUNT(*) AS linhas_invalidas
FROM `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano`
WHERE indice_infraestrutura < 0
   OR indice_infraestrutura > 100
   OR perc_internet < 0
   OR perc_internet > 100
   OR perc_com_deficiencia < 0
   OR perc_com_deficiencia > 100;

-- 3. Cobertura mínima para o índice.
SELECT
  COUNTIF(qtd_indicadores_disponiveis < 6) AS linhas_abaixo_minimo,
  COUNTIF(indice_infraestrutura IS NULL) AS linhas_sem_indice,
  COUNT(*) AS total_linhas
FROM `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano`;

-- 4. Verificar cobertura anual e municípios observados.
SELECT
  ano,
  COUNT(DISTINCT id_municipio) AS municipios,
  SUM(qtd_estudantes) AS qtd_estudantes
FROM `seu_projeto.seu_dataset.indice_infraestrutura_municipio_ano`
GROUP BY ano
ORDER BY ano;
