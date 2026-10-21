# Contrato de dados — simulação didática COVID-19

> **Natureza do case:** NorteVia Distribuição é uma empresa fictícia (distribuidora B2B imaginária de Rio Branco-AC). O arquivo de configuração contém somente premissas selecionadas para exercício, não dados operacionais reais. A janela de 8 semanas/56 dias e os dois ramos são cenários hipotéticos paralelos, não períodos pré/pós nem grupos observados.

## População, período e comparação

- **Coorte:** 100 pedidos planejados, denominador fixo nos dois ramos. Métricas de unidades, SKUs, caixas, dinheiro e atraso têm denominadores próprios descritos abaixo.
- **Janela:** oito semanas, 56 dias corridos; cutoff fixo no dia 56. A disponibilidade usa 40 dias úteis hipotéticos (10 SKUs × 40 = 400 SKU-dias), sem calendário real. Provas e conciliações podem maturar até 5 dias úteis depois, com fechamento previsto até o dia 63; esse prazo não estende a janela.
- **Ramos:** “sem pacote coordenado” e “com pacote hipotético”. São duas linhas de cenário, sem pacote factual implementado.
- **Comparação:** diferença aritmética “com pacote hipotético” menos “sem pacote coordenado”. Não é avaliação causal, estimativa de impacto, previsão ou ROI.
- **Origem dos valores:** selecionados para exercício; não são evidência e não foram observados na empresa fictícia.

## Dicionário de métricas

| ID / indicador | Numerador | Denominador fixo | Fórmula e unidade | Maturidade / cutoff |
|---|---|---|---|---|
| `otif` — OTIF, pedidos no prazo e completos | Pedidos simultaneamente no prazo e completos: 62 / 82 pedidos | 100 pedidos planejados | Numerador ÷ denominador × 100; % | Cutoff no dia 56; provas e status podem maturar por até 5 dias úteis, com fechamento até o dia 63. |
| `fill_rate` — fill rate | Unidades entregues: 8.000 / 9.100 unidades | 10.000 unidades pedidas | Numerador ÷ denominador × 100; % | Cutoff no dia 56; as unidades entregues podem ser conciliadas por até 5 dias úteis, com fechamento até o dia 63. |
| `disponibilidade_skus` — disponibilidade de SKUs críticos | SKU-dias disponíveis: 250 / 340 | 10 SKUs × 40 dias úteis = 400 SKU-dias | Numerador ÷ denominador × 100; % | Cutoff no dia 56, após 40 dias úteis hipotéticos; não há snapshots posteriores ao período de observação. |
| `perda_avaria_validade` — perda por avaria/validade | Caixas perdidas: 35 / 20 caixas | 1.000 caixas | Numerador ÷ denominador × 100; % | Cutoff no dia 56; ocorrências documentadas podem maturar por até 5 dias úteis, com fechamento até o dia 63. |
| `custo_transporte_por_pedido` — custo alocado por pedido planejado | Custo de transporte alocado: R$ 9.200 / R$ 8.400 | 100 pedidos planejados | Numerador ÷ denominador; R$/pedido planejado | Cutoff no dia 56; conciliação documental pode maturar por até 5 dias úteis, com fechamento até o dia 63. |
| `contas_vencidas_30d` — contas a receber vencidas há mais de 30 dias | Saldo vencido no cutoff: R$ 220.000 / R$ 150.000 | Exposição a receber fixa: R$ 1.000.000 | Numerador ÷ denominador × 100; % | Cutoff financeiro fixado no dia 56; considera atraso estritamente superior a 30 dias, sem incluir movimentos posteriores. |

## Regras de cálculo e comparação

1. O script usa `Decimal` e `ROUND_HALF_UP`, sem dependências externas. Percentuais são arredondados a uma casa decimal; custo por pedido, a duas. Para custo, a variação relativa é arredondada a duas casas.
2. Para proporções, o CSV registra `comparison_delta` em **p.p.**: percentual do ramo com pacote hipotético menos percentual do ramo sem pacote coordenado. Logo, 82,0% − 62,0% = +20,0 p.p.; não significa +20% relativo.
3. Para custo, delta absoluto = R$ 84,00 − R$ 92,00 = **−R$ 8,00 por pedido planejado**. Variação relativa = (84 − 92) ÷ 92 × 100 = **−8,70%**, cuja base é o primeiro ramo. Não é ROI.
4. Os deltas são repetidos nas duas linhas do par para facilitar leitura tabular; não são resultados observados. Valores negativos nas proporções de perdas ou atraso indicam apenas menor razão no cenário com pacote hipotético, não benefício causal demonstrado.
5. A coluna `schema_version` é `1.0`. CSV tem cabeçalho definido no script, ordem estável de métricas (a ordem do JSON), dois ramos por indicador, vírgula como separador e LF como terminador.

## Limites de interpretação e uso

- Não existem IDs de pedidos, eventos de entrega, pedidos por SKU, ocorrências de perda, lançamentos de frete, títulos a receber ou registros transacionais neste exercício.
- OTIF não tem regras operacionais observadas para prazo, completude, cancelamento ou entrega parcial. Fill rate não mede pontualidade e não substitui OTIF.
- A disponibilidade dá peso igual a cada SKU-dia, sem ponderar demanda ou criticidade; os 10 SKUs são hipotéticos.
- A perda não separa avaria de validade; a base de 1.000 caixas é uma premissa, não volume de operação.
- Não há regra real de alocação nem composição de custos; os dois valores são escolhidos para exercício.
- A carteira a receber é fictícia: não há vencimentos, recebimentos, aging transacional ou regra de exposição. O denominador de R$ 1.000.000 é constante.
- Não há linha de base factual, grupo de controle, desenho experimental ou contrafactual. A comparação não é pré/pós causal nem estimativa de efeito.
- Os testes verificam consistência do código e do conjunto de premissas, não produção ou eficácia de intervenção.

## Configuração e reprodutibilidade

O contrato executável está em [`../dados/covid19_config.json`](../dados/covid19_config.json), e a saída calculada, em [`../dados/covid19_resultados.csv`](../dados/covid19_resultados.csv). A implementação é [`../scripts/simular_covid19.py`](../scripts/simular_covid19.py); testes: [`../tests/test_covid19.py`](../tests/test_covid19.py). Execute a partir do diretório do projeto:

```bash
python3 scripts/simular_covid19.py
python3 -m unittest discover -s tests -v
```
