# Empresas do portfólio

Esta pasta reúne os **universos de negócio** utilizados nos estudos. Cada empresa tem sua apresentação e, dentro de `projetos/`, os trabalhos específicos realizados ou propostos.

[Voltar ao guia geral do portfólio](../README.md)

## Empresas disponíveis

| Empresa | Natureza | Conteúdo |
|:---|:---|:---|
| [GENA — Grupo Educacional Nascente do Acre](gena/README.md) | Empresa educacional fictícia | Contexto institucional e projetos de planejamento estratégico, retenção EAD e governança de indicadores |

## Padrão para novas empresas

```text
cases/<empresa>/
├── README.md             Empresa, contexto e índice dos projetos
└── projetos/
    └── <projeto>/
        ├── README.md     Problema, escopo, entregas e estágio
        └── ...           Dados, documentos e código necessários
```

Cada projeto guarda seus próprios artefatos. Criar novas subpastas somente quando houver conteúdo, mantendo claro o que é fictício, proposto, implementado ou medido.
