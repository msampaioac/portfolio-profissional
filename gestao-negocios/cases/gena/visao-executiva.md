# GENA — Visão executiva dos projetos

**Documento da empresa e dos projetos**

Gestão e Negócios orientada por Dados

[Portfólio de Gestão](../../README.md) · [Empresas](../README.md) · [Contexto da GENA](README.md)

## A decisão em uma página

O Grupo Educacional Nascente do Acre (GENA) é uma empresa **fictícia** com 10.040 alunos ativos no cenário de 2025. A base sintética verificável reproduz na graduação EAD churn de 27,5%, inadimplência **monetária na posição de referência** de 13,5% e NPS 39. Esses números calibrados levantam uma pergunta de planejamento: **como crescer sem ampliar perdas de permanência, confiança e caixa?**

A recomendação é estabelecer definições confiáveis de indicadores e testar intervenções de retenção antes de ampliar iniciativas de crescimento. A continuidade entre Ensino Médio e graduação permanece no portfólio, mas depende de conhecer seu funil e de validar a capacidade de atendimento.

## Da evidência à decisão

| Evidência do cenário | Interpretação | Recomendação |
|:---|:---|:---|
| Métricas divergentes entre áreas | A priorização pode partir de números incompatíveis | Definir população, fórmulas, responsáveis e regras de qualidade |
| EAD com churn de 27,5%, inadimplência monetária na posição de referência de 13,5% e NPS 39 | A permanência exige investigação por coorte e jornada | Reconciliar a base e, em etapa futura, testar atendimento preventivo |
| Dados financeiros e acadêmicos fragmentados | Não há comprovação de quanto cada intervenção recupera | Medir permanência, custo e margem incremental separadamente |
| Relação com concluintes do Ensino Médio pouco estruturada | Existe uma hipótese de continuidade a validar | Mapear intenção, conversão e permanência antes de escalar campanhas |

Essas interpretações são hipóteses de planejamento; os indicadores não comprovam relações de causa e efeito.

## Três estudos para examinar

| Estudo | O que demonstra | Onde verificar |
|:---|:---|:---|
| Planejamento estratégico | Priorização, objetivos e coordenação de iniciativas | [SWOT, OKRs e execução](projetos/planejamento-estrategico/README.md) |
| Retenção EAD | Tradução de um indicador em hipótese, piloto e critério de decisão | [Plano de intervenção e avaliação](projetos/retencao-ead/README.md) |
| Governança de indicadores | Correção de uma divergência didática, cinco indicadores recalculados e decisões rastreáveis | [Contrato, evidências, testes próprios e defesa do case](projetos/governanca-indicadores/README.md) |

## O que levar ao comitê

**Estágio disponível no cenário simulado:** base sintética, gerador e 13 testes de contrato no projeto de Retenção EAD; ciclo de governança com fontes, modelo lógico, decisões, cálculo independente de cinco indicadores e testes próprios. Dashboard, modelo, implantação empresarial, piloto, efeito e ROI ficam para etapas posteriores.

No exemplo de governança, a leitura de churn com denominador inadequado é 24,68%; com a coorte elegível, 27,50%. A diferença de 2,82 pontos percentuais é **correção de definição**, não aumento de evasão ou efeito de intervenção. Conversão Médio → Graduação permanece preliminar, sem dados de funil.

A meta anual ilustrativa é reduzir o churn EAD em **15% relativos**, de 27,5% para **23,375%** na mesma população e janela de referência. Isso equivale a 4,125 pontos percentuais, não a uma redução de 15 pontos. O cenário de 2025 precisa ser atualizado antes de um ciclo de execução em 2027.

Um piloto de 90 dias pode testar viabilidade, qualidade e sinais de permanência em etapa futura. **Não comprova, por si só, o cumprimento de uma meta anual; não há piloto nesta melhoria.**

## Entregas e limites

**Disponível para exame:** documentação de estratégia; base e controles da Retenção EAD; inventário, contrato, modelo lógico, comparação de definições, decisões e reconciliação executável da Governança. **Ainda futuro:** implementação operacional completa, análise diagnóstica SQL, dashboard, treinamento de modelo preditivo, piloto, análise causal, validação de risco e comprovação de impacto ou ROI.

### Base disponível para exame

A conciliação fixa a abertura EAD em 2.880; 40 conclusões e 40 transferências saem retroativamente do denominador, resultando em 2.800 elegíveis, 770 cancelamentos (27,5%), 2.030 retidos (72,5%) e 1.090 ingressantes ativos de março a novembro. O fechamento é 3.120, enquanto 3.970 é o total anual de indivíduos distintos. NPS 39 é calibrado com 200 respostas (118 promotores, 42 passivos e 40 detratores).

Financeiro, NPS e saídas de abril a dezembro de 2025 não são features para o corte de 28/02/2025. As oito semanas de engajamento (06/01–28/02) partem dos 2.880 da abertura e são geradas independentemente do desfecho; não há conclusão de que baixo engajamento provoque churn. A amostra didática EAD cobre Administração, Pedagogia e Gestão Pública nos polos Cidade Nova, Cruzeiro do Sul e Sena Madureira, sem base para inferência.

[Projeto de Retenção EAD](projetos/retencao-ead/README.md) · [Índice da base](projetos/retencao-ead/dados/README.md) · [Contrato](projetos/retencao-ead/docs/contrato-dados.md) · [Validação](projetos/retencao-ead/dados/validacao.md) · [Gerador Python](projetos/retencao-ead/scripts/gerar_dados_gena.py) · [Testes](projetos/retencao-ead/tests/test_dados_gena.py).

Os estudos foram estruturados com apoio de IA. A base é simulada; qualquer uso operacional exige revisão, validação das definições e dados com uso aprovado.

## Referência documental

Este documento é a visão executiva da empresa GENA e de seus projetos. A [documentação institucional da empresa](README.md) é a base de referência; os artefatos operacionais ficam nos respectivos projetos: [planejamento estratégico](projetos/planejamento-estrategico/README.md), [retenção EAD](projetos/retencao-ead/README.md) e [governança de indicadores](projetos/governanca-indicadores/README.md).
