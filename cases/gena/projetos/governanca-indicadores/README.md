# Governança de indicadores para decisões consistentes

> **Case complementar de portfólio — proposta simulada em Gestão Estratégica, Projetos e BI.** A primeira melhoria já define uma base sintética verificável para exame e reconciliação; este case não apresenta análise causal, risco validado ou implementação de negócio.

## 1. Contexto e desafio

O GENA é um grupo educacional fictício fundado em 2004, com Educação Básica, graduação presencial e EAD, pós-graduação e extensão. Em 2025, os relatórios de matrícula, financeiro, atendimento e experiência apresentariam visões divergentes por usarem filtros, períodos, status e denominadores diferentes.

A divergência mais crítica seria a pergunta “a evasão está subindo?”: uma planilha poderia contar cancelamentos, outra comparar fotografias de alunos ativos e uma terceira excluir transferências sem documentar a regra. O efeito é uma decisão sem população comparável, difícil de auditar e sujeita a priorizar a intervenção errada.

O desenho proposto cria uma camada semântica mínima antes de qualquer dashboard: cada indicador terá definição, fórmula, granularidade, data de referência, fonte, responsável, exceções e trilha de alteração.

### Fato simulado e limite de evidência

- O **churn anual de 27,5% na graduação EAD** é reproduzido na base sintética a partir de 2.880 na abertura, 40 conclusões, 40 transferências, 2.800 elegíveis e 770 cancelamentos; continua sendo referência calibrada, não fato operacional.
- A reconciliação verifica regras e totais sintéticos; não é validação real, análise causal nem validação de risco.
- O snapshot de 2025 não substitui uma linha de base atualizada para o ciclo estratégico de 2027–2029.
- Qualquer meta de melhoria depende de baseline a apurar, janela, coorte, custo e elegibilidade aprovados.

### Base disponível para exame

O contrato da primeira melhoria está no [índice da base](../retencao-ead/dados/README.md), na [especificação](../retencao-ead/docs/contrato-dados.md) e na [validação/reconciliação](../retencao-ead/dados/validacao.md). O gerador está referenciado em [`scripts/gerar_dados_gena.py`](../retencao-ead/scripts/gerar_dados_gena.py) e os testes em [`tests/test_dados_gena.py`](../retencao-ead/tests/test_dados_gena.py); não se antecipa que todos os testes passaram antes da execução correspondente.

A convenção inclui 2.030 retidos (72,5%), 1.090 ingressantes ativos de março a novembro sem churn estimado no grupo, 3.120 no fechamento e 3.970 indivíduos distintos no ano. NPS 39 usa 200 respostas (118/42/40). Inadimplência significa **monetária na posição de referência**; no EAD, 13,5% é alvo de calibração em títulos vencidos até 31/12/2025, não validação real.

No corte de features em 28/02/2025, financeiro, NPS e saídas de abril a dezembro de 2025 não entram; os sinais de oito semanas (06/01–28/02), gerados a partir da abertura de 2.880, são independentes do desfecho. Administração, Pedagogia e Gestão Pública nos polos Cidade Nova, Cruzeiro do Sul e Sena Madureira são premissas didáticas, não autorização para inferência.


## 2. Decisão de negócio e objetivos

### Decisão a apoiar

A liderança precisa decidir **quais segmentos, coortes e ações priorizar** para permanência, continuidade da jornada e saúde financeira, sem misturar alunos, matrículas, títulos e respostas de pesquisa em uma mesma taxa.

### Objetivos do desenho

1. Harmonizar seis indicadores executivos com um contrato de métrica único.
2. Explicar, com rastreabilidade, por que dois relatórios divergem.
3. Separar fato observado, hipótese, projeção e meta.
4. Criar uma rotina de decisão com responsáveis e critérios de aceite.
5. Preparar uma linha de base a apurar, sem inventar resultados de melhoria.

### Por que este método

- **Semântica antes da visualização:** uma definição aprovada evita que filtros sejam reescritos em cada planilha.
- **População e grão explícitos:** o denominador revela se a taxa é de aluno, matrícula, título, valor ou resposta.
- **Snapshot e coorte:** preservam a fotografia temporal e impedem comparar períodos incompatíveis.
- **Rastreabilidade por exceção:** registros fora da regra não desaparecem; recebem motivo e fila de tratamento.
- **Decisão orientada a evidência:** o painel é um meio para registrar ação, dono, prazo e revisão, não o produto final isolado.

## 3. Escopo da proposta

### Incluído

- Contrato dos seis indicadores deste case e seus campos mínimos.
- Inventário de relatórios de matrícula, financeiro, CRM, atendimento e pesquisa.
- Matriz de divergência e reconciliação para o snapshot de 2025.
- Modelo lógico por aluno, matrícula, título e resposta, com IDs sintéticos.
- Regras de qualidade, tratamento de falhas, RACI e rotina de governança.
- Roteiro de validação sem dashboard; a análise diagnóstica SQL e o painel executivo ficam para etapa futura.

