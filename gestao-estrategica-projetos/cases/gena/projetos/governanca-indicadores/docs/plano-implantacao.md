# Plano de implantação — marcos, dependências e decisões

[Projeto de governança](../README.md) · [Contrato de indicadores](dicionario-indicadores.md) · [Registro de decisões](registro-decisoes.md)

## 1. Entrega atual: ciclo técnico no estudo fictício

O MVP deste estudo utiliza a base sintética existente para demonstrar cinco indicadores e tratar uma divergência de denominador. Inventário, modelo lógico, contrato, código, testes e registro de decisão são artefatos do portfólio, não provas de aprovação ou implantação empresarial.

A [reconciliação](../evidencias/reconciliacao.md) registra os cálculos e os controles executados. Conversão está fora do cálculo; sua especificação preliminar não impede o aceite técnico deste MVP, mas impede declarar cobertura operacional completa dos seis indicadores.

## 2. Implantação operacional proposta, ainda não realizada

Em vez de prometer implantação e efeito de retenção em 90 dias, o plano utiliza **marcos condicionados a dependências**. Esforço, prazo e orçamento devem ser estimados com as áreas após o inventário operacional. O laboratório sintético não oferece base para inventar disponibilidade de equipes ou horas de trabalho.

| Marco | Responsável por executar / aprovar | Dependência | Critério para avançar |
|:---|:---|:---|:---|
| **M1 — Conhecer as fontes reais** | Negócio e BI executam; Coordenação aprova a entrega | Acesso autorizado, responsável por fonte e capacidade das áreas | Sistemas, campos, atualização, exceções e uso permitido identificados; inventário operacional aceito |
| **M2 — Validar o contrato do MVP** | Negócio valida; Coordenação formaliza | M1, ciclo de referência e população atualizados | Cinco indicadores com fonte, fórmula, população, janela, unidade e responsável definidos; comparação histórica e mudanças registradas |
| **M3 — Demonstrar qualidade contínua** | BI e Negócio executam; Coordenação aprova o aceite técnico | M2, rotinas de ingestão e capacidade de tratamento | Duas cargas operacionais consecutivas verificadas; falhas críticas com causa, responsável e tratamento; nenhuma comparação sem população conciliada |
| **M4 — Homologar comunicação executiva** | Coordenação e BI preparam; Direção aprova | M3 e uma decisão de negócio delimitada | Protótipo informa referência, versão e limitações; liderança compreende a decisão apoiada; aceite e pendências registrados |

Repetir o script sobre os mesmos CSV demonstra reprodução. **Não equivale a verificar duas cargas operacionais distintas** nem a atingir M3.

## 3. Antes de fixar um cronograma

| Item a apurar | Decisão necessária |
|:---|:---|
| Disponibilidade de Acadêmico, Financeiro e área de experiência | Indicar responsáveis e tempo disponível para validação |
| Acesso e atualização das fontes | Definir permissões, periodicidade e restrições |
| Volume e complexidade das exceções | Estimar esforço de tratamento e priorizar falhas que afetam decisão |
| Capacidade de BI e ferramentas existentes | Escolher forma de implantação e esforço técnico |
| Patrocínio e orçamento | Aprovar recursos e limites antes de assumir prazos |

O trabalho pode ser priorizado por entregas de maior risco sem aguardar um painel completo. População, denominador, unicidade e conciliação financeira precedem a expansão das visualizações.

## 4. Rotina enxuta de governança

| Situação | Fórum proposto | Encaminhamento |
|:---|:---|:---|
| Preparação e tratamento de falhas | Uma revisão de trabalho com Coordenação, Negócio e BI, inicialmente semanal e ajustável à necessidade | Evidência, pendência, responsável e prazo; evitar criar vários comitês para o mesmo problema |
| Mudança que afeta interpretação, prioridade, risco ou recursos | Direção, acionada pela Coordenação | Decisão e justificativa registradas; nenhuma mudança silenciosa de regra |
| Contrato estável e operação homologada | Cadência de revisão a pactuar com as áreas | Acompanhar qualidade, versão e uso dos indicadores; ajustar a frequência ao volume de mudanças |

Correção técnica que apenas restabeleça uma regra já aprovada é registrada e verificada. Alteração da definição exige análise do negócio e aprovação de nova versão; a mudança não apaga a regra ou a fotografia anterior.

## 5. Piloto de retenção: projeto dependente, não etapa concluída aqui

O [projeto de Retenção EAD](../../retencao-ead/README.md) define o desenho da intervenção. Sua entrada depende da governança homologada, dados com uso autorizado, equipe de atendimento, desenho de comparação e capacidade de medir experiência, permanência e custos.

O piloto de intervenção requer aprovação da Direção e critérios próprios. Não é iniciado automaticamente após executar os testes deste estudo. Uma janela curta pode informar viabilidade, mas não comprova redução anual de churn.

Conversão Médio → Graduação depende de outra fonte e de contrato de funil completo. Ela deve ser estimada e implementada como expansão controlada, não incorporada aos resultados já entregues.

## 6. Quando continuar, corrigir ou interromper

**Continuar:** definição e população estão estáveis, fontes estão disponíveis e as falhas críticas foram tratadas. **Corrigir:** há divergência explicável e reparável, com responsável e prazo. **Bloquear a taxa:** status desconhecido, denominador inválido, fonte incompleta ou soma não conciliada. **Replanejar:** a capacidade ou as permissões não sustentam o marco seguinte.

Os benefícios esperados são decisões comparáveis e maior rastreabilidade. Não há prazo de implantação cumprido, economia medida, ROI ou efeito de intervenção atribuído a este plano.
