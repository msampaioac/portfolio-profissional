# Portfólio de Gestão Estratégica e de Projetos

## Gestão Estratégica e de Projetos orientada por Dados

Meu foco profissional é conectar **análise de dados, prioridades de negócio e execução**: compreender o problema, definir indicadores, organizar iniciativas e estabelecer uma rotina de acompanhamento para apoiar decisões.

Este portfólio apresenta esse raciocínio aplicado ao setor educacional. O objetivo não é apenas mostrar ferramentas, mas explicar **qual decisão tomar, por que priorizá-la e como acompanhar sua execução**.

[LinkedIn e contato](https://linkedin.com/in/msampaioac) · [Portfólio técnico de Dados e BI](https://github.com/msampaioac/data-analytics-portfolio) · [GitHub](https://github.com/msampaioac)

> **Natureza dos trabalhos:** estudos autorais estruturados com apoio de IA sobre uma empresa fictícia. Há uma base sintética verificável para exame e reprodução; os artefatos não representam projetos implantados, clientes atendidos ou resultados profissionais realizados.

## Comece por aqui

**Leitura rápida:** [síntese executiva dos cases](docs/apresentacao-executiva.md). Veja o problema, a recomendação e a evidência disponível antes de abrir a documentação completa.

**Avaliação aprofundada:** escolha um dos três estudos abaixo. Todos compartilham o mesmo [universo de negócio — GENA](docs/empresa-ficticia-grupo-educacional.md), permitindo acompanhar a conexão entre estratégia, projetos e governança.

## Cases em destaque

| Estudo | Decisão de negócio | Evidências disponíveis |
|:---|:---|:---|
| **[Planejamento estratégico do GENA](cases/grupo-educacional/README.md)** | Como priorizar crescimento, retenção e transformação digital? | SWOT, objetivos, OKRs propostos, critérios de priorização, roteiro de 90 dias e riscos |
| **[Redução de churn no EAD](cases/grupo-educacional/reducao-churn-ead.md)** | Como agir antes do abandono sem prometer um efeito ainda não medido? | Hipóteses, [base sintética](dados/gena/README.md), [contrato de dados](docs/contrato-dados-gena.md) e [reconciliação e testes](dados/gena/validacao.md) |
| **[Governança de indicadores e BI](cases/governanca-indicadores-bi.md)** | Como fazer áreas diferentes decidirem com métricas comparáveis? | Dicionário de indicadores, RACI, controles de qualidade e critérios de aceite |

**Estágio:** planejamento documentado, com preparação de dados do case EAD executada em ambiente simulado. A implementação operacional, o dashboard, o modelo e o piloto continuam futuros; não há impacto ou ROI realizado.

## Evidência técnica disponível para exame

A [base fictícia da GENA](dados/gena/README.md) possui **seis CSV, gerador Python, dicionário e testes automatizados**. Os dados preservam os 3.120 ativos EAD finais e os 10.040 ativos institucionais, com entradas, saídas e população elegível documentadas.

A [reconciliação](dados/gena/validacao.md) permite conferir churn, retenção, posição financeira, NPS e hashes dos arquivos. Os números são calibrados para o cenário fictício: demonstram consistência e reprodutibilidade, não eficácia de uma intervenção.

Para examinar a implementação: [gerador](scripts/gerar_dados_gena.py) · [testes](tests/test_dados_gena.py) · [contrato e limites](docs/contrato-dados-gena.md).

## Competências demonstradas nos artefatos

| Frente | Como aparece no portfólio |
|:---|:---|
| Diagnóstico e estratégia | Relação entre contexto, restrições, hipóteses e escolhas |
| Gestão de projetos | Escopo, dependências, papéis, riscos e critérios para avançar ou interromper |
| Gestão por resultados | Separação entre objetivo, resultado-chave, indicador operacional e iniciativa |
| Business Intelligence e governança | Definições de métricas, granularidade, qualidade e rotina de decisão |
| Comunicação executiva | Síntese que conecta evidência, recomendação e decisão requerida |

A primeira melhoria usa **Python para geração e testes de contrato/reconciliação**; SQL, BigQuery e Power BI têm evidências técnicas no [portfólio de Análise de Dados](https://github.com/msampaioac/data-analytics-portfolio), outro repositório. Aqui, o foco é o **raciocínio de gestão que orienta a análise e a execução**. A análise diagnóstica em SQL e o dashboard Power BI são etapas futuras; não apresento modelo, piloto, efeito ou ROI implementados neste repositório.

## Como avaliar o meu raciocínio

Nos cases, procure a sequência **problema → diagnóstico → escolha → execução → medição**. As alternativas descartadas, as limitações dos dados e as condições para revisar uma decisão fazem parte da proposta, e não ficam escondidas no final.

Para discutir os trabalhos em entrevista, três perguntas ajudam a aprofundar a avaliação:

1. Por que priorizar governança e retenção antes de acelerar a expansão?
2. Como distinguir uma meta de negócio de uma entrega do projeto?
3. Que evidência justificaria continuar, ajustar ou interromper o piloto?

## Navegação do repositório

| Área | Conteúdo |
|:---|:---|
| [Cases](cases/README.md) | Estudos aplicados e roteiro de avaliação |
| [Documentação](docs/README.md) | Síntese executiva, empresa fictícia e estágio das entregas |
| [Base sintética GENA](dados/gena/README.md) | Contrato, CSV, gerador, testes e reconciliação da primeira melhoria |
| [Modelos de trabalho](templates/README.md) | Diagnóstico, OKRs, canvas, 5W2H, riscos e decisões |

## Contato profissional

Para conversar sobre oportunidades em **Gestão Estratégica, Gestão de Projetos e BI**, entre em contato pelo [LinkedIn](https://linkedin.com/in/msampaioac).

Este repositório demonstra propostas e formas de raciocínio. Experiência profissional, formação e trajetória devem ser consultadas no perfil do autor; não são inferidas dos dados da empresa fictícia.
