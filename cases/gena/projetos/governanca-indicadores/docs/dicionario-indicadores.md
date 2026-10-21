# Contrato dos indicadores — versão 1.0 do estudo

[Projeto](../README.md) · [Fontes](inventario-fontes.md) · [Modelo lógico](modelo-logico.md) · [Reconciliação](../evidencias/reconciliacao.md)

**Referência:** cenário fictício de 2025, com posição final em 31/12/2025. Este contrato formaliza regras do estudo; não registra aprovação de uma empresa real.

## Cobertura da entrega

| Indicador | Situação | Evidência |
|:---|:---|:---|
| Churn anual EAD | Implementado no ciclo sintético | Coorte, exclusões e comparação de denominadores |
| Retenção anual EAD | Implementado no ciclo sintético | Mesmo denominador do churn e teste de complementaridade |
| Adimplência monetária EAD | Implementado no ciclo sintético | Conciliação de títulos e pagamentos |
| Inadimplência monetária EAD | Implementado no ciclo sintético | Saldo aberto sobre valor devido dos títulos vencidos |
| NPS EAD | Implementado no ciclo sintético | Classificação e respostas válidas da amostra |
| Conversão Médio → Graduação | **Especificação preliminar; sem cálculo** | Fonte de funil inexistente; nenhuma meta ou resultado inventado |

São cinco indicadores recalculados, não cinco medidas independentes: churn/retenção e adimplência/inadimplência são pares complementares sob as regras desta versão. O NPS usa uma amostra calibrada.

## 1. Churn anual da coorte de abertura

| Campo | Regra |
|:---|:---|
| Pergunta | Qual proporção das matrículas elegíveis da abertura foi cancelada durante 2025? |
| Fórmula | `100 × cancelados elegíveis ÷ matrículas elegíveis da abertura` |
| Fonte e nível de detalhe | `matriculas_ead.csv`; uma matrícula por aluno nesta versão |
| População | Abertura de 2.880; excluir separadamente 40 conclusões e 40 transferências externas; 2.800 elegíveis |
| Numerador e resultado | 770 cancelados; referência calibrada de 27,5% |
| Entradas | Os 1.090 ingressantes de março a novembro não entram no denominador da abertura |
| Exceções | Status desconhecido ou elegibilidade incompatível bloqueia o cálculo; não inferir cancelamento por baixo acesso |
| Responsabilidade proposta | Negócio valida o significado; Coordenação formaliza o contrato; mudança de regra segue a RACI |

**Escolha metodológica:** medir abandono entre os elegíveis, sem classificar conclusão regular ou transferência como evasão. As exclusões são retrospectivas e precisam aparecer na reconciliação. Uma taxa bruta de saídas da abertura seria outra métrica; não deve ser renomeada como churn sem explicar a diferença.

## 2. Retenção anual da mesma coorte

| Campo | Regra |
|:---|:---|
| Fórmula | `100 × elegíveis ativos no fechamento ÷ elegíveis da abertura` |
| População e janela | Iguais às do churn; exclui ingressantes, conclusões e transferências |
| Numerador e resultado | 2.030 retidos; referência de 72,5% |
| Controle | Churn + retenção = 100% apenas se cada elegível terminar ativo ou cancelado |
| Limite | Não usar o fechamento de 3.120 ativos como total de retidos da abertura |

## 3. Adimplência monetária

| Campo | Regra |
|:---|:---|
| Fórmula | `100 × valor pago alocado aos títulos maturados ÷ valor devido desses títulos` |
| Fonte e nível de detalhe | `financeiro_ead.csv`; título × posição em 31/12/2025 |
| Elegibilidade | Competências de 2025 com vencimento até 31/12/2025; sem títulos após o mês da saída |
| Controle financeiro | Valores inteiros em centavos; devido = pago + saldo, sem saldo ou pagamento negativo |
| Resultado de referência | 86,5%, complemento monetário da inadimplência desta posição |
| Limite | Valor devido e pago não são, por si só, receita contábil nem margem |

## 4. Inadimplência monetária na posição final

| Campo | Regra |
|:---|:---|
| Fórmula | `100 × saldo aberto dos títulos maturados ÷ valor devido desses títulos` |
| População e posição | Iguais às da adimplência |
| Resultado de referência | 13,5%, calibrado na geração com arredondamento ao centavo |
| Controle | Excluir títulos futuros; conferir pagamentos parciais; usar soma monetária, não quantidade de títulos |
| Limite | Não é média de taxas mensais, proporção de alunos devedores ou perda financeira definitiva |

A versão sintética não possui bolsas, descontos, acordos, multas, substituição de títulos ou baixas contábeis. Em uma implantação, essas regras exigiriam contrato financeiro próprio; não foram testadas por inexistirem nos arquivos.

## 5. NPS da pesquisa sintética

| Campo | Regra |
|:---|:---|
| Fórmula | `100 × (promotores − detratores) ÷ respostas válidas` |
| Fonte e nível de detalhe | `pesquisa_nps_ead.csv`; uma resposta por matrícula selecionada |
| Classificação | 9–10: promotor; 7–8: passivo; 0–6: detrator |
| Amostra | 200 respostas; 118 promotores, 42 passivos e 40 detratores |
| Resultado e unidade | 39 pontos; escala de −100 a 100, não percentual de satisfação |
| Limite | Composição calibrada, sem comprovação de representatividade ou efeito de intervenção |

## 6. Conversão Médio → Graduação — preliminar

Para evitar dois denominadores sob um mesmo nome, o escopo proposto é a continuidade de concluintes do Ensino Médio da GENA para sua graduação. O funil de leads comerciais seria um indicador separado.

| Campo | Especificação a validar antes de implementar |
|:---|:---|
| Numerador | Pessoas da coorte elegível com matrícula de graduação confirmada na janela aprovada |
| Denominador | Pessoas concluintes elegíveis daquela mesma coorte de Ensino Médio |
| Janela | Início, encerramento e evento de confirmação a definir antes do cálculo |
| Chave | Identificador de pessoa que permita ligar conclusão e matrícula sem duplicação |
| Fontes necessárias | Base de concluintes, elegibilidade e eventos de matrícula/confirmação |
| Situação | Não existem dados desse funil na base EAD; sem cálculo, teste de conversão, baseline ou meta |

Essa delimitação é uma proposta metodológica, não uma homologação. O ciclo entregue de governança tem como aceite técnico **cinco indicadores**, enquanto conversão segue fora do cálculo até haver fonte e contrato completo.

## Regras comuns

Um denominador nulo gera falha ou resultado não calculável, nunca zero automático. Todo resultado deve indicar população, janela, unidade, versão e fonte. A implementação usa a [configuração oficial](../../retencao-ead/dados/config.json) e preserva os arquivos originais.

A referência de 2025 não substitui uma linha de base operacional atualizada para o ciclo estratégico de 2027–2029.
