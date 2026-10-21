# GENA — Gestão Estratégica e Projetos

> **Estudo de caso inteiramente simulado.** O Grupo Educacional Nascente do Acre (GENA), seus contextos, números, papéis e decisões são fictícios e servem apenas para demonstrar raciocínio de gestão. Há uma base sintética verificável para exame; ela não representa emprego, experiência, certificação, resultado realizado, análise causal ou risco validado.

**Horizonte estratégico:** 2027–2029 · **Janela de validação:** piloto dos primeiros 90 dias
**Snapshot de referência:** 2025, a ser revalidado antes de usar qualquer baseline de 2027

## Síntese de decisão

Recomendo aprovar um portfólio sequenciado, começando por **governança mínima e revalidação de dados**, seguido de um piloto de **retenção na graduação EAD** e, somente após evidência de capacidade, pela expansão da jornada **Ensino Médio → Graduação**.

A decisão não é escalar três projetos simultaneamente. É criar uma cadeia de evidências que responda, nesta ordem:

1. Os conceitos, denominadores e fontes permitem medir o problema em 2027?
2. Uma intervenção de retenção é executável, aceitável e economicamente plausível?
3. A continuidade entre etapas gera conversão sustentável sem depender apenas de desconto?

O gate de escala deve exigir baseline validado, responsável nomeado por indicador, custo da intervenção, evidência de execução e sinal de efeito. Até lá, metas são hipóteses de planejamento; não são resultados alcançados.

## Contexto e desafio

A GENA é uma organização educacional privada fictícia, fundada em Rio Branco (AC), com Educação Básica, graduação presencial e EAD, pós-graduação e extensão. No cenário simulado, o snapshot de 2025 registra **10.040 alunos ativos**.

O ponto de atenção é a graduação EAD: o snapshot indica **27,5% de churn anual**, 13,5% de inadimplência **monetária na posição de referência** e NPS 39. Esses números são referências sintéticas calibradas de 2025, não uma medição do ciclo 2027.

O desafio de gestão é converter sinais dispersos em decisões de portfólio: proteger permanência sem prometer impacto, conectar a jornada acadêmica sem mascarar conversão e criar indicadores que possam ser auditados.

## Base disponível para exame

A preparação de dados disponível no projeto de Retenção EAD inclui a base sintética, gerador Python, testes de contrato/reconciliação e conciliação do snapshot EAD. A abertura de 2.880 em janeiro perde 40 conclusões e 40 transferências do denominador, deixando 2.800 elegíveis; 770 cancelamentos produzem 27,5% de churn e 2.030 retidos (72,5%). Há 1.090 ingressantes entre março e novembro, todos ativos no fechamento e sem churn estimado no grupo; o fechamento é 3.120 e o total anual distinto é 3.970.

NPS 39 usa 200 respostas (118/42/40). A inadimplência EAD de 13,5% é monetária na posição de referência de títulos de 2025 vencidos até 31/12/2025, com alvo em centavos ao mais próximo: calibração, não validação real. O corte de 28/02/2025 exclui financeiro, NPS e saídas de abril a dezembro de 2025; engajamento de 06/01 a 28/02 é independente do desfecho, sem conclusão de que baixo engajamento provoque churn.

A amostra didática EAD usa Administração, Pedagogia e Gestão Pública nos polos Cidade Nova, Cruzeiro do Sul e Sena Madureira; isso é premissa, não autorização para inferência. Consulte o [índice da base](../retencao-ead/dados/README.md), o [contrato](../retencao-ead/docs/contrato-dados.md), a [validação](../retencao-ead/dados/validacao.md), o [gerador](../retencao-ead/scripts/gerar_dados_gena.py) e os [testes](../retencao-ead/tests/test_dados_gena.py).


### Diagnóstico do problema

- Dados de matrícula, acesso, pagamentos, desempenho e atendimento estão distribuídos em sistemas distintos.
- Conceitos como aluno ativo, churn, evasão, inadimplência e conversão podem ter denominadores diferentes.
- A intervenção tende a ocorrer depois de faltas, atraso, baixa atividade ou abandono já observáveis.
- A passagem do Ensino Médio para a graduação ocorre sem uma jornada contínua mensurada por turma, canal e curso.
- Bolsas, custos de atendimento e recuperação financeira precisam ser lidos junto da permanência, e não isoladamente.

### SWOT concisa

