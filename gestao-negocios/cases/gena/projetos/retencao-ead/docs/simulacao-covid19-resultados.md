# COVID-19: espelho de resultados simulados — Retenção EAD

> **Simulação retrospectiva, não resultado observado.** Os valores abaixo são premissas fictícias criadas para demonstrar como uma decisão de continuidade poderia ser acompanhada. Não são dados da GENA real, não foram observados durante a pandemia e não provam impacto, causalidade, aprendizagem ou ROI. Esta entrega foi preparada com apoio de IA.

[README de Retenção EAD](../README.md) · [Configuração do cenário](../dados/covid19_config.json) · [CSV calculado](../dados/covid19_espelho_resultados.csv) · [Gerador](../scripts/simular_espelho_covid19.py) · [Testes](../tests/test_espelho_covid19.py) · [Resposta estratégica](../../planejamento-estrategico/docs/simulacao-resposta-covid19.md) · [Governança e mapa de processos](../../governanca-indicadores/docs/simulacao-covid19-processos.md)

## Desenho do cenário

O exercício padroniza uma coorte fictícia de **1.000 alunos EAD** e um horizonte de **oito semanas**. Compara dois ramos hipotéticos: (A) **sem pacote coordenado** e (B) **com pacote de continuidade multicanal**, suporte, capacitação e acompanhamento. Os dois ramos usam denominadores fixos por indicador para tornar as contas comparáveis.

Isso **não é uma medição longitudinal** da mesma pessoa antes e depois. É uma comparação didática de cenários hipotéticos; os numeradores foram escolhidos para exercitar fórmulas e gates. A simulação não usa microdados da base EAD 2025 e não altera seus parâmetros, seu gerador ou seu resultado de 27,5% anual.

A janela quantitativa de oito semanas (56 dias) é um **marco intermediário** dentro do plano operacional de 90 dias. O gate do dia 90 também revisa custo, acesso, recuperação acadêmica e caixa; não anualiza nem extrapola as taxas do espelho.

## Espelho de indicadores

| Indicador e regra nesta simulação | Ramo sem pacote coordenado (8 semanas) | Ramo com pacote hipotético (8 semanas) | Diferença entre ramos (não causal) |
|:---|---:|---:|---:|
| Aulas entregues ÷ 300 planejadas em 8 semanas | 174/300 = **58,00%** | 270/300 = **90,00%** | **+32,00 p.p.** |
| Alunos com atividade em pelo menos 4 das 8 semanas ÷ coorte de 1.000 | 620/1.000 = **62,00%** | 760/1.000 = **76,00%** | **+14,00 p.p.** |
| Necessidades de acesso resolvidas em até 10 dias úteis ÷ 200 necessidades identificadas | 40/200 = **20,00%** | 150/200 = **75,00%** | **+55,00 p.p.** |
| Solicitações de suporte resolvidas em até 48 horas ÷ 150 solicitações | 45/150 = **30,00%** | 120/150 = **80,00%** | **+50,00 p.p.** |
| Pedidos de negociação financeira respondidos em até 5 dias úteis ÷ 160 pedidos | 48/160 = **30,00%** | 128/160 = **80,00%** | **+50,00 p.p.** |
| Cancelamentos registrados na janela ÷ 1.000 matrículas iniciais | 120/1.000 = **12,00%** | 90/1.000 = **9,00%** | **−3,00 p.p.**; queda relativa simulada de **25,00%** |

O CSV é gerado pela configuração por meio de aritmética determinística. O teste automatizado confere os denominadores, as taxas e as diferenças. A execução do script prova apenas que o espelho reproduz as premissas declaradas.

## Como interpretar sem exagerar

- O ramo sem pacote representa a hipótese de operação durante o choque inicial; o ramo com pacote é uma alternativa hipotética. Nenhum dos dois foi observado.
- A diferença de cancelamentos de 12% para 9% corresponde a 3 pontos percentuais ou 25% relativamente ao ramo sem pacote. **Não é efeito causal estimado** e não deve ser descrita como evasão efetivamente evitada.
- “Negociação respondida” mede prazo de atendimento, não acordo aceito, dinheiro recebido, inadimplência reduzida ou sustentabilidade financeira.
- A janela simulada de oito semanas não é comparável ao churn anual da base EAD 2025. O indicador de 2025 usa outra população, outra janela e exclusões explícitas.
- Não há resultados simulados para NPS, aprendizagem, receita, margem ou ROI. Eles exigiriam premissas e métodos adicionais e não devem ser inferidos deste espelho.

A escolha de combinar canais digitais e não digitais e monitorar barreiras de acesso é coerente com as respostas multimodais reunidas pela OCDE e com o contexto de fechamentos educacionais registrado pela UNESCO [1] [2]. Essas fontes não validam os números sintéticos deste case.

## Reprodução

A partir da raiz do repositório, dentro da pasta do projeto:

```bash
cd gestao-negocios/cases/gena/projetos/retencao-ead
python3 scripts/simular_espelho_covid19.py
python3 -m unittest tests.test_espelho_covid19 -v
```

O script lê `dados/covid19_config.json` e grava `dados/covid19_espelho_resultados.csv`. Não altera `dados/config.json`, os CSV da referência 2025, o relatório de validação existente nem os números da série institucional 2021–2025.

## Referências

[1]: https://www.oecd.org/en/publications/how-learning-continued-during-the-covid-19-pandemic_bbeca162-en.html "How Learning Continued during the COVID-19 Pandemic"
[2]: https://www.unesco.org/en/articles/covid-19-educational-disruption-and-response "COVID-19 Educational Disruption and Response"
