# Reconciliação didática de indicadores — GENA EAD

> **Escopo e aviso:** base inteiramente fictícia; reconciliação técnica de contrato, bytes e definições, sem validação de mercado ou efeito de negócio.

## Rastreabilidade, fontes e integridade

- Referência dos dados: snapshot `2025-12-31`; versão do artefato: `1.0`; versão da configuração: `1.0.0`.
- Configuração: [`config.json`](../../retencao-ead/dados/config.json), SHA-256 verificado `98444bcb176af6ec…` (completo no [`resultado-reconciliacao.json`](./resultado-reconciliacao.json)).
- Dicionário da fonte: [`dicionario.md`](../../retencao-ead/dados/dicionario.md).
- Manifesto e hashes: [`manifesto.json`](../../retencao-ead/dados/csv/manifesto.json); 6/6 CSVs tiveram SHA-256, tamanho e contagem conferidos.

| CSV | Uso | SHA-256 verificado | Linhas |
|:---|:---|:---|---:|
| [`alunos_ead.csv`](../../retencao-ead/dados/csv/alunos_ead.csv) | identificacao/FK | `b4c61c4d334051f4…` | 3.970 |
| [`engajamento_semanal_ead.csv`](../../retencao-ead/dados/csv/engajamento_semanal_ead.csv) | contagem/qualidade complementar (nao entra nos cinco indicadores) | `35e03dde7f1ab293…` | 23.040 |
| [`financeiro_ead.csv`](../../retencao-ead/dados/csv/financeiro_ead.csv) | calculo | `a043ff6c8abf5ba4…` | 37.742 |
| [`matriculas_ead.csv`](../../retencao-ead/dados/csv/matriculas_ead.csv) | calculo | `fc00679dbbb9fd0e…` | 3.970 |
| [`pesquisa_nps_ead.csv`](../../retencao-ead/dados/csv/pesquisa_nps_ead.csv) | calculo | `b73848de17410486…` | 200 |
| [`referencias_segmentos.csv`](../../retencao-ead/dados/csv/referencias_segmentos.csv) | referencias agregadas/configuracao | `6b7bf5385a766dfb…` | 4 |

- Fontes usadas no cálculo dos cinco indicadores: `matriculas_ead.csv`, `financeiro_ead.csv`, `pesquisa_nps_ead.csv`.
- `alunos_ead.csv` apoia identificação/FK; `referencias_segmentos.csv` confere referências; `engajamento_semanal_ead.csv` fornece apenas contagem/qualidade complementar, não entra nos cinco indicadores.
- Implementação: [`scripts/reconciliar_indicadores.py`](../scripts/reconciliar_indicadores.py). Testes isolados: [`tests/test_reconciliacao.py`](../tests/test_reconciliacao.py). Contexto do caso: [`README.md`](../README.md), [`registro-decisoes.md`](../docs/registro-decisoes.md), [`dicionario-indicadores.md`](../docs/dicionario-indicadores.md).

## Erro semântico deliberado e correção

A mesma quantidade de 770 cancelamentos foi dividida primeiro pela fotografia de fechamento de 3.120 (denominador didático deliberadamente errado) e depois pela coorte de abertura elegível de 2.800. O segundo denominador é derivado de abertura/status e exclui retrospectivamente 40 concluídos e 40 transferidos. A anomalia foi criada intencionalmente para o exercício; não é descoberta operacional.

| Definição | Saídas | Denominador | Churn |
|:---|---:|---:|---:|
| Foto de ativos no fechamento (errado) | 770 | 3.120 | 24,68% |
| Coorte de abertura elegível (correto) | 770 | 2.800 | 27,50% |

Diferença: **2,82 p.p.** (a precisão integral permanece no JSON e no CSV). Isso é correção de definição, **não aumento de churn nem efeito de negócio**.

## Reconciliação populacional

- Abertura: `2.880`; conclusões: `40`; transferências: `40`; elegíveis: `2.800`; cancelamentos: `770`; retidos: `2.030`; ingressantes: `1.090`; ativos no fechamento: `3.120`.
- Equações conferidas: `2880 − 40 − 40 = 2800`; `2800 = 770 + 2030`; `2030 + 1090 = 3120`; `2880 + 1090 = 3970`.
- IDs únicos: `3.970`; FK aluno–matrícula e flag `elegivel_churn` conferidas contra abertura/status.

## Cinco indicadores recalculados independentemente

| Indicador | Numerador/contagem | Denominador/base | Resultado |
|:---|---:|---:|---:|
| Churn | 770 saídas | 2.800 elegíveis | **27,50%** |
| Retenção | 2.030 retidos | 2.800 elegíveis | **72,50%** |
| Inadimplência monetária | R$ 1.579.502,70 em aberto | R$ 11.700.020,00 devidos | **13,50%** |
| Adimplência monetária | R$ 10.120.517,30 liquidados | R$ 11.700.020,00 devidos | **86,50%** |
| NPS amostral | 118 promotores − 40 detratores | 200 respostas | **39** |

A posição monetária foi conferida em centavos com `ROUND_HALF_UP` sobre o total devido e alvo `0.135`. O NPS conferiu `200 = 118 + 42 + 40` e `(118 − 40) / 200 × 100 = 39`; ele não é estimativa populacional.

## Complementares e limites

- Engajamento: 23.040 linhas, 2.880 matrículas, 8 janelas por matrícula, de `2025-01-06` a `2025-02-28`. É apenas controle de contagem/qualidade; não há indicador agregado nem inferência de causalidade.
- Referência `Graduacao EAD` em configuração/CSV confere churn 27,50%, inadimplência 13,50%, NPS 39, ativos 2025 3.120 e ticket de R$ 310,00.
- Conversão: **não calculada, não testada, preliminarmente sem CRM/funil**; não há dado de conversão nesta fonte.
- Não há SQL, dashboard, modelo, piloto, ROI, custo, causalidade ou afirmação de impacto nesta entrega.

## Execução reprodutível

- O CLI executou **12 testes deste projeto** no momento da geração, antes de escrever as evidências, e só prosseguiu com resultado OK; não é gravado timestamp variável e esse número é independente de outros testes `test_dados_gena`.
- Comando principal (a partir de `governanca-indicadores`): `python3 scripts/reconciliar_indicadores.py`.
- Opções: `--source-dir CAMINHO_DADOS` troca a pasta `dados` (espera `config.json` e `csv/manifesto.json`); `--output-dir DIRETORIO` troca a pasta dos três artefatos; `--output CAMINHO_JSON` troca apenas o caminho do JSON (sem `--output-dir`, CSV/Markdown usam o diretório pai do JSON).
- Para apenas validar/inspecionar sem escrever, importe `analisar(source_dir)`; ela é side-effect-free. A referência de dados é o snapshot; a execução é real, mas os artefatos não registram o relógio.