| Dimensão | Evidência do cenário simulado | Implicação para a decisão |
|:---|:---|:---|
| Forças | Marca regional, proximidade comunitária e presença em várias etapas educacionais | Usar vínculo e continuidade como diferenciação, não competir somente por preço |
| Fraquezas | Dados fragmentados, métricas inconsistentes e baixa visibilidade do funil | Priorizar dicionário, denominadores, rastreabilidade e rotina de decisão |
| Oportunidades | Alertas de risco, trilhas de orientação e uso integrado de dados | Testar intervenções pequenas, mensuráveis e reversíveis |
| Ameaças | Redes nacionais de baixo custo, inadimplência e expectativa digital crescente | Controlar custo, experiência e sustentabilidade antes de escalar |

## Tese estratégica 2027–2029

A tese é **crescer com sustentabilidade por meio de permanência, continuidade e gestão por evidências**. O horizonte 2027–2029 organiza três objetivos interdependentes:

1. **Proteger a permanência:** reduzir churn EAD com intervenção antecipada e avaliação de custo.
2. **Conectar a jornada:** melhorar a conversão do Ensino Médio para a graduação com orientação e relacionamento contínuos.
3. **Decidir com consistência:** estabelecer governança de indicadores para tornar as decisões comparáveis e rastreáveis.

O snapshot de 2025 orienta hipóteses, mas **não substitui a revalidação do baseline para 2027**. Antes do primeiro KR, a equipe deve confirmar população elegível, período, fórmula, fonte, coorte e exclusões.

## Encadeamento: objetivos, iniciativas e KPIs

| Objetivo | Iniciativa prioritária | KPI de efeito ou decisão | Evidência necessária |
|:---|:---|:---|:---|
| Proteger permanência no EAD | P01 — piloto de redução de churn | Churn anual por coorte; retenção; permanência pós-intervenção | Baseline 2027, coortes comparáveis e registro de intervenção |
| Conectar Ensino Médio e graduação | P02 — jornada de transição | Conversão de elegíveis; funil por turma, curso e canal | Denominador de elegíveis, consentimento e trilha de contatos |
| Decidir com indicadores confiáveis | H01 — governança e painel mínimo, habilitador transversal | Cobertura operacional, atualização, qualidade e decisões registradas | Dicionário, linhagem, proprietário, SLA e log de exceções |
| Proteger sustentabilidade financeira | P03 — adimplência e finanças, frente a detalhar | Inadimplência, aging, recuperação e permanência por faixa de atraso | Regras financeiras e conciliação com status acadêmico |

## Priorização e trade-offs

### Critérios de decisão

A priorização usa critérios qualitativos verificáveis, sem atribuir pontuações artificiais:

- **Urgência do risco:** magnitude e proximidade do problema no cenário simulado.
- **Valor estratégico:** contribuição para permanência, continuidade ou sustentabilidade.
- **Dependências:** necessidade de definições, integração ou capacidade antes da execução.
- **Testabilidade:** possibilidade de testar em coorte delimitada e interromper sem grande custo.
- **Equidade e experiência:** risco de excluir alunos, pressionar atendimento ou usar preço como única resposta.
- **Viabilidade:** capacidade disponível, dados acessíveis, custo e conformidade a validar.

### Ordem recomendada

| Ordem | Decisão | Por que agora | Trade-off assumido |
|---:|:---|:---|:---|
| 1 | Governança mínima e baseline 2027 | Sem medida comum, efeito e custo não são interpretáveis | Consome tempo inicial e pode adiar campanhas visíveis |
| 2 | P01 — retenção EAD em piloto | Risco prioritário, hipótese testável e possibilidade de intervenção reversível | Concentra capacidade no EAD antes de cobrir todos os segmentos |
| 3 | P02 — transição Médio → Graduação | Depende de funil, elegibilidade e baseline de conversão mais estáveis | Pode postergar ganho de captação no curto prazo para reduzir desperdício |
| 4 | Escala seletiva e frente financeira integrada | Só após evidência de execução, efeito e custo | Evita escalar uma solução que apenas desloca custo ou inadimplência |

A ordem pode mudar se a revalidação revelar risco financeiro ou operacional superior ao risco de churn. Essa mudança deve ser registrada no comitê, com evidência e consequência explícita.

## OKRs e indicadores verificáveis

### Objetivo 1 — Aumentar a permanência na graduação EAD

