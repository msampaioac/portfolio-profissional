# Dicionário de dados GENA EAD

Esta é a primeira melhoria da base fictícia do GENA. O gerador é [`scripts/gerar_dados_gena.py`](../scripts/gerar_dados_gena.py), a configuração é [`config.json`](config.json), o manifesto é [`csv/manifesto.json`](csv/manifesto.json) e o contrato documental geral está em [`docs/contrato-dados.md`](../docs/contrato-dados.md).

## Escopo e aviso

- Todos os registros são sintéticos, sem nomes, documentos ou identificadores pessoais reais.
- Esta entrega cria dados para exploração e validação de integração. **Não contém modelo, dashboard, análise para afirmar efeito, experimento, evidência causal, custos, ROI, desempenho observado ou atendimentos.**
- A semente vem de `config.json`; os namespaces de geração são independentes. O gerador não usa data/hora corrente e grava UTF-8, separador vírgula, LF e ordenação estável para permitir reprodução byte a byte e conferência pelos hashes do manifesto.
- Booleanos nos CSV são literais `true` e `false`; valores nulos são campos vazios. Datas são ISO 8601 (`YYYY-MM-DD`), competência é `YYYY-MM` e valores monetários são inteiros em centavos de real.
- A fotografia de **2.880 alunos em 2024** é usada como população de abertura de 1º de janeiro de 2025. Há 2.880 registros da abertura, 1.090 ingressantes em 2025 e 3.970 alunos/matrículas no total.
- Os 2.880 registros da abertura recebem admissão sintética em 2022, 2023 ou 2024. As 40 conclusões são selecionadas somente na coorte de 2022. Outras 40 matrículas são transferidas e os 770 cancelamentos são embaralhados entre os 2.800 elegíveis restantes; os 2.030 demais permanecem ativos.
- Saídas de cancelamento, conclusão e transferência ocorrem sinteticamente entre abril e dezembro de 2025, sempre no dia 15 ou posterior. Os 1.090 ingressantes entram em março a novembro de 2025, sempre no dia 1, permanecem ativos no fechamento por construção e **não têm sinais de engajamento das primeiras oito semanas**.
- A atribuição de desfecho é um embaralhamento independente das características iniciais. O motivo de cancelamento é igualmente sintético e aleatório, não é um sinal determinante e não deve ser interpretado como causa.
- O financeiro é uma **posição em 31/12/2025**, não uma média mensal anual. Há no máximo 12 títulos por matrícula; cobranças não são emitidas depois do mês de saída e o mês de saída é incluído. O total de saldo aberto é calibrado para `ROUND_HALF_UP(total devido * 0,135)` em centavos: títulos inteiramente não pagos são percorridos por embaralhamento independente, há no máximo um título parcialmente pago e os demais são pagos. Datas de pagamento podem ser antecipadas ou atrasadas, mas ficam entre o primeiro dia da competência e 31/12/2025.
- O NPS contém 200 IDs distintos, amostrados dos 3.120 ativos finais, com data fixa de pesquisa em 15/12/2025: 118 promotores (9–10), 42 passivos (7–8) e 40 detratores (0–6), NPS amostral 39. Esta amostra não estima nem comprova o NPS da população.
- `referencias_segmentos.csv` tem apenas quatro linhas agregadas de referência, sem entidades individuais dos demais segmentos. Os valores são contexto sintético e não são entidades EAD adicionais.

## Populações, janelas e grãos

