# COVID-19 Brasil Analytics

> **Pergunta central:** como vacinação, mortalidade e capacidade hospitalar variaram entre municípios, estados e períodos da pandemia?

![SQL](https://img.shields.io/badge/SQL-Analítico-blue) ![BigQuery](https://img.shields.io/badge/Google-BigQuery-4285F4) ![BI](https://img.shields.io/badge/Business-Intelligence-F2C811)

## Visão rápida

Este projeto integra dados públicos disponibilizados pela [Base dos Dados](https://basedosdados.org/) para estruturar análises territoriais e temporais de vacinação, óbitos, casos graves, população e infraestrutura hospitalar. O foco é demonstrar como perguntas de saúde pública podem ser transformadas em consultas analíticas reproduzíveis para consumo em BI.

**Entregas atuais:** cinco consultas analíticas organizadas por pergunta, modelo dimensional documentado, dicionário inicial de dados e documentação de reprodução.

## O que o projeto responde

- Qual foi a velocidade de vacinação por UF e ao longo do tempo?
- Qual a cobertura vacinal proporcional à população?
- Como comparar infraestrutura hospitalar e indicadores de mortalidade?
- Quais municípios apresentaram maior pressão hospitalar?
- Como a vacinação evoluiu por faixa etária?

## Principais técnicas

- CTEs para decompor o raciocínio analítico;
- funções de janela (`LAG`, `LEAD`, `RANK`, `DENSE_RANK`, `NTILE`);
- acumulados e médias móveis;
- `SAFE_DIVIDE` e `COALESCE` para métricas mais robustas;
- junção de fatos com população, municípios e dimensões territoriais;
- organização compatível com camada analítica e modelo dimensional.

## Fluxo da solução

```text
Base dos Dados → BigQuery → consultas por pergunta → camada analítica → BI
                                      ↓
                 vacinação · mortalidade · hospitais · território
```

## Estrutura

```text
README.md
docs/
├── metodologia.md
├── perguntas_negocio.md
├── conclusoes.md
└── reproducibilidade.md
modelagem/
├── dicionario_dados.md
└── modelo_dimensional.md
sql/
├── 01_velocidade_vacinacao.sql
├── 02_cobertura_vacinal.sql
├── 03_infraestrutura_vs_obitos.sql
├── 04_pressao_hospitalar.sql
├── 05_faixa_etaria.sql
├── 06_views.sql
└── 07_performance.sql
```

## Limitações atuais

As consultas entregues calculam indicadores, rankings e comparações; elas não estabelecem causalidade entre vacinação, infraestrutura e mortalidade. A análise de correlação estatística e a publicação de um dashboard interativo permanecem como próximas evoluções. Os arquivos `06_views.sql` e `07_performance.sql` são reservados para essa evolução e ainda não representam implementações completas.

## Próximos passos

1. Implementar views Gold com nomes e contratos de saída documentados;
2. adicionar testes de qualidade para chaves, duplicidades, período e denominadores;
3. publicar um preview visual ou link do dashboard;
4. incluir correlação estatística exploratória, sempre separando associação de causalidade.

## Autor

**Marcelo dos Santos Sampaio** · [LinkedIn](https://linkedin.com/in/msampaioac) · [GitHub](https://github.com/msampaioac)
