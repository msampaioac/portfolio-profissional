# Governança de indicadores para decisões consistentes

**Case de portfólio · GENA · Dados, Estratégia e Projetos**

[Portfólio](../../../../README.md) · [Empresa GENA](../../README.md) · [Defesa do case](docs/defesa-do-case.md) · [Evidência reproduzível](evidencias/reconciliacao.md)

> Estudo fictício desenvolvido com apoio de IA na documentação e no código. Há execução técnica reproduzível sobre dados sintéticos; não há implantação empresarial, aprovação de uma equipe real ou impacto de retenção medido.

## 1. O problema e a decisão

Dois relatórios podem usar os mesmos cancelamentos e chegar a taxas diferentes porque contam populações distintas. A liderança passa a discutir o número, quando deveria decidir qual problema enfrentar e qual ação priorizar.

**Minha proposta neste estudo:** definir a população antes do painel, demonstrar a divergência, registrar a decisão metodológica e verificar o cálculo com testes. A contribuição apresentada é conectar especificação de dados, responsabilidade e decisão de gestão.

**Resultado técnico do exemplo:** a leitura inadequada de **24,68%** passa a **27,50%** ao substituir a fotografia final de ativos pela população elegível da abertura. A diferença de **2,82 pontos percentuais** é uma correção de definição — não aumento de evasão, efeito de intervenção ou descoberta sobre uma empresa real.

## 2. Contribuição apresentada e escolhas do estudo

| Escolha metodológica | Por que adotei nesta proposta | Onde o avaliador verifica |
|:---|:---|:---|
| Usar coorte e exclusões explícitas | Não confundir abandono com conclusão regular, transferência ou fotografia de ativos | [Contrato dos indicadores](docs/dicionario-indicadores.md) |
| Reutilizar a base existente | Preservar o cenário da GENA, evitar versões divergentes e permitir auditoria | [Inventário de fontes](docs/inventario-fontes.md) e [modelo lógico](docs/modelo-logico.md) |
| Tornar a correção reproduzível | Mostrar uma entrega verificável, não apenas uma recomendação | [Comparação](evidencias/comparacao-churn.csv), [script](scripts/reconciliar_indicadores.py) e [testes](tests/test_reconciliacao.py) |
| Separar governança de intervenção | Testar uma fórmula não autoriza atendimento a alunos nem comprova retenção | [Decisões do estudo](docs/registro-decisoes.md) e [plano de implantação](docs/plano-implantacao.md) |

Essas escolhas descrevem o estudo apresentado, não uma experiência de liderança na GENA. O apoio de IA é identificado; a evidência é o artefato auditável, não uma alegação de código escrito exclusivamente à mão ou validação pessoal não registrada.

## 3. Ciclo de governança demonstrado

| Etapa | Entrega efetiva | Evidência |
|:---|:---|:---|
| **Identificar a divergência** | Construir deliberadamente duas leituras do mesmo conjunto de cancelamentos | [Comparação de churn](evidencias/comparacao-churn.csv) |
| **Explicar a causa** | Diferenciar os 3.120 ativos finais dos 2.800 elegíveis da abertura | [Regra de população](docs/dicionario-indicadores.md) |
| **Escolher e registrar a regra** | Usar a coorte elegível e preservar as exclusões na reconciliação | [Decisão D001](docs/registro-decisoes.md) |
| **Recalcular e verificar** | Conferir fontes, fórmulas, complementaridade e reprodução | [Relatório executado](evidencias/reconciliacao.md) e [resultado estruturado](evidencias/resultado-reconciliacao.json) |

A divergência foi introduzida como cenário didático, não encontrada em relatórios de uma operação real. Nenhum CSV de origem foi alterado. O cenário continua com 2.880 matrículas na abertura, 40 conclusões, 40 transferências, 770 cancelamentos, 2.030 retidos, 1.090 ingressantes e 3.120 ativos finais.

## 4. Cobertura e estágio das entregas

