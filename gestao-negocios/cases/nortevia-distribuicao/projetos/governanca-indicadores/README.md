# Governança de indicadores — NorteVia Distribuição

**Case de portfólio · estudo fictício · Rio Branco, Acre**

[Empresa NorteVia Distribuição](../../README.md) · [Abastecimento e logística](../abastecimento-logistica/README.md) · [Planejamento estratégico](../planejamento-estrategico/README.md) · [Simulação COVID-19: processos e indicadores](docs/simulacao-covid19-processos.md)

> A NorteVia Distribuição é uma empresa inteiramente fictícia, criada para este estudo: um atacadista B2B de alimentos em Rio Branco-AC, com um armazém e atendimento a pequenos mercados e operações de food service. Os processos, papéis, valores, denominadores e resultados abaixo são hipotéticos. Não são dados de uma empresa real nem resultados observados.

## Objetivo e abordagem

Este projeto adapta ao contexto de distribuição de alimentos os princípios de governança do case GENA: definir a população antes de calcular, explicitar fórmula e exceções, atribuir responsáveis, manter trilha de auditoria e separar proposta de gestão de evidência de resultado. As dimensões aqui são pedido, fornecedor, SKU/lote/validade, armazém, rota, cliente/crédito/contas a receber e evidência logística. Não se aplicam dimensões de matrícula, aluno ou churn.

A [simulação de processos e indicadores](docs/simulacao-covid19-processos.md) contrasta dois ramos hipotéticos de 100 pedidos planejados, fixa contratos para seis KPIs e descreve os controles para uma decisão de gestão. O ramo “com pacote hipotético” é apenas uma ilustração numérica. A diferença entre os ramos não demonstra que o pacote causou melhoria, que uma intervenção ocorreu ou que os valores representam a NorteVia.

## Governança proposta

| Papel fictício | Responsabilidade proposta | Evidência a manter |
|:---|:---|:---|
| Direção | Aprovar objetivo, limites de risco, recursos e decisões dos gates | Ata ou registro datado de decisão, condições e responsável |
| Coordenação de Operações e Dados | Manter calendário, contratos, pendências e versão do dicionário | Registro de alterações e pauta das revisões |
| Responsável de Vendas/Pedidos | Validar escopo, pedido original, promessa e aceite de substituição | Identificador do pedido, horário, versão e aceite do cliente |
| Responsável de Abastecimento | Validar fornecedor, lead time, recebimento e disponibilidade por SKU/lote/validade | Pedido de compra, recebimento e ocorrência de ruptura |
| Responsável de Armazém/Qualidade | Validar saldo, FEFO, cadeia fria, separação e avaria/validade | Movimentos por lote, checagens e ocorrências |
| Responsável de Logística | Validar plano de rota, pedido planejado, entrega e prova de entrega | Rota, horário, status e evidência logística autorizada |
| Responsável Financeiro/Crédito | Validar faturamento, contas a receber, vencimento e corte | Conciliação de títulos, recebimentos e ajustes |
| Analista de Dados (papel de preparação) | Aplicar contratos aprovados, reconciliar fontes e sinalizar exceções | Extração/registro versionado, cálculo reproduzível e log de qualidade |

O dono de cada dado confirma o significado operacional; a Direção aprova mudanças materiais de regra ou prioridade; quem prepara o cálculo não aprova sozinho a própria alteração. Uma pessoa pode acumular papéis em uma operação pequena, mas a revisão independente deve ser registrada sempre que viável; quando não houver revisor independente, a limitação deve ser declarada e a Direção deve revisar as exceções críticas.

Não se presume a existência de CRM, ERP, WMS, TMS, BI ou integração. Um registro temporário controlado em planilha ou formulário pode ser usado se tiver acesso restrito, campos e versões documentados, cópia de segurança, histórico de alterações, conferência com documentos de origem e reconciliação por responsável. A ferramenta não substitui os documentos nem autoriza acesso a dados pessoais além do necessário.

## Regras de integridade e decisão

- Definição, unidade, numerador, denominador, elegibilidade, janela, corte, dono e versão são aprovados antes da leitura. Denominadores não podem ser reduzidos retroativamente para melhorar a taxa; exceções têm justificativa, autor, data e efeito quantificado.
- Preservar o pedido original e registrar separadamente substituições, cortes, recusas, cancelamentos e aceite do cliente. A priorização deve ser explícita e consistente, com revisão humana, critérios documentados e comunicação transparente. Não discriminar clientes sem justificativa legítima, não favorecer contas por critério oculto e não praticar aumento abusivo de preços ou retenção especulativa de alimentos.
- Aplicar FEFO (primeiro a vencer, primeiro a sair) e controles de cadeia fria conforme produto e procedimento validado. Um saldo sem lote/validade ou condição de conservação confiável não deve ser tratado como disponibilidade confirmada.
- Manter trilha de auditoria de pedidos, alterações de promessa, compras, lotes, separação, rota, prova de entrega, faturas e recebimentos. Restringir dados de contato e crédito por necessidade de função, minimizar cópias e mascarar identificadores em relatórios de ampla circulação.
- Revisão semanal reúne caixa e nível de serviço, registra divergências e ações com prazo e responsável. A revisão é humana: indicadores apoiam a decisão, não substituem julgamento sobre segurança alimentar, equidade de alocação, crédito ou atendimento.

A simulação define um plano gerencial de 90 dias. A observação fecha em **8 semanas (56 dias)**, com até 5 dias úteis de maturidade documental e consolidação prevista até o dia 63. Os prazos são marcos propostos, não cronologia de implementação comprovada. Os gates **continue / adjust / pause / stop** têm critérios no documento de simulação; cada decisão exige evidência disponível, responsável e registro. Dados incompletos, cadeia fria comprometida, regra injusta ou risco material podem exigir pausa independentemente do valor do KPI.

## Limite de interpretação e contexto

A publicação oficial da OCDE descreve choques da COVID-19 em diferentes segmentos das cadeias alimentares — produção agrícola, processamento, transporte e logística e demanda final, sem impacto uniforme entre setores e produtos [1]. Esse contexto justifica a escolha didática de olhar o fluxo ponta a ponta; não valida os números hipotéticos nem permite atribuir à NorteVia impactos ou respostas específicos.

## Referência

[1]: https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/06/food-supply-chains-and-covid-19-impacts-and-policy-lessons_62c97266/71b57aea-en.pdf "Food Supply Chains and COVID-19: Impacts and Policy Lessons"
