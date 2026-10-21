# Visão executiva — NorteVia Distribuição

> Case integralmente fictício. A empresa, o mercado, os dados, os papéis e as decisões não descrevem uma operação real. As seis métricas COVID-19 são premissas didáticas selecionadas e não resultados medidos.

## Decisão central

O problema da NorteVia é apresentado como uma escolha entre continuidade do abastecimento e disciplina operacional/financeira. Uma distribuidora regional não controla a produção nem todas as rotas, mas pode explicitar prioridades, confirmar disponibilidade por SKU e validade, oferecer substituições com consentimento, agrupar entregas e acompanhar caixa e recebíveis.

A recomendação é preparar uma resposta limitada e reversível, primeiro validando dados, qualidade dos alimentos, capacidade e critérios de atendimento. Em seguida, testar regras focadas em poucos itens/rotas e revisá-las semanalmente. O plano de 90 dias prevê gates; a simulação retrospectiva da COVID-19 serve para ilustrar decisões, não para afirmar que foram executadas.

## Três projetos

| Frente | Entrega disponível | Evidência ou próximo estágio |
|:---|:---|:---|
| Planejamento estratégico | Diagnóstico por hipóteses, prioridades, trade-offs, objetivos condicionais, sequência de 90 dias, RACI e riscos | Validar linhas de base, critérios de segurança, capacidade, caixa e alçadas antes de qualquer uso operacional |
| Abastecimento e logística | Configuração sintética, gerador Python, espelho CSV com seis indicadores e testes reprodutíveis | Dados transacionais não existem no case; uma aplicação real exigiria contratos de dados, fontes, reconciliação e governança aprovados |
| Governança de indicadores | Mapas hipotéticos de processo antes/depois, fórmulas, denominadores, maturidade, responsáveis e trilha de auditoria | Homologar cada definição com áreas responsáveis; testar registro e evidências apenas em ambiente autorizado |

## Resultado ilustrativo — não observado

No ramo “sem pacote coordenado”, o espelho didático calcula OTIF de 62%, fill rate de 80%, disponibilidade de SKUs críticos de 62,5%, perdas de 3,5%, custo de transporte de R$ 92 por pedido planejado e contas vencidas há mais de 30 dias de 22%. No ramo “com pacote hipotético”, as premissas produzem 82%, 91%, 85%, 2%, R$ 84 e 15%, respectivamente.

Esses deltas são diferenças aritméticas entre premissas. Não medem a NorteVia, não demonstram relação de causa e efeito e não devem ser apresentados como ganhos comprovados. O código e os testes verificam o cálculo, não a eficácia do pacote.

## Rotas de leitura

- [Apresentação e contexto fictício da empresa](README.md)
- [Planejamento estratégico](projetos/planejamento-estrategico/README.md) e [simulação de resposta COVID-19](projetos/planejamento-estrategico/docs/simulacao-resposta-covid19.md)
- [Abastecimento e logística](projetos/abastecimento-logistica/README.md), [resultados da simulação](projetos/abastecimento-logistica/docs/simulacao-covid19-resultados.md) e [contrato de dados](projetos/abastecimento-logistica/docs/contrato-dados.md)
- [Governança de indicadores](projetos/governanca-indicadores/README.md) e [mapas de processos/indicadores](projetos/governanca-indicadores/docs/simulacao-covid19-processos.md)