| Arquivo | Grão | Linhas esperadas | Janela | Chave primária | Chaves estrangeiras e observações |
|:---|:---|---:|:---|:---|:---|
| `alunos_ead.csv` | Um aluno EAD sintético | 3.970 | Admissões 2022–2025 | `student_id` | Nenhuma; não contém PII |
| `matriculas_ead.csv` | Uma matrícula por aluno | 3.970 | Início em 01/01/2025 para abertura; março–novembro para ingressantes; desfechos em 2025 | `matricula_id` | `student_id` referencia `alunos_ead.student_id` |
| `financeiro_ead.csv` | Um título mensal de 2025 por matrícula e competência | Determinada pelas janelas de cada matrícula; máximo 12 por matrícula | Janeiro–dezembro de 2025, limitado ao mês de saída | `titulo_id` | `matricula_id` referencia `matriculas_ead.matricula_id` |
| `engajamento_semanal_ead.csv` | Uma matrícula da abertura por semana | 23.040 = 2.880 × 8 | 06/01/2025–28/02/2025 | Chave composta (`matricula_id`, `semana_inicio`) | `matricula_id` referencia `matriculas_ead.matricula_id`; somente abertura |
| `pesquisa_nps_ead.csv` | Uma resposta por matrícula selecionada | 200 | Pesquisa fixa em 15/12/2025 | `resposta_id` | `matricula_id` referencia `matriculas_ead.matricula_id`; IDs distintos e ativos no fechamento |
| `referencias_segmentos.csv` | Uma linha agregada por segmento de referência | 4 | Fotografia de referências 2024/2025 | `segmento` | Sem entidades ou chaves EAD |

Cada arquivo de dados possui uma coluna de simulação (`simulado=true`). O arquivo semanal também possui `origem_simulada=true`, explicitando que o sinal não é um log operacional.

## Esquema dos CSV

### `alunos_ead.csv`

| Campo | Tipo no CSV | Obrigatório | Chave/FK | Domínio e significado |
|:---|:---|:---:|:---|:---|
| `student_id` | texto | sim | PK | ID sintético estável no formato `ALU######`. Não identifica pessoa real. |
| `curso` | texto | sim | — | Um dos cursos da configuração: `Administracao`, `Pedagogia` ou `Gestao Publica`. |
| `polo` | texto | sim | — | Um dos polos da configuração: `Polo Cidade Nova`, `Polo Cruzeiro do Sul` ou `Polo Sena Madureira`. |
| `data_admissao` | data ISO | sim | — | Abertura: primeiro dia do ano sintético de admissão 2022, 2023 ou 2024; ingressante: primeiro dia do mês de entrada em 2025. |
| `tipo_coorte` | texto | sim | — | `abertura_2025` para os 2.880 da fotografia de abertura; `ingressante_2025` para os 1.090 novos. |
| `simulado` | booleano literal | sim | — | Sempre `true`. |

### `matriculas_ead.csv`

| Campo | Tipo no CSV | Obrigatório | Chave/FK | Domínio e significado |
|:---|:---|:---:|:---|:---|
| `matricula_id` | texto | sim | PK | ID sintético estável no formato `MAT######`; há exatamente uma linha por `student_id`. |
| `student_id` | texto | sim | FK | Referencia `alunos_ead.student_id`. |
| `curso` | texto | sim | — | Cópia controlada do curso do aluno para uso no grão de matrícula. |
| `polo` | texto | sim | — | Cópia controlada do polo do aluno para uso no grão de matrícula. |
| `data_inicio` | data ISO | sim | — | Início da cobertura na base de 2025: `2025-01-01` para abertura; primeiro dia entre março e novembro para ingressante. Não é a admissão original, registrada em `alunos_ead.data_admissao`. |
| `status_final` | texto | sim | — | Um de `ativo`, `cancelado`, `concluido` ou `transferido`. `cancelado` representa os 770 desfechos de churn. |
| `data_saida` | data ISO ou vazio | não | — | Preenchida apenas para `cancelado`, `concluido` e `transferido`; de abril a dezembro de 2025, dia 15–28. Vazia para ativos. |
| `tipo_coorte` | texto | sim | — | `abertura_2025` ou `ingressante_2025`, conforme `alunos_ead`. |
| `pertencente_abertura` | booleano literal | sim | — | `true` para os 2.880 da fotografia usada em 01/01/2025; `false` para ingressantes. |
| `elegivel_churn` | booleano literal | sim | — | `true` retrospectivamente para os 2.800 da abertura após excluir 40 conclusões e 40 transferências; `false` para excluídos e ingressantes. |
| `motivo_saida` | texto ou vazio | não | — | Para `cancelado`, um de `financeiro`, `academico`, `pessoal` ou `nao_informado`, atribuído aleatoriamente sem relação desenhada com sinais. Vazio nos demais status. |
| `simulado` | booleano literal | sim | — | Sempre `true`. |

