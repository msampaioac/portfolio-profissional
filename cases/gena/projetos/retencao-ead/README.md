# Redução de churn na graduação EAD

**Estudo simulado · Retenção e experiência do aluno, com base sintética para exame**

[Portfólio](../../../../README.md) · [Plano estratégico](../planejamento-estrategico/README.md) · [Empresa fictícia](../../README.md) · [Governança de indicadores](../governanca-indicadores/README.md) · [Base](dados/README.md) · [Contrato](docs/contrato-dados.md) · [Validação](dados/validacao.md)

> **Estágio:** a base sintética é verificável para exame e a primeira melhoria cobre gerador, testes e reconciliação; este case continua sendo desenho de projeto. Não há modelo treinado, piloto executado, análise causal, risco validado, efeito medido ou ROI. Os números são sintéticos/calibrados e diferentes de operação real.

## Artefatos deste projeto

| Pasta | Conteúdo |
|:---|:---|
| [dados/](dados/README.md) | Seis CSV, configuração, dicionário, manifesto e reconciliação |
| [docs/](docs/contrato-dados.md) | Contrato de dados e registro de mudanças |
| [scripts/](scripts/gerar_dados_gena.py) | Gerador reproduzível e validador |
| [tests/](tests/test_dados_gena.py) | Testes automatizados de integridade e reprodução |

Todos os artefatos específicos de Retenção EAD ficam nesta pasta. O contexto institucional está na apresentação da GENA; os outros projetos estão em pastas próprias.

## 1. A decisão de negócio

**Recomendação para etapa futura:** iniciar um piloto de atendimento preventivo em uma coorte EAD, com regras de risco simples e explicáveis, em vez de começar por um modelo preditivo complexo ou por descontos indiscriminados. Esta decisão não integra a primeira melhoria de base sintética.

Essa escolha reduz dependências técnicas, permite testar a capacidade de atendimento e exige que a instituição meça permanência e custo. O piloto não presume que atraso ou baixo acesso causam evasão; esses sinais orientam hipóteses a investigar.

## 2. Contexto e problema

| Indicador EAD no cenário de 2025 | Referência simulada | O que precisa ser investigado |
|:---|---:|:---|
| Alunos ativos | 3.120 | Fotografia de volume, não denominador automático de churn |
| Churn anual | 27,5% | Coortes, janela, motivos de saída e população elegível |
| Inadimplência monetária na posição de referência | 13,5% | Relação entre títulos maturados, dificuldades financeiras e continuidade |
| NPS | 39 | Motivos de insatisfação e pontos de atrito |

A empresa possui sinais acadêmicos, financeiros e de atendimento em sistemas distintos. O problema de gestão é organizar esses sinais para decidir **quem atender, como atender e como avaliar a intervenção**.

## Base disponível para exame

A etapa de preparação de dados entrega base sintética, gerador Python, testes e reconciliação — não dashboard, modelo, piloto, efeito ou ROI. A conciliação EAD usa 2.880 na abertura de 01/01/2025; 40 conclusões e 40 transferências são retiradas retroativamente, deixando 2.800 elegíveis. São 770 cancelamentos (27,5%), 2.030 retidos (72,5%) e 1.090 ingressantes de março a novembro, todos ativos no fechamento e sem churn estimado no grupo. O fechamento é 3.120, enquanto 3.970 é o total anual de indivíduos distintos.

NPS 39 é calibrado com 200 respostas finais (118 promotores, 42 passivos, 40 detratores). A inadimplência monetária na posição de referência é o saldo aberto equivalente a 13,5% do valor devido dos títulos de 2025 vencidos até 31/12/2025, com alvo arredondado em centavos; é calibração/checagem de coerência, não validação real. O ticket EAD de R$ 310 é uniforme por simplificação em parcelas válidas; valores inteiros em centavos não significam `alunos × ticket = receita/ROI`.

Para o corte de features em 28/02/2025, financeiro, NPS e saídas de abril a dezembro de 2025 não são utilizáveis; em particular, dezembro fica fora. O engajamento de oito semanas (06/01–28/02), gerado a partir dos 2.880 da abertura, é independente do desfecho; portanto, não existe conclusão de que baixo engajamento provoque churn. Administração, Pedagogia e Gestão Pública e os polos Cidade Nova, Cruzeiro do Sul e Sena Madureira são premissas didáticas, não autorização para inferência. Detalhes de entradas, saídas e contrato estão no [índice da base](dados/README.md), [contrato](docs/contrato-dados.md) e [validação](dados/validacao.md).


## 3. Objetivo e critério de sucesso

A meta anual ilustrativa é reduzir o churn em **15% relativos** na mesma população e janela: `27,5% × (1 − 0,15) = 23,375%`. A diferença é **4,125 pontos percentuais**. Não é uma meta alcançada nem uma previsão de resultado.

| Camada de avaliação | Critério proposto |
|:---|:---|
| Resultado de negócio | Churn anual com regras e população estáveis, acompanhado junto ao custo |
| Resultado do piloto | Permanência na janela observável, comparada entre grupos comparáveis |
| Execução | Cobertura de contato, tempo de atendimento e cumprimento das ações |
| Proteção da experiência | Reclamações, satisfação e ausência de abordagem excessiva |

**Limite temporal:** 90 dias permitem avaliar viabilidade e sinais de resultado, mas não comprovam uma redução anual. O efeito anual depende de acompanhamento posterior.

## 4. Escopo do projeto (etapa futura)

| Incluído no piloto | Fora do escopo inicial |
|:---|:---|
| Uma coorte e conjunto limitado de cursos/polos a selecionar | Expansão imediata para todos os alunos |
| Dados autorizados de matrícula, acesso, pagamento e atendimento | Coleta indiscriminada de dados pessoais |
| Regras simples de segmentação e revisão humana | Modelo preditivo apresentado como validado |
| Registro de intervenção e acompanhamento | Oferta automática de descontos ou cobrança agressiva |
| Avaliação de permanência, experiência e custo | Promessa de ROI ou receita recuperada sem medição |

