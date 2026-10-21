# Defesa do case — governança de indicadores

**Respostas para entrevista sobre o estudo de portfólio**

[Projeto](../README.md) · [Decisões metodológicas](registro-decisoes.md) · [Evidência técnica](../evidencias/reconciliacao.md)

Apresento estas respostas como defesa das escolhas do estudo fictício, não como relato de uma implantação empresarial. A documentação e o código foram desenvolvidos com apoio de IA; as evidências permitem examinar o raciocínio e reproduzir os cálculos.

## 1. Por que você excluiu conclusões e transferências do churn?

**Neste estudo, escolhi medir abandono, não toda saída acadêmica.** Uma conclusão regular ou uma transferência externa precisa ser conciliada, mas não recebe automaticamente o mesmo significado de cancelamento.

A abertura tem 2.880 matrículas. Separando 40 conclusões e 40 transferências, obtenho 2.800 elegíveis; 770 cancelados e 2.030 retidos completam essa população. Essa é a razão para usar churn e retenção como pares complementares nesta versão.

Reconheço o limite da escolha: a elegibilidade depende retrospectivamente do status final. Portanto, ela não é informação disponível para priorizar alunos em fevereiro e não deve entrar como variável de um modelo naquele corte.

A alternativa seria uma taxa bruta de saídas da abertura: `100 × (40 + 40 + 770) ÷ 2.880 = 29,51%`. Eu a manteria com outro nome, pois responde a outra pergunta. A decisão e a regra estão no [contrato](dicionario-indicadores.md).

## 2. Como você investigaria dois relatórios divergentes?

**Primeiro comparo definições, não escolho o número mais conveniente.** Verifico pergunta, fonte, período, população, status, chave e versão. Confiro se os arquivos correspondem aos hashes e se alguma junção multiplicou registros.

No cenário didático, uso o mesmo numerador de 770 cancelamentos. A visão inadequada divide pela fotografia de 3.120 ativos finais e mostra 24,68%; a regra da coorte divide por 2.800 elegíveis e mostra 27,50%.

A diferença de 2,82 pontos percentuais é a correção do denominador, não uma mudança de evasão. Registro causa, regra escolhida, alternativa descartada e evidência. Uma taxa não conciliada não deve orientar priorização. O [registro D001](registro-decisoes.md) e a [reconciliação](../evidencias/reconciliacao.md) demonstram esse ciclo no estudo.

## 3. Quem pode mudar uma fórmula?

**Eu separo validação do negócio, execução técnica e autoridade de aprovação.** No desenho proposto, a área responsável pelo dado valida o significado; a Coordenação formaliza o contrato; BI implementa e testa. Uma mudança de regra segue a aprovação da Direção indicada na RACI.

Correção técnica que restabelece uma definição já aprovada não é o mesmo que trocar o denominador ou o conceito da métrica. Na mudança de definição, registro nova versão, motivo, efeito sobre a comparabilidade e condição de revisão, preservando o cálculo anterior. Não apresento esses papéis fictícios como pessoas que aprovaram o portfólio.

## 4. Qual controle é indispensável e qual reunião pode ser simplificada?

**Minha prioridade é impedir que população ou denominador incorretos produzam uma decisão aparentemente precisa.** Por isso começo por unicidade, status, coorte, janela e conciliação. Campos ausentes ou desconhecidos não podem ser transformados silenciosamente em zero ou em cancelamento.

Antes de um piloto, proponho uma revisão de trabalho com Coordenação, Negócio e BI, com pendência, responsável e prazo. A Direção é acionada para mudanças materiais de regra, risco, prioridade e recursos. Não criaria vários comitês para tratar a mesma falha. A cadência deve acompanhar o volume de trabalho, como detalhado no [plano](plano-implantacao.md).

## 5. O que os testes demonstram — e o que não demonstram?

**Os 13 testes da Retenção EAD verificam o contrato da base gerada de 2025.** Eles cobrem integridade, populações, financeiro, NPS, janelas iniciais e reprodução. Não comprovam operação real, conversão, governança implantada ou efeito de intervenção. Os cinco indicadores recalculados no contrato EAD 2025 são distintos dos seis KPIs da simulação COVID-19; os testes desta última verificam apenas a consistência de suas premissas fictícias.

A [suíte própria deste projeto](../tests/test_reconciliacao.py) verifica a reconciliação, o cenário de denominador inadequado e o cálculo dos cinco indicadores disponíveis. A contagem e os resultados executados constam no [relatório](../evidencias/reconciliacao.md). Não confundo repetir arquivos sintéticos com validar duas cargas reais de produção.

Conversão está fora do cálculo. Delimitei uma especificação preliminar de Médio → Graduação, separada de leads comerciais, mas faltam fonte de concluintes, eventos, vínculo por pessoa e janela aprovada. Não apresento resultado ou meta onde não existe dado.

## 6. Qual é sua contribuição e como você utilizou IA?

**A contribuição que apresento é conectar uma decisão de gestão a regras e evidências verificáveis.** O portfólio explicita as escolhas de população, a reutilização de uma fonte, a correção semântica e os limites para avançar ao piloto.

A IA apoiou documentação, modelagem, dados sintéticos e código. A trilha de revisão disponível é formada por configuração, fontes, diferenças de versão, testes e relatório de execução. Não atribuo ao uso dessas ferramentas autoria manual exclusiva, experiência com clientes ou gestão de uma equipe real.

Em entrevista, a defesa do trabalho é explicar as regras, executar os comandos, interpretar os resultados e justificar as alternativas. Os testes mostram o comportamento do artefato; o domínio pessoal deve ser demonstrado nessa conversa, não presumido por existir um README.

## Contribuição e evidências em uma leitura

| Decisão apresentada | Evidência do estudo |
|:---|:---|
| Delimitar a população que responde à pergunta de negócio | [Contrato](dicionario-indicadores.md) e [comparação](../evidencias/comparacao-churn.csv) |
| Preservar a origem e evitar duplicação de bases | [Inventário](inventario-fontes.md) e [modelo lógico](modelo-logico.md) |
| Documentar a escolha e verificar o efeito da definição | [Decisões](registro-decisoes.md), [script](../scripts/reconciliar_indicadores.py) e [testes](../tests/test_reconciliacao.py) |
