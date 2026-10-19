# Entregas da camada SQL

Esta pasta contém a evolução do Projeto 01 — **Perfil dos Estudantes Brasileiros**. A camada SQL foi organizada para separar a consulta consolidada do preparo específico para análise de infraestrutura, clusterização, classificação e previsão.

## Visão geral do fluxo

```text
Fontes INEP / Base dos Dados
            ↓
consulta_principal.sql
            ↓
02_base_infraestrutura_municipio_ano.sql
            ↓
03_indice_infraestrutura.sql
            ↓
 ┌────────────────────┬────────────────────────┬─────────────────────────┐
 │ clusterização       │ classificação          │ previsão                │
 │ 04_base_modelagem   │ 05_base_modelagem     │ 06_serie_temporal       │
 │ _cluster.sql        │ _classificacao.sql    │ _previsao.sql            │
 └────────────────────┴────────────────────────┴─────────────────────────┘
            ↓
07_validacoes_modelagem.sql
            ↓
Python / Colab / Power BI
```

## 1. `consulta_principal.sql`

### Objetivo

Construir a base analítica consolidada do projeto, integrando dados da Educação Básica, do Ensino Superior e do diretório de municípios.

### Fontes utilizadas

- Censo Escolar — matrícula;
- Censo Escolar — escola;
- Censo da Educação Superior — curso;
- Censo da Educação Superior — instituição de ensino;
- diretório de municípios.

### O que entrega

A consulta retorna indicadores e dimensões para análise por:

- ano;
- fonte;
- nível de ensino;
- estado, região e município;
- rede de ensino;
- sexo;
- raça/cor;
- faixa etária;
- nacionalidade;
- localização da escola;
- modalidade e grau acadêmico;
- organização institucional;
- área de conhecimento.

Também calcula métricas de matrículas, inclusão, transporte, infraestrutura escolar, financiamento, reserva de vagas, apoio social, atividades extracurriculares e mobilidade acadêmica.

### Granularidade

A saída é agregada por dimensões analíticas. Ela não representa uma linha individual por estudante. A coluna `qtd_estudantes` representa a soma dos registros ou matrículas disponíveis na fonte para cada agrupamento.

### Uso recomendado

- visão geral do projeto;
- Power BI;
- análises exploratórias;
- validação de totais por nível de ensino;
- criação de indicadores gerais.

---

## 2. `02_base_infraestrutura_municipio_ano.sql`

### Objetivo

Criar uma base territorial específica para análise da infraestrutura da Educação Básica.

### Unidade de análise

Uma linha por:

```text
município + ano
```

### O que entrega

A consulta calcula, para cada município e ano:

- quantidade de estudantes ou registros de matrícula;
- quantidade de escolas;
- percentual com água potável;
- percentual com energia da rede pública;
- percentual com esgoto da rede pública;
- percentual com internet;
- percentual com internet disponível para alunos;
- percentual com biblioteca;
- percentual com biblioteca ou sala de leitura;
- percentual com laboratório de informática;
- percentual com laboratório de ciências;
- percentual com quadra esportiva;
- percentual de estudantes com deficiência;
- percentual que utiliza transporte escolar público.

### Uso recomendado

Esta é a base principal para:

- mapas municipais;
- comparação regional;
- cálculo do índice de infraestrutura;
- clusterização;
- análise de desigualdades.

---

## 3. `03_indice_infraestrutura.sql`

### Objetivo

Calcular um índice sintético de infraestrutura escolar para cada município e ano.

### Regra do índice

O índice é calculado como a média dos indicadores de infraestrutura disponíveis, em uma escala de 0 a 100.

São considerados dez indicadores:

- água potável;
- energia da rede pública;
- esgoto da rede pública;
- internet;
- internet disponível para alunos;
- biblioteca;
- biblioteca ou sala de leitura;
- laboratório de informática;
- laboratório de ciências;
- quadra esportiva.

### Tratamento de nulos

Valores nulos são tratados como indicadores não disponíveis ou não aplicáveis. Eles não são automaticamente interpretados como infraestrutura ausente.

O índice somente é calculado quando existem pelo menos seis indicadores disponíveis para o município-ano.

### Classificação da cobertura

O script também cria a coluna `qualidade_cobertura_indicadores`:

- `ALTA`: pelo menos oito indicadores disponíveis;
- `MEDIA`: seis ou sete indicadores disponíveis;
- `INSUFICIENTE`: menos de seis indicadores disponíveis.

### Uso recomendado

- ranking de infraestrutura;
- mapas de vulnerabilidade;
- criação de perfis municipais;
- variável de entrada para clusterização;
- variável-alvo para classificação e previsão.

### Observação

Antes de executar o script, substitua:

```sql
seu_projeto.seu_dataset.base_infraestrutura_municipio_ano
```

pelo nome real da tabela criada no BigQuery.

---

## 4. `04_base_modelagem_cluster.sql`

### Objetivo

Preparar uma base de características para clusterização no Python/Colab.

### O que entrega

