# Documentação do portfólio

[Voltar ao portfólio](../README.md) · [Cases](../cases/README.md) · [Modelos de trabalho](../templates/README.md)

## Qual documento abrir?

| Documento | Para que serve | Público principal |
|:---|:---|:---|
| [Síntese executiva](apresentacao-executiva.md) | Entender problema, recomendação e evidências em uma leitura curta | Recrutadores, lideranças e examinadores |
| [Empresa fictícia — GENA](empresa-ficticia-grupo-educacional.md) | Consultar história, produtos, unidades e indicadores de referência | Quem deseja aprofundar os cases |
| [Base sintética GENA](../dados/gena/README.md) | Examinar contrato, CSV, reconciliação e limites da primeira melhoria | Quem deseja reproduzir ou auditar as regras |

## Estado das entregas

| Entrega | Situação neste repositório |
|:---|:---|
| Perfil institucional e cenário de negócio | Documentado, com indicadores de referência |
| Diagnóstico e planejamento estratégico | Proposta documentada |
| Projeto de retenção EAD | Desenho futuro de piloto e avaliação documentados |
| Governança de indicadores | Definições, reconciliação e controles propostos |
| Modelos de gestão | Modelos reutilizáveis, não registros de execução |
| Dataset CSV + gerador Python + testes | Primeira melhoria: base sintética verificável referenciada no [índice](../dados/gena/README.md), [gerador](../scripts/gerar_dados_gena.py) e [testes](../tests/test_dados_gena.py); não é dado real |
| Reconciliação do snapshot EAD | Contrato e regras documentados; execução operacional deve ser registrada sem antecipar aprovação |
| Análise diagnóstica SQL | Futura, após a base e a reconciliação |
| Dashboard Power BI do GENA | Futuro; não implementado nesta etapa |
| Modelo preditivo, piloto e efeito causal | Futuros; não autorizados nesta primeira melhoria |
| Resultados, ROI e impacto realizados | Futuros e não medidos |

## Base disponível para exame

A primeira melhoria trata uma base sintética calibrada, seu gerador, testes e reconciliação. No EAD, 2.880 abertos em janeiro geram 2.800 elegíveis após retirar 40 conclusões e 40 transferências, 770 cancelamentos (27,5%), 2.030 retidos (72,5%) e 1.090 ingressantes ativos de março a novembro; o fechamento é 3.120 e o total anual distinto é 3.970. NPS 39 usa 200 respostas (118/42/40); 13,5% é inadimplência **monetária na posição de referência** dos títulos de 2025 vencidos até 31/12/2025, apenas calibração.

Os valores são sintéticos e testáveis, não padrão factual. O corte de features de 28/02/2025 exclui financeiro, NPS e saídas de abril a dezembro de 2025; engajamento de 06/01 a 28/02 é independente do desfecho, portanto não há conclusão causal. A fonte única de parâmetros é o [`config.json`](../dados/gena/config.json). Consulte o [contrato](contrato-dados-gena.md), a [validação](../dados/gena/validacao.md), o [gerador Python](../scripts/gerar_dados_gena.py) e os [testes](../tests/test_dados_gena.py).


## Regras para evolução

A base sintética desta primeira melhoria declara período, granularidade, denominadores e regras de status acadêmico; novos datasets devem seguir o mesmo contrato. A fotografia de alunos ativos não deve ser confundida com ingressantes, população elegível para churn ou acumulado de formados.

Novos resultados devem distinguir **linha de base simulada, meta, projeção e observação medida**. Para transformar uma proposta em evidência de execução, será necessário incluir dados, método reproduzível, validação e registro das decisões.

Os estudos foram estruturados com apoio de IA para redação e organização. Isso não substitui domínio do conteúdo nem validação antes de aplicação operacional. As evidências técnicas de SQL, Python e BI disponíveis em outro contexto estão no [portfólio de Dados](https://github.com/msampaioac/data-analytics-portfolio).
