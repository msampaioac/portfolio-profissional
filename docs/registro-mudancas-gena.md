# Registro de mudanças — dados fictícios da GENA

[Portfólio](../README.md) · [Contrato de dados](contrato-dados-gena.md) · [Base sintética](../dados/gena/README.md)

## Versão 1.0.0 — 21/10/2026

Primeira materialização do cenário de 2025 em microdados de graduação EAD, com geração Python, configuração versionada, dicionário, testes e reconciliação. Todos os registros são fictícios e nenhum benefício de intervenção foi medido.

| Tema | Preservado ou atualizado |
|:---|:---|
| Identidade institucional | GENA, Nascente Educação, história, localidades e agenda estratégica preservadas |
| Alunos ativos finais de 2025 | 3.340 Básica + 2.560 presencial + 3.120 EAD + 1.020 pós/extensão = 10.040 |
| Fotografia EAD de 2024 | 2.880, usada como abertura de 2025 |
| Churn e retenção EAD | 27,5% e 72,5%, agora com população elegível explícita |
| Movimentos novos de modelagem | 40 conclusões, 40 transferências externas, 770 cancelamentos, 2.030 retidos e 1.090 ingressantes |
| Ticket EAD | R$ 310 por parcela; uniforme e sem descontos por simplificação |
| Indicador financeiro | 13,5% preservado; “média” sem definição substituída por posição monetária em 31/12/2025, sobre títulos vencidos de 2025 |
| NPS EAD | 39, calibrado em 200 respostas sintéticas; não pesquisa real |
| Oferta EAD da amostra | Administração, Pedagogia e Gestão Pública como premissa didática explícita |
| Engajamento | Oito janelas iniciais até 28/02, independentes dos desfechos de evasão |
| Outros segmentos | Apenas referências agregadas, não microdados |
| Estágio do portfólio | Preparação de dados disponível; piloto, dashboard, modelo e impacto continuam não realizados |

A atualização dos arquivos de dados e dos textos afetados é publicada em **um único commit**, evitando uma página que declare base inexistente enquanto outra já a utiliza.

## Regra para as próximas versões

Uma alteração deve informar a motivação, os parâmetros afetados, a migração das definições, o efeito nos indicadores e a compatibilidade com versões anteriores. Gerar os arquivos em pasta limpa, executar testes e recalcular a reconciliação antes de atualizar os documentos relacionados em conjunto.

Não alterar números apenas para confirmar uma hipótese ou criar um benefício aparente. Qualquer estudo de impacto futuro deve diferenciar parâmetros de simulação, cálculos descritivos e efeito atribuído a uma intervenção.
