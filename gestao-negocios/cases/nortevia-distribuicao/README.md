# NorteVia Distribuição — empresa fictícia

> **Este é um universo de negócio inventado para estudos de portfólio.** A NorteVia, sua trajetória, estrutura, clientes, fornecedores, processos, números, papéis e decisões não representam uma empresa real nem experiência profissional realizada. Todos os quantitativos são premissas didáticas. As simulações não são resultados observados, previsões ou estimativas de impacto.

[Índice de empresas](../README.md) · [Guia da trilha Gestão e Negócios](../../README.md) · [Visão executiva](visao-executiva.md)

## O que é a NorteVia

A NorteVia Distribuição é uma distribuidora B2B imaginária, sediada em Rio Branco, Acre. No universo do case, compra alimentos de fabricantes e fornecedores e os entrega a pequenos mercados, mercadinhos e operações de food service em localidades acreanas. Sua proposta de valor é simplificar o abastecimento desses clientes por meio de sortimento útil, reposição e entregas regionais previsíveis.

O mix didático combina alimentos secos e embalados com uma parcela de produtos refrigerados. A operação pressupõe um armazém central, recebimento e armazenagem, gestão por SKU/lote/validade, separação de pedidos, transporte e cobrança. Os desafios se encadeiam: uma falta de fornecedor pode causar ruptura, entrega incompleta, substituição, custo logístico, reclamação e atraso no recebível.

| Elemento do cenário | Premissa fictícia | O que precisa ser validado numa operação real |
|:---|:---|:---|
| Sede e armazém | Rio Branco-AC; um armazém central | Endereço, infraestrutura, capacidade, segurança e licenças aplicáveis |
| Clientes | Pequenos mercados/mercadinhos e food service | Segmentos atendidos, contratos, critérios de prioridade e necessidades |
| Catálogo e carteira | 450 SKUs e 320 contas como parâmetros didáticos | Cadastro, atividade, mix, volumes, unidades de venda e concentração |
| Produtos | Alimentos secos/embalados e alguns refrigerados | Regras de armazenamento, temperatura, validade, rastreabilidade e devolução |
| Distribuição | Entregas B2B em municípios acreanos | Municípios efetivamente cobertos, rotas, janelas, custos e capacidade |
| Sistemas e dados | Nenhum ERP, WMS, TMS ou CRM é presumido | Fontes existentes, direitos de acesso, qualidade e integração |

Os números de 450 SKUs e 320 contas descrevem somente a escala imaginada para orientar a análise. A simulação COVID usa uma coorte específica de 100 pedidos planejados e denominadores próprios; ela não deve ser extrapolada para o total de contas ou catálogo.

## Por que este case é diferente da GENA

A GENA é um estudo sobre educação, jornada acadêmica, retenção e governança de indicadores. A NorteVia desloca o foco para **abastecimento, estoque, transporte, segurança dos alimentos e capital de giro**. Isso permite demonstrar o mesmo raciocínio de estratégia e gestão de projetos em outro setor, com diferentes decisões e contratos operacionais — sem reutilizar métricas de aluno, matrícula ou churn.

## Três projetos

| Projeto | Pergunta de gestão | Conteúdo disponível |
|:---|:---|:---|
| [Planejamento estratégico](projetos/planejamento-estrategico/README.md) | Como proteger a continuidade do abastecimento e a liquidez quando oferta, demanda e capacidade ficam incertas? | Diagnóstico e hipóteses, escolhas e trade-offs, OKRs condicionais, governança, riscos, gates e plano proposto de 90 dias |
| [Abastecimento e logística](projetos/abastecimento-logistica/README.md) | Como explicitar disponibilidade, serviço, perdas, custo de transporte e recebíveis em uma decisão operacional? | Contrato das métricas, configuração sintética, gerador Python, CSV reproduzível, seis KPIs e testes automatizados |
| [Governança de indicadores](projetos/governanca-indicadores/README.md) | Como ligar pedido, SKU/lote, rota, prova de entrega e contas a receber a uma rotina confiável de decisão? | Mapas de processo hipotéticos, responsabilidades, definições, controles, auditoria e gates |

## Simulação retrospectiva COVID-19

A pandemia é usada como **situação de estresse simulada em 2020**, não como alegação de que a NorteVia existiu ou reagiu à crise. A referência da OCDE documenta que as cadeias alimentares foram pressionadas em diferentes pontos — da produção ao processamento, transporte/logística e demanda — com impactos variáveis por produto e setor [1]. Essa fonte oferece contexto geral; não fornece nem valida os números fictícios do case.

A resposta hipotética combina classificação de fornecedores e SKUs por risco/lead time, estoque de segurança focalizado, substituições com aceite do cliente, consolidação de rotas, controle de validade e cadeia fria e revisão semanal de caixa. O pacote tenta equilibrar continuidade e custo: comprar mais pode reduzir risco de ruptura, mas imobiliza capital e aumenta a exposição a vencimento; consolidar entregas pode reduzir viagens, mas diminui flexibilidade.

O espelho quantitativo compara dois ramos de premissas — “sem pacote coordenado” e “com pacote hipotético” — numa janela de observação de oito semanas, com cutoff no dia 56 e consolidação documental até o dia 63. Entre os seis indicadores figuram OTIF de 62% versus 82%, fill rate de 80% versus 91%, disponibilidade de SKU-dias de 62,5% versus 85%, e custo de transporte alocado de R$ 92 versus R$ 84 por pedido planejado. **São resultados aritméticos de valores escolhidos para exercício, não observações, impacto causal, previsão ou ROI.** As definições, arredondamentos e limites constam do [projeto operacional](projetos/abastecimento-logistica/docs/simulacao-covid19-resultados.md).

Leia em sequência a [resposta estratégica simulada](projetos/planejamento-estrategico/docs/simulacao-resposta-covid19.md), o [espelho reproduzível de resultados](projetos/abastecimento-logistica/docs/simulacao-covid19-resultados.md) e os [mapas de processos e contratos dos indicadores](projetos/governanca-indicadores/docs/simulacao-covid19-processos.md).

## Limites do case

- A empresa e todo o seu universo operacional são fictícios. Não são apresentados dados de clientes ou fornecedores reais.
- Os números e os contratos analíticos são premissas selecionadas, não registros amostrais ou evidências de mercado.
- O plano estratégico é uma proposta; não há implantação, compra, piloto, operação medida ou resultado empresarial realizado.
- As diferenças entre os ramos COVID-19 são aritmética descritiva e não provam que as decisões propostas causariam aquelas mudanças.
- Os resultados de oito semanas não são anualizados. A base não permite calcular ROI, estimar efeito, prever vendas ou concluir sobre toda a distribuição de alimentos no Acre.
- As métricas não substituem revisão humana de segurança alimentar, condições de crédito, privacidade, tratamento equitativo de clientes e capacidade operacional.

## Referência

[1]: https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/06/food-supply-chains-and-covid-19-impacts-and-policy-lessons_62c97266/71b57aea-en.pdf "Food Supply Chains and COVID-19: Impacts and Policy Lessons"