### Não incluído

- Implementação de ETL, data warehouse, CRM ou painel produtivo.
- Análise diagnóstica SQL, teste estatístico, diagnóstico causal ou validação de risco.
- Reprocessamento de uma série histórica real ou validação externa do cenário.
- Definição de preço, concessão de bolsa, cobrança automática ou contato com aluno.
- Decisão jurídica sobre base legal, retenção de dados ou compartilhamento.
- Promessa de redução de churn, aumento de NPS ou recuperação financeira.

## 4. Mini dicionário de seis indicadores

> As fórmulas abaixo são propostas de especificação. Cada resultado real exigirá fonte, janela, versão da regra e baseline apurado.

| Indicador | Fórmula proposta e regra de população | Granularidade e leitura |
|:---|:---|:---|
| **Churn anual** | `100 × saídas por cancelamento/evasão/abandono ÷ população elegível`. População elegível: IDs de matrícula ativos na abertura, sem status concluído ou transferido. Para manter o par complementar, IDs que se tornarem concluídos/transferidos na janela são retirados da população e reportados em “fora do escopo”; só cancelamento/evasão/abandono entra no numerador. | Matrícula-aluno × coorte × período, com cortes por segmento, modalidade, curso e polo. Mede perda entre elegíveis, não a soma de fotos anuais. |
| **Retenção anual** | `100 × elegíveis ativos ao final ÷ população elegível`. Usa a mesma coorte e exclusões do churn. As regras são fixadas antes do cálculo; conclusões/transferências da janela são conciliadas separadamente. Retenção + churn = 100% somente quando todos os elegíveis terminam classificados em um dos dois estados. | Matrícula-aluno × coorte × período. Não misturar retenção de cursos curtos com graduação sem regra de renovação equivalente. |
| **Adimplência monetária** | `100 × valor liquidado até a data de referência ÷ valor monetário dos títulos maturados`. Denominador: soma do valor devido líquido de títulos com vencimento alcançado na data (`vencimento ≤ snapshot`), excluídos cancelados e substituídos. O valor pago é alocado aos títulos pela regra financeira aprovada. | Título × snapshot, agregado por segmento, curso, polo e faixa de atraso. Maturação significa que o vencimento já ocorreu; títulos futuros não entram. |
| **Inadimplência monetária na posição de referência** | `100 × saldo aberto dos títulos maturados ÷ valor monetário dos títulos maturados`. Tem o mesmo denominador da adimplência; portanto, no snapshot e após conciliação, os dois percentuais são complementares. Atraso, acordo e baixa parcial devem ser classificados antes do cálculo. | Título × snapshot × faixa de aging. Não usar quantidade de títulos no denominador desta versão e não misturar valor faturado futuro. O 13,5% EAD é calibração sintética de títulos vencidos em 31/12/2025, não validação real. |
| **NPS** | `% promotores (notas 9–10) − % detratores (notas 0–6)`, entre respostas válidas; notas 7–8 são passivas. Escala de **−100 a 100**, não percentual de satisfação. | Resposta × pesquisa × período, com cortes por segmento, modalidade, curso e polo quando houver amostra. Taxa de resposta e tamanho da amostra acompanham o índice. |
| **Conversão** | `100 × matrículas confirmadas ÷ concluintes elegíveis ou leads qualificados`, conforme funil aprovado. O evento, a janela e a população do denominador devem ser iguais entre etapas; não há baseline disponível neste case. | Pessoa/lead × etapa do funil × coorte de entrada. Exibir volume em cada etapa, conversão por etapa e origem; só definir meta após apurar a linha de base. |

### Regras comuns de comparação

- Toda visualização exibirá `snapshot`, período de competência, população, grão e versão do dicionário.
- “Aluno ativo”, “matrícula”, “concluído”, “transferido”, “cancelado” e “título maturado” terão códigos de origem mapeados.
- Um indicador não será comparado entre segmentos se a janela acadêmica ou a regra de renovação não for equivalente.
- A fotografia de 2025 será tratada como referência simulada do case, nunca como evidência de dataset validado.

## 5. Arquitetura de governança proposta

### Papéis

- **Patrocinador/Direção:** arbitra prioridade, risco e investimento; aprova decisões de negócio.
- **Dono do produto — Escritório de Estratégia, Projetos e Dados:** mantém backlog, contrato de métricas e calendário.
- **Data Steward — Acadêmico/Financeiro:** conhece o processo de origem, valida significado e exceções.
- **BI/Engenharia de Dados:** modela, reconcilia, testa e publica evidências técnicas, sem aprovar regra de negócio sozinho.

### RACI por atividade

