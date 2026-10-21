# Base fictícia da GENA — retenção EAD

**Dados sintéticos · Versão 1.0.0 · Referência de 2025**

[Portfólio](../../README.md) · [Case de retenção](../../cases/grupo-educacional/reducao-churn-ead.md) · [Contrato de dados](../../docs/contrato-dados-gena.md) · [Dicionário](dicionario.md) · [Reconciliação e testes](validacao.md)

## O que avaliar primeiro

Esta entrega transforma os indicadores institucionais em registros verificáveis. Comece pela [reconciliação](validacao.md): a fotografia final de 3.120 ativos EAD não é o denominador de churn, que corresponde a 2.800 elegíveis da coorte inicial.

**Os números foram calibrados para o cenário fictício.** Reconstruir 27,5% de churn, 13,5% de inadimplência monetária e NPS 39 demonstra coerência do dataset, não uma descoberta analítica nem a eficácia de um projeto de retenção.

## Arquivos disponíveis

| Arquivo | Unidade de registro | Uso |
|:---|:---|:---|
| [alunos_ead.csv](csv/alunos_ead.csv) | Aluno sintético | Identificação, sem nome ou documento pessoal |
| [matriculas_ead.csv](csv/matriculas_ead.csv) | Matrícula | Abertura, entradas, status e saídas |
| [financeiro_ead.csv](csv/financeiro_ead.csv) | Título mensal | Valor devido, pagamento e saldo no fechamento |
| [engajamento_semanal_ead.csv](csv/engajamento_semanal_ead.csv) | Matrícula × semana | Sinais iniciais, até 28/02/2025 |
| [pesquisa_nps_ead.csv](csv/pesquisa_nps_ead.csv) | Resposta única | Reprodução da composição fictícia do NPS |
| [referencias_segmentos.csv](csv/referencias_segmentos.csv) | Segmento | Preservação dos totais e referências institucionais |
| [manifesto.json](csv/manifesto.json) | Artefato gerado | Contagens, configuração e hashes SHA-256 |

Os microdados cobrem somente EAD. Básica, presencial e pós/extensão aparecem como referências agregadas; não receberam bases individuais nesta etapa.

## Como reproduzir

Na raiz de uma cópia do repositório, com **Python 3.10 ou superior**, sem bibliotecas externas:

```bash
python3 scripts/gerar_dados_gena.py
python3 -m unittest discover -s tests -v
python3 scripts/validar_dados_gena.py
```

O primeiro comando gera os arquivos CSV e o manifesto; o segundo executa os testes; o terceiro recalcula os indicadores, verifica o manifesto e atualiza [validacao.md](validacao.md). Falhas impedem emitir o relatório como aprovado.

O gerador também aceita uma configuração e pasta de saída alternativas:

```bash
python3 scripts/gerar_dados_gena.py --config dados/gena/config.json --output /tmp/gena-reproducao
```

Consulte o [gerador](../../scripts/gerar_dados_gena.py), os [testes](../../tests/test_dados_gena.py), o [validador](../../scripts/validar_dados_gena.py) e a [configuração oficial](config.json). Não é necessário instalar pacotes ou usar uma chave de API.

## O que já existe e o que ainda não existe

**Disponível:** base sintética, dicionário, regras de geração, reconciliação e controles automatizados. **Ainda não implementado:** análise diagnóstica por curso/polo, consultas SQL de negócio, dashboard, segmentação validada, piloto e mensuração de impacto.

Não use os desfechos de dezembro, a elegibilidade retrospectiva ou a posição financeira final como informações conhecidas em fevereiro. O [contrato](../../docs/contrato-dados-gena.md) explica os limites temporais e as premissas simplificadoras.

## Manutenção em lote

A configuração é a fonte única de parâmetros. Qualquer mudança deve regenerar os dados e atualizar simultaneamente os documentos relacionados. O [registro de mudanças](../../docs/registro-mudancas-gena.md) explica o que foi preservado, o que foi definido e o que continua pendente.