Equações de consistência: `2.800 = 2.880 − 40 − 40`; `2.800 = 770 + 2.030`; `3.120 = 2.030 + 1.090`; `3.970 = 2.880 + 1.090`.

### `engajamento_semanal_ead.csv`

| Campo | Tipo no CSV | Obrigatório | Chave/FK | Domínio e significado |
|:---|:---|:---:|:---|:---|
| `matricula_id` | texto | sim | FK e parte da chave composta | Referencia matrícula da coorte de abertura; cada matrícula tem oito linhas. |
| `semana_inicio` | data ISO | sim | Parte da chave composta | `2025-01-06`, `2025-01-13`, `2025-01-20`, `2025-01-27`, `2025-02-03`, `2025-02-10`, `2025-02-17` ou `2025-02-24`. |
| `semana_fim` | data ISO | sim | — | Seis dias depois para as sete primeiras semanas; `2025-02-28` na última. Nunca passa do corte. |
| `dias_com_acesso` | inteiro | sim | — | De 0 a 7, limitado ao número de dias reais da janela; na última semana, de 0 a 5. |
| `atividades_previstas` | inteiro | sim | — | Inteiro maior ou igual a 1, heterogêneo e simulado. |
| `atividades_entregues` | inteiro | sim | — | Inteiro de 0 até `atividades_previstas`. |
| `origem_simulada` | booleano literal | sim | — | Sempre `true`; sinal gerado, não log de sistema. |
| `simulado` | booleano literal | sim | — | Sempre `true`. |

Os valores de engajamento usam um namespace de RNG independente do namespace que embaralha desfechos. Não há colunas de status, saída, risco ou qualquer resultado futuro e não há linhas para os ingressantes.

### `financeiro_ead.csv`

| Campo | Tipo no CSV | Obrigatório | Chave/FK | Domínio e significado |
|:---|:---|:---:|:---|:---|
| `titulo_id` | texto | sim | PK | ID sintético estável no formato `TIT#######`. |
| `matricula_id` | texto | sim | FK | Referencia `matriculas_ead.matricula_id`. |
| `competencia` | mês ISO | sim | — | Mês de referência de 2025 (`2025-01` a `2025-12`). |
| `vencimento` | data ISO | sim | — | Dia 10 da competência. |
| `valor_devido_centavos` | inteiro não negativo | sim | — | Sempre o ticket EAD da configuração: 31.000 centavos por título. |
| `valor_pago_centavos` | inteiro não negativo | sim | — | Menor ou igual ao devido; inclui pagamento integral ou parcial. |
| `data_pagamento` | data ISO ou vazio | não | — | Vazia quando `valor_pago_centavos=0`; caso contrário, de 1º dia da competência até 31/12/2025, permitindo antecipação e atraso. |
| `saldo_aberto_centavos` | inteiro não negativo | sim | — | `valor_devido_centavos − valor_pago_centavos`, posição em 31/12/2025. |
| `posicao_financeira2025-12-31` | texto | sim | — | `aberto` quando `saldo_aberto_centavos>0`; `liquidado` quando zero. |
| `simulado` | booleano literal | sim | — | Sempre `true`. |

A geração cria títulos do mês de entrada até dezembro para ativos ingressantes, de janeiro até dezembro para ativos da abertura, e de janeiro até o mês de saída inclusive para uma matrícula que saiu. Não há título posterior à saída. A taxa de 13,5% é aplicada ao total devido de todos os títulos gerados e arredondada em centavos com `ROUND_HALF_UP`; o manifesto registra a calibração.

### `pesquisa_nps_ead.csv`

| Campo | Tipo no CSV | Obrigatório | Chave/FK | Domínio e significado |
|:---|:---|:---:|:---|:---|
| `resposta_id` | texto | sim | PK | ID sintético estável no formato `NPS####`. |
| `matricula_id` | texto | sim | FK | Referencia uma matrícula ativa no fechamento; 200 IDs distintos são amostrados dos 3.120 ativos. |
| `data_pesquisa` | data ISO | sim | — | Sempre `2025-12-15`. |
| `nota` | inteiro | sim | — | Escala inteira de 0 a 10. Promotor: 9–10; passivo: 7–8; detrator: 0–6. |
| `classificacao_nps` | texto | sim | — | `promotor`, `passivo` ou `detrator`, coerente com `nota`. |
| `simulado` | booleano literal | sim | — | Sempre `true`. |