| Atividade | Patrocinador/Direção | Dono do produto | Data Steward | BI/Engenharia |
|:---|:---:|:---:|:---:|:---:|
| Aprovar objetivo e decisão apoiada | A | R | C | I |
| Aprovar contrato dos seis indicadores | C | A | R | C |
| Mapear fontes, campos e status | I | A | R | R |
| Definir população, fórmula e grão | C | A | R | C |
| Construir modelo lógico e reconciliação | I | A | C | R |
| Registrar e classificar falhas de qualidade | I | A | R | R |
| Homologar protótipo de painel | A | R | C | R |
| Conduzir ritual de decisão | A | R | C | I |
| Aceitar entrada em piloto | A | R | C | C |
| Revisar regra ou alterar versão | A | R | C | C |

**R:** responsável pela execução; **A:** aprovador que responde pela atividade; **C:** consultado; **I:** informado. Cada atividade tem **um único A**. Responsáveis e consultados podem ser mais de um; informado não aprova nem altera a regra.

## 6. Qualidade, tratamento e falhas

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

## 7. Plano de 30/60/90 dias

| Horizonte | Entregas propostas | Gate de decisão |
|:---|:---|:---|
| **0–30 dias** | Inventário de relatórios; mapa de divergências; contrato dos seis indicadores; RACI; população e grão; baseline a apurar; snapshot 2025 como referência simulada. | Donos aprovam 6/6 definições, fontes e exceções; regras para atualizar a linha de base ficam documentadas. |
| **31–60 dias** | Análise diagnóstica SQL futura; mapeamento de status, consultas de qualidade, reconciliação de uma carga e log de decisões. | Casos de teste têm resultado esperado documentado; divergências têm classificação e responsável. |
| **61–90 dias** | Dashboard, piloto controlado, rituais, apuração de baseline e avaliação de efeito/custo, todos em etapa futura e condicionados ao aceite da base. | Critérios de entrada são revisados sem declarar melhoria de negócio; não são entregas desta primeira melhoria. |

## 8. Rotina de decisão e aceite

- **Quinzenal — Comitê de retenção:** revisar churn, retenção, engajamento e exceções por coorte; decidir priorizar, ajustar ou encerrar ações.
- **Mensal — Reunião de indicadores:** revisar qualidade, divergências, mudanças de regra e frescor; aprovar correções versionadas.
- **Mensal — Comitê estratégico:** usar evidência conciliada para decidir foco, capacidade, risco e investimento.
- **Trimestral — Revisão de portfólio:** comparar benefícios esperados com baseline apurado; manter, pausar ou replanejar iniciativas.

Toda ata registra evidência, snapshot, decisão, único responsável, prazo, risco, hipótese e critério de revisão. O aceite do desenho exige: **6/6 indicadores com owner, fórmula, grão e denominador aprovados; 100% dos painéis com snapshot e versão; 100% das divergências críticas com causa e dono; zero chave duplicada nos casos de teste; e duas execuções consecutivas sem falha crítica não tratada**. Esses são critérios de entrada em piloto, não resultados já alcançados.

## 9. Riscos e proteção de dados

| Risco | Resposta proposta | Limite |
|:---|:---|:---|
| Métricas aprovadas com fontes ainda incompletas | Gate de qualidade, fila de exceções e sinalização de defasagem | Não publicar taxa como fato validado |
| Pressão por meta antes do baseline | Separar baseline, meta e realizado no modelo e na ata | Nenhuma melhoria será inventada |
| Reidentificação por cortes pequenos | IDs sintéticos, agregação mínima e revisão de acesso | Limite estatístico a definir com responsável apropriado |
| Uso indevido de situação financeira | Acesso por necessidade, mascaramento e trilha de consulta | Não decidir automaticamente cobrança ou matrícula |
| Alteração silenciosa de fórmula | Versionamento, aprovação única e changelog | Regra antiga permanece auditável |

A proposta aplica minimização, controle de acesso, segregação de ambientes, registro de consultas e descarte conforme política interna a definir. A avaliação de privacidade, retenção, compartilhamento e demais requisitos deve ser feita com os responsáveis competentes; este case **não promete conformidade jurídica**.

## 10. Referências internas

- [Portfólio de Gestão Estratégica — índice](../../../../README.md)
- [Índice de cases](../../../README.md)
- [Grupo Educacional — índice](../planejamento-estrategico/README.md)
- [Empresa fictícia Grupo Educacional](../../README.md)
- [Templates do portfólio](../../../../templates/README.md)
- [Base sintética GENA](../retencao-ead/dados/README.md) · [Contrato](../retencao-ead/docs/contrato-dados.md) · [Validação](../retencao-ead/dados/validacao.md)

**Contribuição demonstrada:** especificação de métricas, responsabilidades e controles que tornam uma proposta de BI verificável antes de sua implementação.
