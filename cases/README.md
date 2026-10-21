# Cases de Gestão Estratégica e de Projetos

Os estudos desta pasta aplicam diferentes perspectivas ao **mesmo grupo educacional fictício, GENA**. Não são três clientes distintos nem três implementações realizadas. A primeira melhoria transversal acrescenta uma base sintética verificável, gerador, testes e reconciliação; seus resultados não são fatos da operação.

[Voltar ao portfólio](../README.md) · [Síntese executiva](../docs/apresentacao-executiva.md) · [Conhecer a empresa](../docs/empresa-ficticia-grupo-educacional.md)

## Escolha o estudo pela competência que deseja avaliar

| Interesse do avaliador | Case recomendado | Evidência a examinar |
|:---|:---|:---|
| Estratégia e priorização | [Plano estratégico](grupo-educacional/README.md) | Diagnóstico, escolhas, OKRs, riscos e coordenação |
| Execução de projetos | [Redução de churn EAD](grupo-educacional/reducao-churn-ead.md) | Escopo, base sintética, reconciliação, backlog futuro e critérios para avançar |
| BI e governança | [Governança de indicadores](governanca-indicadores-bi.md) | Fórmulas, papéis, controles e aceite |

## Ordem de leitura sugerida

Comece pela [síntese executiva](../docs/apresentacao-executiva.md), avance para o plano estratégico e depois examine a retenção e a governança. Consulte a empresa fictícia apenas quando precisar aprofundar o contexto ou conferir a linha de base.

## Como as peças se conectam

A **estratégia** define o problema e a prioridade. O **projeto de retenção** transforma essa escolha em um piloto. A **governança** estabelece as condições para confiar nos indicadores e avaliar o piloto. Os [modelos de trabalho](../templates/README.md) apoiam a documentação dessas decisões.

## Estágio e limites

Todos os cases estão no estágio de **planejamento documentado**. A base sintética é verificável para exame; seus números são calibrados, as metas são propostas e não há análise causal, risco validado, benefício medido ou impacto realizado. A implementação operacional de gerador/testes/reconciliação é a primeira melhoria; dashboard, modelo, piloto, efeito e ROI são etapas futuras.

As frentes de transição Ensino Médio → Graduação e adimplência são descritas no universo da empresa como oportunidades de expansão do portfólio. Ainda não são cases completos nem dashboards publicados.

## Base disponível para exame

Consulte o [índice da base sintética](../dados/gena/README.md), o [contrato](../docs/contrato-dados-gena.md), a [validação/reconciliação](../dados/gena/validacao.md), o [gerador Python](../scripts/gerar_dados_gena.py) e os [testes](../tests/test_dados_gena.py). A conciliação EAD usa abertura 2.880, exclusões de 40 conclusões e 40 transferências, 2.800 elegíveis, 770 cancelamentos, 2.030 retidos, 1.090 ingressantes ativos de março a novembro, fechamento 3.120 e 3.970 distintos no ano. NPS 39 usa 200 respostas; 13,5% é inadimplência monetária na posição de referência.

Os cursos e polos EAD são uma premissa didática (Administração, Pedagogia, Gestão Pública; Cidade Nova, Cruzeiro do Sul e Sena Madureira). O corte de 28/02/2025 exclui as saídas de abril a dezembro de 2025 e demais dados posteriores; o engajamento das oito semanas é independente do desfecho.