| Tipo | Definição verificável | Condição de validade |
|:---|:---|:---|
| KR de efeito | Reduzir o churn anual da graduação EAD em **15% relativamente** ao baseline 2027 validado | Fixar coorte, janela, população elegível e fórmula antes do piloto |
| Referência de planejamento | Snapshot 2025: 27,5%; se o baseline 2027 confirmar 27,5%, a referência calculada é `27,5% × (1 − 15%) = 23,375%` | Se o baseline mudar, recalcular; não tratar 23,375% como resultado observado |
| Indicador de execução, não KR de efeito | Contatar pelo menos **90% dos alunos classificados em risco** dentro do SLA definido | Registrar elegibilidade, data, canal, tentativa e resposta; contato não prova retenção |

**Iniciativas:** definição de churn e coortes; integração de matrícula, acesso, pagamentos, desempenho e atendimento; regra de risco; régua de relacionamento; avaliação de custo e permanência.

### Objetivo 2 — Melhorar a continuidade Ensino Médio → Graduação

| Tipo | Definição verificável | Condição de validade |
|:---|:---|:---|
| KR condicional | Aumentar em **20% relativamente** a conversão de elegíveis do Ensino Médio para a graduação | Só definir o alvo após baseline 2027, elegibilidade, período e denominador validados; fórmula: `baseline × 1,20` |
| Indicadores de funil | Interessados, leads qualificados, orientações, inscrições, matrículas e retenção inicial | Cortar por turma, curso, canal e perfil; não confundir contato com matrícula |

**Iniciativas:** mapa da jornada; orientação de carreira; experiências com cursos; CRM de potenciais ingressantes; oferta com critérios transparentes; mensuração de custo e continuidade.

### Objetivo 3 — Tornar a gestão orientada por indicadores

| Tipo | Definição verificável | Condição de validade |
|:---|:---|:---|
| Meta operacional de implantação | Cobrir **95% dos indicadores operacionais priorizados** com definição, fórmula, fonte, proprietário, frequência, SLA e log de exceções | A base de indicadores e a cobertura inicial serão apuradas no piloto; não é KR de resultado de negócio |
| Indicadores de governança | Atualização no prazo, completude, divergências, decisões registradas e tempo de resposta | Medir por ciclo mensal, com trilha de auditoria e plano de correção |

**Iniciativas:** dicionário de métricas; linhagem de dados; painel mínimo; rito mensal; registro de decisões; revisão trimestral do portfólio.

## Piloto dos primeiros 90 dias (etapa futura)

O piloto testa viabilidade e sinais de efeito na janela observável. Não comprova sozinho o cumprimento de uma meta anual de churn; esse resultado exige acompanhamento por período compatível. O plano abaixo é proposto, não executado.

| Período | Entregas e perguntas | Gate de saída |
|:---|:---|:---|
| Dias 1–15 | Confirmar sponsor, papéis, escopo EAD, fontes, privacidade, definições e critérios de sucesso | Acesso autorizado, escopo delimitado e riscos críticos registrados |
| Dias 16–30 | Reconstituir snapshot 2025 apenas como referência, desenhar baseline 2027, dicionário e mapa de dados | Denominadores e fórmulas aprovados; lacunas explicitadas |
| Dias 31–45 | Em etapa futura: construir painel mínimo e classificação de risco após a base sintética e a reconciliação | Qualidade mínima, rastreabilidade e regra de risco revisadas |
| Dias 46–60 | Executar contato em coorte-piloto, registrar SLA, resposta, custo e encaminhamento | Pelo menos um ciclo de execução observável; sem afirmar efeito causal |
| Dias 61–75 | Comparar execução e sinais de permanência, revisar experiência e testar jornada de transição em desenho | Evidência suficiente para ajustar escopo ou interromper hipótese |
| Dias 76–90 | Consolidar resultados do piloto, business case, backlog, RACI e recomendação ao comitê | Decisão documentada: continuar, ajustar, pausar ou parar |

## Governança e responsabilidades

Os papéis abaixo são funções fictícias do desenho; não representam nomes, cargos ocupados ou experiência do candidato.

| Papel fictício | Responsabilidade no case |
|:---|:---|
| Sponsor Executivo | Destravar decisões, aprovar escopo, aceitar riscos e presidir o gate |
| Dono de Retenção EAD | Definir jornada, validar intervenções e responder pelo resultado do P01 |
| Dono da Jornada Acadêmica | Definir elegibilidade e experiência do P02 com áreas escolares e superiores |
| Líder de Dados e Indicadores | Manter dicionário, linhagem, qualidade, painel e alertas |
| Líder de Projetos | Integrar cronograma, dependências, riscos, decisões e benefícios esperados |
| Representante Financeiro | Validar inadimplência, custos, descontos, recuperação e premissas econômicas |
| Representante de Atendimento | Garantir capacidade, SLA, registro de contatos e feedback dos alunos |
| Comitê de Portfólio | Revisar evidências e decidir continuar, ajustar, pausar ou parar |

