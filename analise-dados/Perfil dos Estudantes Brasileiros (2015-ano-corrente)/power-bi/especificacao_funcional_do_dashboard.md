# 📊 Storytelling Analítico do Dashboard

# Painel Estratégico da Educação Brasileira (2015–ano corrente)

## Objetivo Geral

Este documento apresenta a especificação funcional do dashboard desenvolvido em Power BI a partir da base analítica construída em SQL no Google BigQuery utilizando dados públicos do INEP disponibilizados pela Base dos Dados.

O objetivo é orientar o desenvolvimento do painel, definindo as principais perguntas de negócio, indicadores estratégicos (KPIs), visualizações, interações e decisões que poderão ser apoiadas pela solução analítica.

O dashboard foi concebido para atender gestores públicos, pesquisadores, profissionais de Business Intelligence, analistas de dados e tomadores de decisão interessados na evolução da educação brasileira desde **2015 até o ano corrente**.

---

# 🎯 Objetivos Estratégicos

O painel foi desenvolvido para:

- Consolidar indicadores educacionais em uma visão única.
- Facilitar a exploração dos dados por diferentes níveis de ensino.
- Apoiar a formulação de políticas públicas.
- Identificar tendências educacionais ao longo do tempo.
- Evidenciar desigualdades regionais.
- Disponibilizar indicadores confiáveis para tomada de decisão baseada em dados.

---

# 📄 Página 1 — Visão Executiva

## Objetivo

Apresentar uma visão consolidada da educação brasileira, permitindo compreender rapidamente a evolução dos principais indicadores do período.

## Pergunta principal

> **Como evoluiu a educação brasileira desde 2015 até o ano corrente?**

## Perguntas respondidas

- Quantos estudantes existem no Brasil?
- Como evoluíram as matrículas ao longo do período?
- Como os estudantes estão distribuídos por nível de ensino?
- Qual a participação das redes pública e privada?
- Quais estados concentram o maior número de matrículas?
- Como evoluiu a infraestrutura escolar?
- Qual o percentual de estudantes com deficiência?

## KPIs

- Total de Estudantes
- Ensino Fundamental
- Ensino Médio
- Ensino Superior
- Crescimento do Período
- Participação da Rede Pública
- Participação da Rede Privada
- Estudantes com Deficiência

## Visualizações

- Linha — Evolução das Matrículas
- Colunas — Distribuição por Nível de Ensino
- Donut — Rede Pública × Privada
- Mapa do Brasil
- Ranking dos Estados
- Cartões de Infraestrutura

## Decisões apoiadas

- Identificação de tendências nacionais.
- Definição de prioridades estratégicas.
- Direcionamento das análises detalhadas.

---

# 📄 Página 2 — Perfil Demográfico

## Objetivo

Analisar as características demográficas dos estudantes brasileiros.

## Pergunta principal

> **Quem são os estudantes brasileiros?**

## Perguntas respondidas

- Como está distribuído o sexo?
- Qual a faixa etária predominante?
- Como está distribuída a raça/cor?
- Qual a nacionalidade predominante?
- Como esses perfis variam por nível de ensino?

## KPIs

- Homens
- Mulheres
- Idade Média
- Estudantes com Deficiência
- Nacionalidades

## Visualizações

- Barras — Sexo
- Pirâmide Etária
- Donut — Raça/Cor
- Colunas — Faixa Etária
- Mapa por Estado

## Decisões apoiadas

- Identificação dos perfis predominantes.
- Formulação de políticas de inclusão.
- Comparação entre regiões.

---

# 📄 Página 3 — Distribuição Geográfica

## Objetivo

Analisar a distribuição espacial das matrículas no território nacional.

## Pergunta principal

> **Onde estão concentrados os estudantes brasileiros?**

## Perguntas respondidas

- Quais regiões concentram mais estudantes?
- Quais estados possuem maior número de matrículas?
- Quais municípios apresentam maior participação?
- Como ocorreu a evolução regional ao longo dos anos?

## KPIs

- Total por Região
- Total por Estado
- Total por Município

## Visualizações

- Mapa Coroplético
- Ranking dos Estados
- Ranking dos Municípios
- Linha Temporal Regional

## Decisões apoiadas

- Planejamento regional.
- Distribuição de investimentos.
- Comparações geográficas.

---

# 📄 Página 4 — Infraestrutura Escolar

## Objetivo

Avaliar a qualidade da infraestrutura das escolas brasileiras.

## Pergunta principal

> **Como evoluiu a infraestrutura das escolas brasileiras?**

## Perguntas respondidas

- Qual o percentual de escolas com internet?
- Quantas possuem biblioteca?
- Quantas possuem laboratório?
- Como está a infraestrutura por estado?
- Houve evolução desde 2015 até o ano corrente?

## KPIs

- Internet
- Biblioteca
- Sala de Leitura
- Laboratório de Informática
- Laboratório de Ciências
- Quadra Esportiva
- Água Potável
- Energia Elétrica

## Visualizações

