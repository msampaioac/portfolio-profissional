# Abastecimento e logística — simulação didática COVID-19

> **Case inteiramente fictício.** NorteVia Distribuição é uma distribuidora B2B imaginária, sediada em Rio Branco-AC. Este projeto contém somente premissas didáticas selecionadas para exercício: não contém dados operacionais reais, não descreve uma implantação real e não demonstra resultados obtidos por uma empresa.

## Objetivo e desenho

Demonstrar como explicitar contratos de indicadores de abastecimento, serviço, custo e recebíveis em uma simulação com janela de observação de oito semanas (56 dias) e **coorte fixa de 100 pedidos planejados**. O cutoff permanece no dia 56; documentos podem maturar por até 5 dias úteis, com fechamento previsto até o dia 63. A comparação é entre dois ramos hipotéticos paralelos — **“sem pacote coordenado”** e **“com pacote hipotético”** — e não uma comparação pré/pós.

Todos os valores foram escolhidos para o exercício, não são evidência. A aritmética da diferença entre ramos **não é estimativa de impacto, efeito causal, previsão nem ROI**. Não se deve concluir que qualquer pacote causaria tais resultados.

## Indicadores do exercício

| Indicador | Sem pacote coordenado | Com pacote hipotético | Base/denominador |
|---|---:|---:|---|
| OTIF (pedidos no prazo e completos) | 62/100 = 62,0% | 82/100 = 82,0% | 100 pedidos planejados fixos |
| Fill rate (unidades entregues ÷ pedidas) | 8.000/10.000 = 80,0% | 9.100/10.000 = 91,0% | 10.000 unidades pedidas |
| Disponibilidade de SKUs críticos | 250/400 = 62,5% | 340/400 = 85,0% | 10 SKUs × 40 dias úteis = 400 SKU-dias |
| Perda por avaria/validade | 35/1.000 = 3,5% | 20/1.000 = 2,0% | 1.000 caixas |
| Custo de transporte por pedido planejado | R$ 9.200/100 = R$ 92,00 | R$ 8.400/100 = R$ 84,00 | 100 pedidos planejados fixos |
| Contas a receber vencidas há >30 dias | R$ 220.000/R$ 1.000.000 = 22,0% | R$ 150.000/R$ 1.000.000 = 15,0% | Exposição fixa no cutoff |

Nas taxas, o delta é expresso em pontos percentuais (p.p.), não em variação percentual relativa. No custo, são reportados o delta absoluto por pedido planejado e a variação relativa frente ao ramo “sem pacote coordenado”. A disponibilidade considera 40 dias úteis hipotéticos dentro da janela de 56 dias corridos. O cutoff fica no dia 56; a consolidação documental pode maturar até o dia 63. Consulte o [contrato dos dados e métricas](docs/contrato-dados.md) para definições, maturidade e limites por indicador.

## Arquivos

- [`dados/covid19_config.json`](dados/covid19_config.json): premissas, nomes de ramos e contrato de cada métrica.
- [`dados/covid19_resultados.csv`](dados/covid19_resultados.csv): saída versionada, com 12 linhas (seis métricas × dois ramos), gerada pelo script.
- [`scripts/simular_covid19.py`](scripts/simular_covid19.py): valida premissas e recalcula os resultados usando apenas a biblioteca padrão do Python e `Decimal` com arredondamento `ROUND_HALF_UP`.
- [`tests/test_covid19.py`](tests/test_covid19.py): testes de contrato, resultados, semântica de deltas, validações e reprodutibilidade. São testes da implementação didática, **não testes de produção**.
- [Resultados e leitura da simulação](docs/simulacao-covid19-resultados.md).

## Como executar

A partir deste diretório (`abastecimento-logistica`):

```bash
python3 scripts/simular_covid19.py
python3 -m unittest discover -s tests -v
```

O primeiro comando regrava o CSV versionado com fim de linha LF. A configuração é validada antes da gravação; o script verifica denominadores fixos, proporções válidas e exatamente os dois ramos nomeados no contrato.

## Limites e conexões

O contexto é uma simulação inspirada em desafios gerais de cadeias de suprimentos durante a COVID-19, não uma reconstrução da NorteVia. A referência externa é contextual, não fonte dos números simulados.

- Estratégia relacionada: [simulação de resposta COVID-19](../planejamento-estrategico/docs/simulacao-resposta-covid19.md).
- Governança relacionada: [simulação de processos COVID-19](../governanca-indicadores/docs/simulacao-covid19-processos.md).

Os caminhos são referências de navegação para os projetos relacionados; este projeto não afirma que os conteúdos referenciados validem seus números. Nenhum dado real foi incluído nem inferência causal é autorizada.
