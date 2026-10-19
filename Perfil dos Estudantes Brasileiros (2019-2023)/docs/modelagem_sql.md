# Camada SQL para modelagem

A consulta principal continua sendo a base consolidada do projeto. Os scripts 02 a 07 criam saídas específicas para análise territorial, clusterização, classificação e previsão, sem misturar as necessidades do Power BI com as necessidades dos modelos.

## Ordem de execução

1. Execute `sql/02_base_infraestrutura_municipio_ano.sql` e salve o resultado como `base_infraestrutura_municipio_ano`.
2. Execute `sql/03_indice_infraestrutura.sql`, substituindo `seu_projeto.seu_dataset.base_infraestrutura_municipio_ano`, e salve o resultado como `indice_infraestrutura_municipio_ano`.
3. Execute `sql/07_validacoes_modelagem.sql` e investigue qualquer resultado inesperado.
4. Use `sql/04_base_modelagem_cluster.sql` como fonte do notebook de clusterização.
5. Use `sql/05_base_modelagem_classificacao.sql` como fonte do notebook de classificação.
6. Use `sql/06_serie_temporal_previsao.sql` como fonte do notebook de previsão.

## Decisões metodológicas

- A unidade para clusterização e classificação é município-ano da Educação Básica.
- O índice varia de 0 a 100 e usa a média dos indicadores disponíveis.
- O índice só é calculado quando pelo menos seis dos dez indicadores de infraestrutura estão disponíveis.
- Nulos significam indicador não disponível ou não aplicável; não são automaticamente tratados como infraestrutura ausente.
- A classificação usa as variáveis do ano `t` para prever o quartil do índice no ano `t+1`.
- A série de previsão por UF usa médias ponderadas pela quantidade de registros/matrículas. Como o período é anual e começa em 2015, o número de observações depende da atualização disponível na fonte.
- A escolha de normalização, algoritmo, número de clusters, métricas e hiperparâmetros será feita no Python/Colab.

## Tabelas esperadas

| Tabela | Granularidade | Uso |
|---|---|---|
| `base_infraestrutura_municipio_ano` | município-ano | indicadores brutos e percentuais |
| `indice_infraestrutura_municipio_ano` | município-ano | índice e qualidade da cobertura |
| `base_modelagem_cluster` | município-ano | entrada do K-Means ou método alternativo |
| `base_modelagem_classificacao` | município-ano com alvo futuro | classificação supervisionada |
| `serie_temporal_previsao` | UF-ano | baselines e previsão temporal |

Os nomes `seu_projeto.seu_dataset` são placeholders. Substitua-os pelo projeto e dataset do BigQuery antes da execução.