A composição é fixa em 118 promotores, 42 passivos e 40 detratores. O NPS amostral é `(118 − 40) / 200 × 100 = 39`; não se deve inferir um parâmetro populacional nem efeito de intervenção.

### `referencias_segmentos.csv`

| Campo | Tipo no CSV | Obrigatório | Chave/FK | Domínio e significado |
|:---|:---|:---:|:---|:---|
| `segmento` | texto | sim | PK | Um dos quatro segmentos agregados definidos no `config.json`. |
| `ativos_2024` | inteiro não negativo | sim | — | Contagem de referência na fotografia de 2024. |
| `ativos_2025` | inteiro não negativo | sim | — | Contagem de referência na fotografia de 2025. |
| `ticket_centavos` | inteiro não negativo | sim | — | Ticket mensal de referência, sempre em centavos. |
| `churn_percentual_referencia` | decimal textual | sim | — | Percentual de referência, não uma medição calculada a partir dos demais CSV. |
| `inadimplencia_percentual_referencia` | decimal textual | sim | — | Percentual de referência agregado, não uma média calculada desta base. |
| `nps_referencia` | inteiro | sim | — | NPS de referência no intervalo de −100 a 100. |
| `simulado` | booleano literal | sim | — | Sempre `true`. |

As quatro linhas são `Educacao Basica`, `Graduacao presencial`, `Graduacao EAD` e `Pos-graduacao e extensao`. Não há alunos, matrículas ou títulos dos outros segmentos nesta entrega.

## Manifesto

`csv/manifesto.json` não é incluído no próprio conjunto de hashes. Seus campos principais são:

| Campo | Significado |
|:---|:---|
| `versao` | Versão permitida da configuração usada na geração. |
| `semente` | Semente inteira da configuração. |
| `seed` | Alias da mesma semente inteira, para consumo por ferramentas que usam nomenclatura inglesa. |
| `config_sha256` | SHA-256 dos bytes originais de `config.json`; o mesmo valor também aparece em `config.sha256`. |
| `snapshot` | `2025-12-31`. |
| `data_corte_sinais` | `2025-02-28`. |
| `contagens` | Quantidade de linhas de dados, sem contar o cabeçalho, por CSV. |
| `sizes` | Tamanho em bytes de cada CSV UTF-8. |
| `sha256` | SHA-256 dos bytes de cada CSV. |
| `granularidade` | Descrição do grão de cada CSV. |
| `arquivos` | Metadados combinados de contagem, tamanho, hash e granularidade. |
| `calibracoes` | Resumo das calibrações de churn, NPS e posição financeira. |
| `aviso` e `aviso_calibrado` | Aviso de ficcionalidade, limites e interpretação da posição financeira/NPS. |

A ausência de timestamp dinâmico no manifesto e nos CSV é deliberada: com a mesma configuração e versão do gerador, os bytes e hashes devem permanecer estáveis.

## Métodos e limites de uso

1. O gerador valida versão permitida, equações de população, taxa de churn, composição do NPS, ticket e janelas antes de escrever qualquer CSV.
2. Cursos, polos, admissões, datas de saída, motivos, engajamento, seleção NPS, notas e datas de pagamento são sintéticos. O embaralhamento dos desfechos não usa engajamento futuro nem cria relação causal desenhada.
3. A base não tem custos de intervenção, orçamento, atendimento, notas, desempenho acadêmico, impacto, ROI ou mecanismo de acompanhamento de efeito. Esses elementos devem ser especificados em uma etapa posterior, sem atribuir efeito a esta primeira melhoria.
4. O documento da empresa informa hipóteses estratégicas, não evidência. Qualquer análise posterior deve declarar denominador, elegibilidade, janela e a diferença entre referência agregada, posição financeira e amostra NPS.