- Barras Horizontais
- Heatmap
- Radar
- Mapa Temático

## Decisões apoiadas

- Priorização de investimentos.
- Redução das desigualdades regionais.
- Planejamento da infraestrutura educacional.

---

# 📄 Página 5 — Inclusão e Acessibilidade

## Objetivo

Avaliar os indicadores relacionados à inclusão educacional.

## Pergunta principal

> **Como evoluíram os indicadores de inclusão desde 2015 até o ano corrente?**

## Perguntas respondidas

- Quantos estudantes possuem deficiência?
- Como evoluiu esse indicador?
- Como está distribuído o transporte escolar?
- Quais regiões apresentam maior inclusão?

## KPIs

- Estudantes com Deficiência
- Transporte Escolar
- Percentual de Inclusão

## Visualizações

- Linha Temporal
- Barras
- Indicadores Percentuais
- Mapa Temático

## Decisões apoiadas

- Avaliação das políticas de inclusão.
- Planejamento de ações governamentais.
- Monitoramento dos indicadores sociais.

---

# 📄 Página 6 — Ensino Superior

## Objetivo

Analisar os principais indicadores relacionados ao Ensino Superior.

## Pergunta principal

> **Como evoluiu o Ensino Superior brasileiro?**

## Perguntas respondidas

- Quais áreas concentram mais estudantes?
- Como está distribuído o ensino presencial e EAD?
- Como evoluiu o financiamento estudantil?
- Como está a reserva de vagas?
- Como evoluíram os programas de apoio estudantil?

## KPIs

- Matrículas
- Financiamento Estudantil
- Reserva de Vagas
- Apoio Social
- Mobilidade Acadêmica

## Visualizações

- Treemap
- Sunburst
- Barras
- Donut
- Linha Temporal

## Decisões apoiadas

- Planejamento da expansão universitária.
- Avaliação das políticas de acesso.
- Monitoramento do Ensino Superior.

---

# 📄 Página 7 — Comparativos

## Objetivo

Permitir comparações entre diferentes dimensões da educação brasileira.

## Pergunta principal

> **Como os indicadores se comportam entre regiões, estados, anos e redes de ensino?**

## Perguntas respondidas

- Estado × Estado
- Região × Região
- Ano × Ano
- Rede Pública × Rede Privada
- Ensino Fundamental × Médio × Superior

## KPIs

- Diferença Absoluta
- Diferença Percentual
- Crescimento Acumulado

## Visualizações

- Barras Agrupadas
- Linha Comparativa
- Matriz
- Dispersão

## Decisões apoiadas

- Benchmarking.
- Comparações estratégicas.
- Identificação de melhores práticas.

---

# 📄 Página 8 — Insights Estratégicos

## Objetivo

Destacar automaticamente os principais achados identificados durante a análise dos dados.

## Pergunta principal

> **Quais indicadores exigem maior atenção dos gestores?**

## Perguntas respondidas

- Quais estados apresentaram maior crescimento?
- Onde estão as maiores deficiências de infraestrutura?
- Quais regiões apresentam melhores indicadores?
- Quais tendências foram observadas ao longo do período?
- Quais indicadores merecem acompanhamento prioritário?

## KPIs

- Top 5 Crescimentos
- Top 5 Reduções
- Melhor Infraestrutura
- Maior Inclusão
- Maior Evolução das Matrículas

## Visualizações

- Rankings
- Cartões Inteligentes
- Heatmap
- Linha de Tendência

## Decisões apoiadas

- Definição de prioridades estratégicas.
- Formulação de políticas públicas.
- Comunicação executiva.
- Identificação de oportunidades de melhoria.

---

# 🔎 Filtros Globais

O dashboard deverá disponibilizar filtros para todas as páginas, permitindo análises dinâmicas por diferentes perspectivas.

## Filtros

- Ano
- Região
- Estado
- Município
- Rede de Ensino
- Etapa de Ensino
- Sexo
- Faixa Etária
- Raça/Cor
- Deficiência
- Modalidade de Ensino

---

# 🧭 Navegação

Fluxo recomendado de exploração do dashboard:

1. Visão Executiva
2. Perfil Demográfico
3. Distribuição Geográfica
4. Infraestrutura Escolar
5. Inclusão e Acessibilidade
6. Ensino Superior
7. Comparativos
8. Insights Estratégicos

---

# 🎯 Resultado Esperado

Ao final da navegação, o usuário deverá compreender:

- A evolução da educação brasileira desde **2015 até o ano corrente**.
- O perfil demográfico dos estudantes.
- A distribuição geográfica das matrículas.
- As diferenças entre redes pública e privada.
- A evolução da infraestrutura escolar.
- Os avanços em inclusão educacional.
- O comportamento do Ensino Superior.
- As principais tendências e oportunidades identificadas nos dados.

O dashboard foi concebido para oferecer uma experiência analítica intuitiva, permitindo que gestores públicos, pesquisadores e profissionais de dados transformem informações dispersas em conhecimento estratégico para apoiar decisões fundamentadas em evidências.
