# Portfólio Profissional — Dados, Estratégia e Projetos

Este portfólio reúne duas frentes complementares: **Análise de Dados e Business Intelligence** e **Gestão Estratégica e de Projetos**. O objetivo é tornar visível a conexão entre pergunta de negócio, evidência, decisão e execução.

[LinkedIn e contato](https://linkedin.com/in/msampaioac) · [Perfil no GitHub](https://github.com/msampaioac)

## Escolha a trilha de avaliação

| Portfólio | O que examinar | Acesso |
|:---|:---|:---|
| **Análise de Dados** | SQL, BigQuery, Python, modelagem analítica e Power BI em projetos com dados públicos | [analise-dados](analise-dados/README.md) |
| **Gestão Estratégica e de Projetos** | Diagnóstico, OKRs, priorização, riscos, responsabilidades e governança de indicadores | [gestao-estrategica-projetos](gestao-estrategica-projetos/README.md) |

## Trabalhos para conhecer primeiro

| Trabalho | Questão ou competência apresentada | Onde verificar |
|:---|:---|:---|
| COVID-19 Brasil Analytics | Estruturar perguntas, consultas e indicadores de análise territorial | [Projeto de dados](analise-dados/An%C3%A1lise%20Espacial%20e%20Temporal%20da%20COVID-19%20no%20Brasil/README.md) |
| Perfil dos Estudantes Brasileiros | Integrar dados educacionais, explorar a base e organizar consumo em BI | [Projeto de dados](analise-dados/Perfil%20dos%20Estudantes%20Brasileiros%20%282015-ano-corrente%29/README.md) |
| GENA — Planejamento Estratégico | Relacionar diagnóstico, prioridades, objetivos e iniciativas | [Planejamento](gestao-estrategica-projetos/cases/gena/projetos/planejamento-estrategico/README.md) |
| GENA — Governança de Indicadores | Explicar uma divergência, documentar a regra e verificar o cálculo | [Case e evidências](gestao-estrategica-projetos/cases/gena/projetos/governanca-indicadores/README.md) |

Os projetos de dados utilizam fontes públicas e documentam seus limites. Os cases da GENA utilizam empresa e dados fictícios. O apoio de IA, as entregas técnicas e as etapas futuras são identificados nos respectivos trabalhos; não se apresentam simulações como experiência com clientes ou impacto real.

## Organização

```text
portfolio-profissional/
├── README.md
├── analise-dados/
│   ├── README.md
│   └── projetos de análise e BI
└── gestao-estrategica-projetos/
    ├── README.md
    ├── cases/
    │   └── gena/
    │       └── projetos/
    │           ├── planejamento-estrategico/
    │           ├── governanca-indicadores/
    │           └── retencao-ead/
    └── templates/
```

A raiz apresenta o conjunto. Cada portfólio organiza sua trilha; em Gestão, cada empresa reúne seus próprios projetos. Dados, código, evidências e documentos específicos permanecem dentro do trabalho a que pertencem.

## Como avaliar as entregas

Para verificar a dimensão técnica, comece por um projeto de dados e examine suas fontes, consultas, modelos e limitações. Para verificar a dimensão de gestão, comece pela GENA e acompanhe a relação entre diagnóstico, decisão, responsáveis e critérios de avanço.

O [case de governança](gestao-estrategica-projetos/cases/gena/projetos/governanca-indicadores/README.md) inclui código e testes sobre a base fictícia. Sua execução demonstra consistência de definições, não redução de evasão. A [defesa do case](gestao-estrategica-projetos/cases/gena/projetos/governanca-indicadores/docs/defesa-do-case.md) explica as escolhas e seus limites.

## Manutenção e rastreabilidade

Este é o ponto de entrada único para evolução do portfólio. Os conteúdos e históricos dos dois repositórios de origem foram incorporados. Após auditoria e confirmação, os repositórios redundantes foram excluídos em 21/10/2026. Os históricos e snapshots finais estão preservados neste repositório; as duas pastas de trabalho permanecem intactas.

Mudanças devem atualizar documentos, links, índices e testes correspondentes em lote. Comandos de execução devem indicar se partem da raiz deste repositório ou da pasta de um projeto. A consolidação e suas origens estão registradas em [MIGRACAO.md](MIGRACAO.md).
