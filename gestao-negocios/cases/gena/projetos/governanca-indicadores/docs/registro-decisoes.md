# Registro de decisões metodológicas

**Elaboração: 21/10/2026 · Referência dos dados: 2025 · Estudo fictício**

[Projeto](../README.md) · [Defesa do case](defesa-do-case.md) · [Reconciliação](../evidencias/reconciliacao.md)

Este registro documenta escolhas do estudo de portfólio, não atas ou aprovações de uma empresa real.

## D001 — churn da coorte, não fotografia final

| Campo | Registro |
|:---|:---|
| Problema demonstrado | Criar deliberadamente uma leitura com denominador inadequado para testar a governança da métrica |
| Evidência | 770 cancelamentos; 3.120 ativos finais produzem 24,68%; 2.800 elegíveis da abertura produzem 27,50% |
| Decisão metodológica | Usar a coorte elegível; separar 40 conclusões e 40 transferências, conciliando essas saídas |
| Alternativa descartada para esta pergunta | Dividir cancelamentos da abertura pela foto de ativos finais, que mistura retidos e ingressantes |
| Justificativa | Numerador e denominador devem se referir à mesma população e janela |
| Tratamento demonstrado | Registrar a causa, explicitar a regra e recalcular com controles; preservar os CSV de origem |
| Resultado técnico | Diferença de 2,82 pontos percentuais por definição; não aumento de churn ou efeito de atendimento |
| Condição de revisão | Mudança no conceito de evasão, na janela, nos status ou na população exige nova versão e comparação histórica |
| Evidência reproduzível | [CSV da comparação](../evidencias/comparacao-churn.csv), [script](../scripts/reconciliar_indicadores.py), [testes](../tests/test_reconciliacao.py) e [relatório](../evidencias/reconciliacao.md) |

O status final é conhecido retrospectivamente. A elegibilidade assim reconstruída não é uma variável disponível para prever risco em fevereiro. No laboratório, o fechamento é técnico; não representa aceite de um patrocinador.

## D002 — preservar uma única fonte

**Decisão:** reutilizar a base e a configuração de Retenção EAD sem duplicar ou gerar novos registros. **Alternativa descartada:** manter outra cópia de dados no projeto de Governança. **Justificativa:** evitar deriva e tornar mudanças rastreáveis. **Verificação:** hashes da configuração e dos seis CSV, contagens e vínculos; ver [inventário](inventario-fontes.md) e [modelo lógico](modelo-logico.md).

A autoria das fontes continua atribuída ao projeto de Retenção EAD, desenvolvido com apoio de IA. Os testes próprios da Governança verificam o consumo e as definições deste ciclo.

## D003 — cinco indicadores demonstrados; conversão preliminar

**Decisão:** implementar churn, retenção, adimplência, inadimplência e NPS com fontes existentes. Os dois pares complementares não são apresentados como medidas independentes. **Alternativa descartada:** inventar dados de funil para declarar cobertura dos seis indicadores. **Expansão delimitada:** conversão Médio → Graduação, separada de leads comerciais, depende de fonte de concluintes, matrícula, vínculo por pessoa, elegibilidade e janela. **Evidência:** [contrato](dicionario-indicadores.md).

## D004 — separar laboratório, implantação e intervenção

**Decisão:** entregar um ciclo técnico verificável e planejar a implantação por marcos antes de iniciar um piloto de retenção. **Alternativa descartada:** prometer efeito de negócio em um cronograma fechado sem conhecer capacidade, acesso e esforço. **Ritmo proposto:** uma revisão de trabalho entre Coordenação, Negócio e BI; Direção acionada para decisões materiais. **Evidência:** [plano de implantação](plano-implantacao.md).

O estudo não possui atendimento executado, custo de intervenção, prazo operacional cumprido ou ROI. A definição da métrica é uma condição para medir resultados futuros, não uma substituição dessa medição.