| Entrega | Situação | Limite |
|:---|:---|:---|
| Inventário, modelo lógico e contrato | Documentados em arquivos próprios | Representam as fontes sintéticas existentes, não sistemas de uma instituição |
| Churn e retenção EAD | Recalculados no ciclo técnico | Coorte de abertura; exclusões retrospectivas; 27,5% e 72,5% |
| Adimplência e inadimplência monetárias | Recalculadas no ciclo técnico | Posição em 31/12/2025; 86,5% e 13,5%; não média mensal |
| NPS EAD | Recalculado no ciclo técnico | 39 pontos em 200 respostas calibradas, sem inferência populacional |
| Conversão Médio → Graduação | **Especificação preliminar** | Sem fonte de funil, cálculo, baseline ou meta |
| RACI, controles e marcos de implantação | Propostos | Não equivalem a aprovação empresarial ou governança operacional |
| Painel e piloto de retenção | Futuros, em etapas próprias | Dependem de homologação, dados autorizados, capacidade e desenho de avaliação |

O [dicionário](docs/dicionario-indicadores.md) distingue os **cinco indicadores demonstrados** da especificação preliminar de conversão. Os pares acadêmico e financeiro são complementares, não medidas independentes.

## 5. Governança: quem executa, quem valida e quem decide

| Papel proposto | Responsabilidade | Evidência exigida em uma implantação |
|:---|:---|:---|
| **Direção** | Aprovar objetivo, prioridades, recursos e avanço do piloto | Decisão e condições de avanço registradas |
| **Coordenação — Estratégia, Projetos e Dados** | Organizar entregas e formalizar o contrato após validação das áreas | Plano de trabalho, versão, pendências, responsáveis e prazos |
| **Negócio — responsável pelo dado** | Validar significado, população e exceções conforme o indicador | Definição e exceções justificadas pela área |
| **BI — equipe técnica** | Implementar, conciliar e testar, sem alterar a regra de negócio sozinho | Cálculo reproduzível e falhas documentadas |

A RACI detalhada, com um único aprovador por atividade, está em [governança proposta](docs/governanca-proposta.md). Validação do negócio e aprovação formal são responsabilidades distintas; o estudo não simula assinaturas ou aprovações humanas como fatos ocorridos.

## 6. Implantação e critérios de avanço

O plano separa **contrato → qualidade contínua → homologação executiva → eventual piloto de retenção**. Cada marco tem executor, aprovador, dependência e critério de aceite no [plano de implantação](docs/plano-implantacao.md).

Não há compromisso artificial de implantar tudo em 90 dias. Prazos e esforço dependem de acesso às fontes, capacidade das áreas e recursos aprovados. Uma revisão de trabalho enxuta trata as falhas; a Direção é acionada para alterações materiais de regra, risco, prioridade ou investimento.

Repetir este script prova reprodução sobre os mesmos dados, não qualidade de duas cargas operacionais distintas. Conversão permanece fora do aceite técnico do MVP de cinco indicadores.

## 7. Como reproduzir e examinar os controles

A partir da raiz do repositório, com Python 3.10 ou superior, sem bibliotecas externas:

```bash
cd cases/gena/projetos/governanca-indicadores
python3 scripts/reconciliar_indicadores.py
python3 -m unittest discover -s tests -v
```

O projeto lê a base de [Retenção EAD](../retencao-ead/dados/README.md). Os **13 testes daquele projeto** verificam seu contrato de geração. A [suíte própria de governança](tests/test_reconciliacao.py) e o [relatório](evidencias/reconciliacao.md) mostram os controles deste ciclo, sem atribuir a esses testes homologação empresarial, validação de conversão ou efeito causal.

## 8. Perguntas de entrevista respondidas

A [defesa do case](docs/defesa-do-case.md) responde: por que usar essas exclusões, como investigar divergências, quem pode mudar uma fórmula, quais controles priorizar, o que os testes demonstram e como o apoio de IA foi utilizado.

**Síntese da minha abordagem:** apresentar uma decisão sustentada por definição, evidência e limite de interpretação. A maturidade do estudo está em tornar a escolha verificável e saber o que ainda depende de fonte, validação ou implantação.
