# Resultados da simulação didática COVID-19

> **Aviso central:** NorteVia Distribuição é fictícia. Esta simulação usa somente valores selecionados para exercício, sem dados operacionais reais. “Sem pacote coordenado” e “com pacote hipotético” são ramos hipotéticos paralelos — **não pré/pós causal**. As diferenças abaixo são aritmética de cenário, não estimativas de impacto, efeitos atribuíveis, previsões ou ROI.

## Premissas e leitura

A janela de observação dura oito semanas (56 dias) e mantém uma coorte fixa de 100 pedidos planejados. O cutoff permanece no dia 56; provas e conciliações podem maturar por até 5 dias úteis, com fechamento previsto até o dia 63. Os denominadores das outras métricas são próprios (unidades, SKU-dias, caixas ou exposição financeira). Os valores foram escolhidos para este exercício; não constituem evidência sobre a NorteVia nem resultados observados.

| Métrica | Sem pacote coordenado | Com pacote hipotético | Diferença aritmética do ramo com menos o ramo sem |
|---|---:|---:|---:|
| OTIF — pedidos no prazo e completos | 62/100 = **62,0%** | 82/100 = **82,0%** | **+20,0 p.p.** |
| Fill rate — unidades entregues ÷ 10.000 pedidas | 8.000/10.000 = **80,0%** | 9.100/10.000 = **91,0%** | **+11,0 p.p.** |
| Disponibilidade — 10 SKUs críticos × 40 dias úteis (400 SKU-dias) | 250/400 = **62,5%** | 340/400 = **85,0%** | **+22,5 p.p.** |
| Perda por avaria/validade — caixas | 35/1.000 = **3,5%** | 20/1.000 = **2,0%** | **−1,5 p.p.** |
| Custo de transporte alocado ÷ 100 pedidos planejados | R$ 9.200/100 = **R$ 92,00/pedido** | R$ 8.400/100 = **R$ 84,00/pedido** | **−R$ 8,00/pedido** (−8,70% relativo ao ramo sem) |
| Contas a receber >30 dias no cutoff ÷ exposição fixa de R$ 1.000.000 | R$ 220.000/R$ 1.000.000 = **22,0%** | R$ 150.000/R$ 1.000.000 = **15,0%** | **−7,0 p.p.** |

## Como interpretar os deltas

- Em cinco indicadores de proporção, a comparação usa **pontos percentuais**: por exemplo, 82,0% − 62,0% = 20,0 p.p. Isso não é uma variação de 20% relativa.
- Em custo, o delta absoluto é R$ 84,00 − R$ 92,00 = **−R$ 8,00 por pedido planejado**. A variação relativa usa R$ 92,00 como base: (84 − 92) ÷ 92 = **−8,70%**.
- Nenhum dos deltas é estimativa de impacto. Sem observações, tratamento aplicado, grupo de comparação e desenho de identificação, a diferença só descreve as premissas aritméticas dos dois ramos.
- A disponibilidade combina 10 SKUs e 40 dias úteis hipotéticos dentro do cutoff fixo de 56 dias. O saldo a receber usa esse cutoff, estritamente para títulos vencidos há mais de 30 dias. A maturação até o dia 63 não acrescenta eventos ou saldos posteriores ao período observado.

## Relevância contextual e limites

A COVID-19 trouxe desafios a cadeias de suprimentos alimentares e respostas de política, como discute a publicação da OCDE citada em [1]. Essa referência é usada apenas para contexto geral: **não fornece os números deste case**, não valida as premissas e não permite inferir desempenho para NorteVia. A empresa é fictícia; não se simulam transações reais de uma distribuidora específica.

O contrato completo, incluindo maturidade e limitações por métrica, consta em [`contrato-dados.md`](contrato-dados.md); as entradas estão em [`../dados/covid19_config.json`](../dados/covid19_config.json), a saída em [`../dados/covid19_resultados.csv`](../dados/covid19_resultados.csv) e o recálculo em [`../scripts/simular_covid19.py`](../scripts/simular_covid19.py). Os testes verificam premissas e saída didática, **não uma aplicação em produção**.

Projetos relacionados: [estratégia — resposta COVID-19](../../planejamento-estrategico/docs/simulacao-resposta-covid19.md) e [governança — processos da simulação](../../governanca-indicadores/docs/simulacao-covid19-processos.md). São links de contexto; não alteram os limites de evidência deste exercício.

## Referência

[1]: https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/06/food-supply-chains-and-covid-19-impacts-and-policy-lessons_62c97266/71b57aea-en.pdf "Food Supply Chains and COVID-19: Impacts and Policy Lessons"
