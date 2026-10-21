# Governança proposta — papéis, responsabilidades e controles

[Projeto](../README.md) · [Plano de implantação](plano-implantacao.md) · [Contrato](dicionario-indicadores.md)

O desenho abaixo é a referência de uma implantação proposta. O ciclo técnico demonstrado utiliza cinco indicadores da base fictícia; sua reconciliação não equivale a aprovação empresarial. Conversão permanece preliminar.

## 1. Governança: quem executa, quem valida e quem decide

**Objetivo:** evitar que a liderança tome decisões com indicadores calculados de formas diferentes. A proposta separa o conhecimento do negócio, a execução técnica, a coordenação do trabalho e a autoridade para decidir.

**Leitura rápida:** as áreas de negócio validam o significado dos dados; BI calcula e testa; a coordenação organiza e formaliza as entregas; a Direção decide prioridades, recursos e avanço do piloto.

> Os papéis abaixo são propostos para a empresa fictícia GENA. Não representam uma equipe contratada, governança implantada ou resultados obtidos. O painel e o piloto continuam sendo etapas futuras.

### 1.1. Papéis e entregas esperadas

| Papel proposto | Responsabilidade principal | Entrega que permite verificar o trabalho |
|:---|:---|:---|
| **Direção — patrocinador** | Define a decisão de negócio, resolve conflitos de prioridade e aprova investimento e avanço do piloto. | Decisão registrada, com prioridade, recursos autorizados e condições para avançar ou pausar. |
| **Coordenação — Escritório de Estratégia, Projetos e Dados** | Organiza entregas, responsáveis e prazos; formaliza o contrato dos indicadores após validação das áreas. Corresponde ao dono do produto neste desenho. | Plano de trabalho, definições aprovadas, registro de pendências e calendário de acompanhamento. |
| **Negócio — responsável pelo dado** | Acadêmico, Financeiro ou responsável pela pesquisa, conforme o indicador: explica a origem e valida população, fórmula e exceções. Corresponde ao papel de *Data Steward*. | Definição do indicador validada pela área, mapeamento de status e justificativa das exceções. |
| **BI — equipe técnica** | Organiza o modelo de dados, implementa os cálculos, confere os totais e registra falhas. Não aprova sozinho uma regra de negócio. | Cálculo reproduzível, relatório de conciliação e resultados dos testes de qualidade. |

**Limite de autoridade:** validação do negócio e aprovação formal são etapas distintas. A Coordenação não substitui o conhecimento das áreas; BI não altera uma fórmula para fazer um resultado parecer melhor; mudanças de regra são registradas e submetidas à aprovação indicada na matriz.

### 1.2. Como uma definição vira uma decisão

| Etapa | Como o trabalho acontece | Condição para avançar |
|:---|:---|:---|
| **1. Definir a pergunta** | A Coordenação organiza a necessidade e a Direção aprova o objetivo. | Está claro qual decisão será apoiada e qual é o escopo. |
| **2. Acordar a métrica** | Negócio valida população, fórmula, período e exceções; BI avalia a viabilidade; a Coordenação formaliza o contrato. | A definição e as fontes estão documentadas e aprovadas. |
| **3. Conferir o cálculo** | BI implementa e concilia; Negócio explica as exceções; a Coordenação acompanha a correção das falhas. | Divergências críticas têm causa e tratamento documentados; não se usa uma taxa não conciliada como base de decisão. |
| **4. Decidir e acompanhar** | A Coordenação apresenta evidências e alternativas; a Direção decide; cada ação recebe responsável, prazo e condição de revisão. | A decisão e sua justificativa ficam registradas. Painel e piloto só avançam após os critérios de aceite. |

### 1.3. Exemplo aplicado à retenção EAD

No cenário fictício, o churn de **27,5%** usa **770 cancelamentos entre 2.800 matrículas elegíveis**, e não os 3.120 alunos ativos da fotografia final.

Se dois relatórios usarem denominadores diferentes, **BI identifica e registra a divergência**, **Negócio verifica as exclusões e os status** e **a Coordenação encaminha a definição aprovada e a correção versionada**. A Direção recebe a evidência conciliada para decidir sobre a iniciativa de retenção. Até resolver a divergência, a taxa afetada não deve orientar a priorização.

Esse fluxo é uma proposta de controle. A base sintética permite conferir a regra, mas não comprova que a governança foi implantada ou que houve redução de evasão.

### 1.4. Matriz RACI — referência detalhada

A matriz complementa a leitura executiva: mostra quem participa de cada atividade e quem responde pela aprovação final.