A saída mantém uma linha por município e ano e seleciona:

- índice de infraestrutura;
- indicadores individuais de infraestrutura;
- inclusão e transporte;
- quantidade de estudantes;
- quantidade de escolas;
- quantidade de indicadores disponíveis;
- região e UF;
- transformações logarítmicas de estudantes e escolas.

### O que não é feito neste script

O SQL não executa o algoritmo de clusterização. As etapas abaixo serão realizadas no Colab:

- tratamento final de outliers;
- imputação ou exclusão de nulos;
- padronização das variáveis;
- escolha do número de clusters;
- treinamento do K-Means ou outro algoritmo;
- avaliação por silhouette score;
- interpretação dos perfis.

### Uso recomendado

A saída deve ser exportada para o Colab para identificar grupos de municípios com padrões semelhantes de infraestrutura.

---

## 5. `05_base_modelagem_classificacao.sql`

### Objetivo

Criar uma base para classificação supervisionada sem usar o próprio índice futuro como variável explicativa.

### Estratégia temporal

As variáveis do município no ano `t` são usadas para prever o nível de infraestrutura no ano `t+1`.

Exemplo:

```text
Características de 2019 → classe de infraestrutura de 2020
Características de 2020 → classe de infraestrutura de 2021
```

O último ano da base não possui rótulo futuro e não entra nessa preparação.

### Rótulo criado

O índice do ano seguinte é dividido em quatro grupos relativos ao próprio ano:

- `CRITICA`: primeiro quartil;
- `BAIXA`: segundo quartil;
- `MEDIA`: terceiro quartil;
- `CONSOLIDADA`: quarto quartil.

### Uso recomendado

A saída pode ser utilizada para treinar e comparar modelos como:

- Regressão Logística;
- Árvore de Decisão;
- Random Forest;
- Gradient Boosting em uma etapa posterior.

### Avaliações esperadas no Colab

- matriz de confusão;
- precision;
- recall;
- F1-score;
- accuracy;
- importância das variáveis;
- análise específica da classe `CRITICA`.

---

## 6. `06_serie_temporal_previsao.sql`

### Objetivo

Criar uma série temporal anual por Unidade da Federação para uso em previsão.

### Unidade de análise

Uma linha por:

```text
UF + ano
```

### O que entrega

A consulta calcula:

- quantidade de estudantes;
- quantidade de escolas;
- índice de infraestrutura ponderado pela quantidade de estudantes;
- percentual de internet ponderado;
- percentual de internet para alunos ponderado;
- percentual de estudantes com deficiência ponderado.

### Por que usar média ponderada

Municípios com quantidades muito diferentes de estudantes não devem ter o mesmo peso na composição do indicador estadual. A ponderação reduz a distorção causada pela média simples dos municípios.

### Limitação atual

O período de 2019 a 2023 possui apenas cinco observações anuais por UF. Portanto, a primeira utilização deve comparar baselines e servir como exercício metodológico. Modelos complexos exigem uma série mais longa ou uma frequência maior.

### Modelos que serão testados no Colab

- último valor observado;
- média móvel;
- tendência linear;
- Exponential Smoothing;
- ARIMA ou SARIMA, se houver observações suficientes.

---

## 7. `07_validacoes_modelagem.sql`

### Objetivo

Verificar se a tabela do índice está pronta para alimentar modelos e análises posteriores.

### Validações incluídas

1. **Granularidade:** verifica se há mais de uma linha por município e ano.
2. **Intervalos:** verifica índices e percentuais menores que 0 ou maiores que 100.
3. **Cobertura:** mostra linhas sem índice e registros abaixo do mínimo de indicadores disponíveis.
4. **Cobertura temporal:** apresenta municípios e quantidade de estudantes por ano.

### Resultado esperado

A consulta retorna apenas os problemas encontrados. Uma consulta sem linhas nos testes de duplicidade e intervalo indica que essas validações básicas foram atendidas.

As validações não substituem a conferência dos totais contra as publicações oficiais do INEP.

---

## Ordem de execução no BigQuery

1. Executar `consulta_principal.sql` para a visão consolidada.
2. Executar `02_base_infraestrutura_municipio_ano.sql`.
3. Salvar o resultado como `base_infraestrutura_municipio_ano`.
4. Executar `03_indice_infraestrutura.sql`.
5. Salvar o resultado como `indice_infraestrutura_municipio_ano`.
6. Executar `07_validacoes_modelagem.sql`.
7. Executar as consultas 04, 05 e 06 para gerar as bases de consumo do Colab.
8. Documentar o projeto, dataset, data de extração e quantidade de linhas geradas.

## Status da entrega

A camada SQL de preparação foi entregue e publicada. Ainda não estão entregues nesta etapa:

- notebooks de clusterização;
- notebooks de classificação;
- notebooks de previsão;
- avaliação dos modelos;
- interpretação estatística dos resultados;
- atualização do dashboard com os novos indicadores.

Essas etapas serão desenvolvidas após a execução das consultas no BigQuery e a validação das tabelas geradas.