## 5. Hipóteses e dados necessários

| Hipótese de planejamento | Evidência a buscar | Limitação |
|:---|:---|:---|
| Baixo engajamento inicial antecede parte das saídas | Acessos, atividades e datas de cancelamento | Acesso baixo pode refletir falha técnica, não desinteresse |
| Dificuldades financeiras elevam risco de abandono | Vencimentos, pagamentos, acordos e motivos de saída | Correlação não demonstra causalidade |
| Atendimento não resolvido deteriora a experiência | Solicitações, prazo, resolução e pesquisas | Pesquisas podem ter viés de resposta |
| Contato preventivo melhora a permanência | Grupo atendido, comparação e janela de observação | Diferenças de perfil podem distorcer a avaliação |

Essas hipóteses não foram testadas. A seleção dos sinais deve ocorrer após definição das métricas no [case de governança](../governanca-indicadores/README.md).

## 6. Segmentação proposta

| Sinal a validar | Tratamento sugerido | Decisão humana |
|:---|:---|:---|
| Baixa interação com o ambiente virtual | Verificar acesso, onboarding e dificuldades acadêmicas | Confirmar contexto antes de classificar risco |
| Pagamento em atraso | Orientar canais e condições autorizadas | Encaminhar ao financeiro, sem presumir desinteresse |
| Solicitação recorrente sem resolução | Priorizar resolução e retorno ao aluno | Acionar área responsável pelo problema |
| Múltiplos sinais simultâneos | Acompanhamento coordenado | Definir responsável único pela jornada |

Os limiares e a ordem de atendimento devem considerar qualidade dos registros, capacidade das equipes e disponibilidade do aluno. Não são regras de classificação já operacionais.

## 7. Backlog e roteiro de 90 dias

| Etapa | Entrega | Dependência | Critério para avançar |
|:---|:---|:---|:---|
| Dias 1–30: preparar | Escopo, coorte, métricas e diagnóstico de qualidade | Acadêmico, financeiro e BI | População elegível conciliada e problemas críticos tratados |
| Dias 31–60: testar | Segmentação, roteiro de atendimento e início controlado | Equipe capacitada e permissões revisadas | Intervenções registradas e capacidade de atendimento demonstrada |
| Dias 61–90: avaliar | Comparação, custos, riscos e recomendação ao comitê | Janela observável e registros completos | Decidir continuar, ajustar, pausar ou ampliar acompanhamento |

O dono do processo de retenção coordena a jornada; BI cuida das definições e análise; acadêmico e financeiro respondem por suas intervenções; o patrocinador decide escopo e recursos. Os responsáveis são **papéis propostos**, não pessoas contratadas para uma execução real.

## 8. Como avaliar sem atribuir um efeito indevido

Quando viável e apropriado, distribuir aleatoriamente alunos elegíveis entre intervenção e rotina usual, sem retirar suporte essencial. Caso isso não seja possível, utilizar comparação por coorte/perfil e explicitar o risco de viés.

Definir antes do início a janela, os desfechos, a população elegível, o tratamento de transferências e conclusões e o tamanho necessário para uma avaliação informativa. Não há tamanho amostral calculado nesta etapa.

| Pergunta | Medida proposta |
|:---|:---|
| O atendimento foi executado? | Contatados ÷ elegíveis priorizados, com registro por data e ação |
| Houve melhor permanência? | Diferença de taxas na mesma janela e em grupos comparáveis |
| O efeito sustenta a operação? | Custo de intervenção e margem incremental atribuível, se demonstrável |
| A experiência foi preservada? | Reclamações, satisfação e motivos de saída |

**Viabilidade econômica:** benefício líquido incremental = margem de contribuição incremental atribuível − custo incremental da intervenção. Não se deve substituir margem por receita bruta nem multiplicar alunos ativos por ticket e chamar isso de ROI.

## 9. Riscos e decisões de controle

| Risco | Resposta proposta |
|:---|:---|
| Métricas inconsistentes | Bloquear comparação até reconciliar população e janela |
| Equipe sem capacidade | Reduzir a coorte e limitar o volume de contatos |
| Ação invasiva ou repetitiva | Definir frequência, canais autorizados e revisão humana |
| Viés na comparação | Usar desenho de avaliação explícito e registrar limitações |
| Melhoria aparente por mudança de denominador | Congelar regras e versionar qualquer alteração |

**Continuar:** dados e operação são confiáveis, com janela suficiente para aprender. **Ajustar:** existem gargalos corrigíveis ou avaliação inconclusiva. **Pausar:** há risco de atendimento, dados críticos inválidos ou ausência de registros. **Escalar:** somente após evidência consistente de viabilidade e avaliação adequada de efeito e custos.

## 10. O que este case demonstra

Tradução de um indicador em decisão de projeto; delimitação de escopo; hipóteses testáveis; priorização de entregas; coordenação de áreas; avaliação de riscos e resultados sem prometer impacto não observado.

**Próximo trabalho:** análise diagnóstica da base sintética e consultas SQL. Gerador, testes e reconciliação já estão disponíveis e foram executados; devem ser reexecutados quando houver alterações. Dashboard, modelo, piloto e avaliação de efeito/custo permanecem etapas futuras.

[Modelos de gestão](../../../../templates/README.md) · [Índice dos cases](../../../README.md) · [Base sintética](dados/README.md) · [Gerador](scripts/gerar_dados_gena.py) · [Testes](tests/test_dados_gena.py) · [Voltar ao portfólio](../../../../README.md)