| Letra | Significado | O que a pessoa ou área faz |
|:---:|:---|:---|
| **R** | Responsável por executar | Realiza o trabalho e prepara a entrega. |
| **A** | Aprovador e responsável final | Aceita a entrega e responde pela atividade. Há **um único A por linha**. |
| **C** | Consultado | Fornece conhecimento ou validação antes da decisão. |
| **I** | Informado | Recebe o resultado; não executa nem aprova essa atividade apenas por estar informado. |

Responsáveis pela execução podem ser mais de um. As colunas usam os mesmos quatro papéis da seção 1.1.

<details>
<summary><strong>Abrir a matriz RACI por atividade</strong></summary>

| Atividade | Direção | Coordenação | Negócio | BI |
|:---|:---:|:---:|:---:|:---:|
| Definir e aprovar o objetivo de negócio | A | R | C | I |
| Preparar, validar e formalizar o contrato dos indicadores do MVP | C | A | R | C |
| Mapear fontes, campos e status | I | A | R | R |
| Definir população, fórmula e nível de detalhe dos registros | C | A | R | C |
| Construir o modelo de dados e conciliar os totais | I | A | C | R |
| Registrar e classificar falhas de qualidade | I | A | R | R |
| Verificar e aprovar o protótipo de painel — etapa futura | A | R | C | R |
| Conduzir a reunião de decisão | A | R | C | I |
| Autorizar a entrada em piloto — etapa futura | A | R | C | C |
| Revisar a regra e aprovar nova versão | A | R | C | C |

</details>

### 1.5. Competências demonstradas nesta proposta

O desenho evidencia **coordenação entre áreas, delimitação de autoridade, critérios de aceite, tratamento de divergências e comunicação executiva**. A contribuição de gestão está em transformar o indicador em uma decisão rastreável, com responsável, prazo e regra de revisão — não apenas em produzir um painel.

## 2. Qualidade, tratamento e falhas

### Regras mínimas

1. Identificar alunos e matrículas por IDs sintéticos; bloquear nomes e documentos em camadas analíticas.
2. Registrar `source_system`, data de carga, snapshot, competência, versão da regra e horário da última atualização.
3. Rejeitar chaves nulas, duplicadas ou conflitantes em uma fila de exceção; não corrigir silenciosamente.
4. Mapear status desconhecido para “não classificado”, suspender a taxa afetada e abrir responsável e prazo.
5. Validar datas impossíveis, valores negativos sem justificativa e duplicação de títulos antes da agregação. Pagamento antecipado é permitido; não é falha apenas por ocorrer antes do vencimento.
6. Conciliar totais de origem e destino por contagem e valor; diferenças recebem causa, materialidade e aceite documentado.
7. Separar concluídos, transferidos, cancelados, evasão/abandono e ativos; nunca inferir status pela ausência de acesso.
8. Marcar campos ausentes, atrasados ou parcialmente carregados como qualidade insuficiente, não como zero.
9. Se a carga crítica falhar ou o snapshot estiver incompleto, manter o último painel identificado como “defasado” e escalar ao dono.
10. Permitir reprocessamento versionado e preservar a fotografia publicada, a consulta e o motivo da alteração.

## 3. Riscos e proteção de dados

| Risco | Resposta proposta | Limite |
|:---|:---|:---|
| Métricas aprovadas com fontes ainda incompletas | Gate de qualidade, fila de exceções e sinalização de defasagem | Não publicar taxa como fato validado |
| Pressão por meta antes do baseline | Separar baseline, meta e realizado no modelo e na ata | Nenhuma melhoria será inventada |
| Reidentificação por cortes pequenos | IDs sintéticos, agregação mínima e revisão de acesso | Limite estatístico a definir com responsável apropriado |
| Uso indevido de situação financeira | Acesso por necessidade, mascaramento e trilha de consulta | Não decidir automaticamente cobrança ou matrícula |
| Alteração silenciosa de fórmula | Versionamento, aprovação única e changelog | Regra antiga permanece auditável |

A proposta aplica minimização, controle de acesso, segregação de ambientes, registro de consultas e descarte conforme política interna a definir. A avaliação de privacidade, retenção, compartilhamento e demais requisitos deve ser feita com os responsáveis competentes; este case **não promete conformidade jurídica**.


Os campos de origem, carga, acesso e reprocessamento são requisitos para implantação; não se afirma que todos existem nos CSV. Controles efetivamente executados são identificados no [relatório](../evidencias/reconciliacao.md). A rotina de reuniões e os marcos foram separados no [plano de implantação](plano-implantacao.md).
