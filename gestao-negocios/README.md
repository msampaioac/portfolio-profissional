# Portfólio de Gestão e Negócios

Este portfólio conecta **Dados, Estratégia e Execução**. Os trabalhos são organizados por empresa e, dentro de cada empresa, por projeto. Esta página documenta o escopo geral, o conteúdo das pastas e a evolução prevista.

[LinkedIn e contato](https://linkedin.com/in/msampaioac) · [Portfólio unificado](../README.md) · [Análise de Dados](../analise-dados/README.md)

> Os cases atuais utilizam empresas e dados fictícios, com documentação estruturada com apoio de IA. Entregas técnicas, propostas, metas e resultados realizados são identificados separadamente. Não há declaração de clientes atendidos ou impacto profissional obtido.

## 1. Como o portfólio está organizado

```text
gestao-negocios/
├── README.md                         Guia geral do portfólio
├── cases/
│   ├── README.md                     Índice das empresas
│   └── gena/
│       ├── README.md                 Apresentação e contexto da empresa
│       ├── visao-executiva.md         Síntese dos projetos da GENA
│       └── projetos/
│           ├── planejamento-estrategico/
│           │   └── README.md         Diagnóstico, prioridades e OKRs
│           ├── governanca-indicadores/
│           │   ├── README.md         Problema, decisões e evidências
│           │   ├── docs/             Contrato, fontes, modelo e defesa do case
│           │   ├── evidencias/       Comparação e reconciliação executada
│           │   ├── scripts/          Cálculo reproduzível dos indicadores
│           │   └── tests/            Controles do ciclo de governança
│           └── retencao-ead/
│               ├── README.md         Problema, escopo e entregas do projeto
│               ├── dados/            CSV, configuração, dicionário e conferência
│               ├── docs/             Contrato de dados e registro de mudanças
│               ├── scripts/          Geração e validação da base fictícia
│               └── tests/            Testes automatizados
└── templates/
    └── README.md                     Modelos genéricos de gestão
```

**Regra principal:** a raiz explica o portfólio; a pasta da empresa explica o negócio; a pasta do projeto contém seu trabalho. Dados, scripts, testes e documentos específicos não ficam soltos na raiz nem misturados entre empresas.

Os [modelos genéricos](templates/README.md) são a única biblioteca compartilhada: diagnóstico, OKRs, canvas, 5W2H, riscos, decisões e checklist de governança. Modelos preenchidos devem ficar no projeto que os utiliza.

## 2. Empresas do portfólio

| Empresa | Contexto | Onde começar |
|:---|:---|:---|
| **GENA — Grupo Educacional Nascente do Acre** | Grupo educacional fictício; estratégia, permanência e gestão por indicadores | [Apresentação da empresa](cases/gena/README.md) ou [visão executiva](cases/gena/visao-executiva.md) |

Novas empresas serão incluídas em `cases/<empresa>/`, cada uma com sua própria apresentação e seus projetos. Não serão criadas pastas vazias apenas para sugerir experiência inexistente.

## 3. Trabalhos disponíveis e estágio atual

| Empresa / projeto | O que está disponível | O que ainda precisa ser desenvolvido |
|:---|:---|:---|
| GENA / [Planejamento estratégico](cases/gena/projetos/planejamento-estrategico/README.md) | Diagnóstico, SWOT, objetivos, OKRs propostos, prioridades, riscos e roteiro de execução | Aplicação operacional e acompanhamento dos resultados |
| GENA / [Retenção EAD](cases/gena/projetos/retencao-ead/README.md) | Plano do projeto, seis CSV fictícios, gerador Python, dicionário, reconciliação e 13 testes | Análise diagnóstica, SQL, painel, segmentação validada e avaliação do piloto |
| GENA / [Governança de indicadores](cases/gena/projetos/governanca-indicadores/README.md) | Inventário, modelo lógico, contrato, decisões, comparação de denominadores, cinco indicadores recalculados, script, testes próprios e defesa do case | Implantação e homologação operacional; conversão ainda preliminar e sem dados de funil |

As frentes **Jornada Ensino Médio → Graduação** e **Adimplência e Finanças** constam do planejamento da GENA, mas ainda não possuem projetos completos. Seus artefatos serão criados somente quando houver trabalho efetivo a documentar.

## 4. O que será trabalhado nos projetos

| Frente de trabalho | Entregas a desenvolver conforme o escopo |
|:---|:---|
| Diagnóstico e estratégia | Problema de negócio, evidências, hipóteses, alternativas e priorização |
| Gestão de projetos | Objetivos, escopo, responsáveis, backlog, cronograma, riscos e critérios de aceite |
| Dados e análise | Contrato de dados, fontes, tratamento, testes, consultas e análise reproduzível |
| BI e comunicação executiva | Indicadores, visualizações e recomendações vinculadas a decisões |
| Execução e avaliação | Plano de ação, rotina de acompanhamento, custos e avaliação de benefícios, quando houver evidência |

Cada projeto deve explicar **problema → diagnóstico → decisão → execução → medição**, distinguindo o que foi entregue do que continua planejado. Não é obrigatório usar todas as ferramentas ou todos os frameworks em cada trabalho.

## 5. Próxima etapa e sequência de evolução

O próximo trabalho é a **análise diagnóstica da base fictícia de Retenção EAD**. A sequência prevista é:

1. Explorar a base, implementar consultas e registrar limites da simulação.
2. Traduzir os achados em hipóteses e alternativas de gestão, sem afirmar causalidade.
3. Desenvolver um painel e uma síntese executiva com métricas consistentes.
4. Detalhar os instrumentos de execução do projeto e o desenho de avaliação do piloto.
5. Avaliar efeitos e viabilidade econômica somente quando existirem dados e método apropriados.

Essa sequência é um roteiro de desenvolvimento, não uma lista de entregas já concluídas. Não há modelo preditivo treinado, piloto executado, redução comprovada de churn ou ROI realizado.

## 6. Regras de manutenção

A apresentação de cada empresa é a referência do seu universo de negócio. A configuração da base é a fonte dos parâmetros sintéticos, e mudanças devem atualizar **dados, testes, documentação e índices em lote**.

Após alterações de pastas, verificar os links e executar novamente os comandos do projeto. Em Retenção EAD, os comandos são rodados dentro de `gestao-negocios/cases/gena/projetos/retencao-ead/`; o [guia da base](cases/gena/projetos/retencao-ead/dados/README.md) explica a reprodução.

## Contato

[LinkedIn](https://linkedin.com/in/msampaioac) para conversar sobre Gestão e Negócios, Estratégia e Business Intelligence.


## Simulação transversal COVID-19

A GENA agora possui uma simulação retrospectiva documentada dentro dos três projetos existentes — planejamento, retenção EAD e governança de indicadores. Ela não cria um quarto projeto nem substitui o próximo trabalho de análise da base EAD; os resultados de crise são didáticos, separados dos dados de 2025 e não representam execução ou impacto real. O ponto de entrada é a [apresentação da GENA](cases/gena/README.md).