Rituais: acompanhamento quinzenal de entregas e riscos; comitê de retenção quinzenal; reunião mensal de indicadores; revisão de portfólio ao fim do piloto e trimestralmente depois. Toda decisão deve registrar evidência, responsável, prazo, hipótese afetada e próximo teste.

## Riscos e respostas

| Risco | Sinal de alerta | Resposta planejada |
|:---|:---|:---|
| Baseline não comparável | Divergência de denominador ou coorte | Congelar comunicação de meta, revisar fórmula e aprovar nova linha de base |
| Dados incompletos ou fragmentados | Campos ausentes, atraso ou reconciliação baixa | Priorizar dataset mínimo, registrar lacunas e não extrapolar efeito |
| Contato sem mudança de comportamento | Alta cobertura e churn inalterado | Analisar qualidade e timing, ajustar intervenção ou interromper |
| Pressão por desconto | Conversão sobe com margem ou inadimplência pior | Exigir leitura de custo, receita líquida e permanência antes de escalar |
| Sobrecarga de atendimento | SLA cai ou reclamações aumentam | Limitar coorte, ajustar capacidade e criar fila de exceção |
| Uso indevido de dados | Acesso sem finalidade ou consentimento inadequado | Restringir acesso, revisar governança e suspender uso não autorizado |
| Dependência de sistema legado | Integração bloqueia o cronograma | Usar extração controlada, documentar dívida e replanejar o gate |

## Gates: continuar, ajustar, pausar ou parar

- **Continuar:** baseline validado, execução dentro do SLA, qualidade suficiente, custo conhecido e sinal de efeito compatível com a hipótese.
- **Ajustar:** execução possível, mas qualidade, experiência, custo ou segmentação exigem correção antes de ampliar.
- **Pausar:** dependência crítica, risco de conformidade ou capacidade insuficiente impede teste responsável.
- **Parar:** hipótese não se sustenta após teste, o custo supera o benefício esperado, ou há dano não aceitável à experiência e à equidade.

Nenhum gate deve ser decidido apenas pelo dashboard: o comitê precisa revisar fonte, fórmula, população, incertezas e registro operacional.

## Limitações e próximos passos

Este case usa uma base sintética verificável, não dados reais. Ainda não há série histórica auditável de operação, custos de intervenção, margem por curso, consentimentos, análise causal, risco validado ou resultado realizado. O snapshot de 2025 não deve ser apresentado como baseline de 2027; a conversão de 20% é condicional; cobertura de indicadores de 95% é meta operacional a apurar.

Próximos passos: executar a geração e os testes, registrar a reconciliação e a validação de regras da base; depois, em etapas futuras, desenvolver análise diagnóstica SQL, dashboard, modelo, piloto e avaliação de efeito/custo. O gate de escala segue condicionado a evidência de negócio.

## Referências do portfólio

- [Portfólio de Gestão Estratégica](../../../../README.md)
- [Documento-base fictício da GENA](../../README.md)
- [Apresentação executiva](../../visao-executiva.md)
- [Detalhamento: redução de churn EAD](../retencao-ead/README.md)
- [Governança de indicadores e BI](../governanca-indicadores/README.md)
- [Templates do portfólio](../../../../templates/README.md)
- [Base sintética GENA](../retencao-ead/dados/README.md) · [Contrato](../retencao-ead/docs/contrato-dados.md) · [Validação](../retencao-ead/dados/validacao.md) · [Gerador](../retencao-ead/scripts/gerar_dados_gena.py) · [Testes](../retencao-ead/tests/test_dados_gena.py)


## Simulação retrospectiva de COVID-19

O [cenário de resposta estratégica à COVID-19](docs/simulacao-resposta-covid19.md) aplica a tese de continuidade, priorização, liquidez e governança a uma crise fictícia de 2020. A cronologia respeita o início do EAD em 2019, a resposta remota em 2020 e o CRM/painéis a partir de 2022. Etapas, orçamento e resultados são hipóteses didáticas; não alteram o plano 2027–2029 nem representam decisões ou impacto realizados.
