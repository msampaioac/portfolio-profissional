# Modelo lógico — relações e níveis de detalhe

[Projeto de governança](../README.md) · [Inventário](inventario-fontes.md) · [Dicionário de indicadores](dicionario-indicadores.md)

## Relações existentes na base fictícia

| Entidade de origem | Relação | Entidade dependente | Regra |
|:---|:---:|:---|:---|
| Aluno (`student_id`) | 1:1 nesta versão | Matrícula (`matricula_id`) | Cada aluno tem uma matrícula. Em uma instituição real, essa simplificação teria de ser revista. |
| Matrícula | 1:N | Título financeiro (`titulo_id`) | Até 12 competências em 2025, limitadas à entrada e à saída. |
| Matrícula | 1:8 para a abertura | Engajamento semanal | Oito janelas até 28/02/2025. Ingressantes posteriores não recebem sinais inventados. |
| Matrícula | 1:0 ou 1 | Resposta de NPS | Uma resposta por matrícula selecionada; a maioria não respondeu na amostra sintética. |
| Segmento | Referência agregada | Sem relação individual | A tabela macro não cria alunos, títulos ou pesquisas nos demais segmentos. |

As entidades não são intercambiáveis. Uma linha financeira representa um título, não um aluno; uma resposta de NPS representa uma participação na pesquisa, não toda a população matriculada.

## Regra de cálculo por indicador

| Indicador | Nível de detalhe usado | Agregação segura |
|:---|:---|:---|
| Churn e retenção | Matrícula da abertura | Selecionar a coorte e as exclusões antes de contar os desfechos. |
| Adimplência e inadimplência monetárias | Título vencido até o fechamento | Somar os valores em centavos antes de dividir; não usar contagem de alunos devedores. |
| NPS | Resposta válida da pesquisa | Classificar notas e calcular entre as respostas, sem incluir não respondentes no denominador. |
| Conversão | Pessoa/lead × etapa do funil | Ainda não implementado; faltam identificação, eventos e janela. |

## Como evitar multiplicação de registros

Juntar títulos financeiros e engajamento diretamente por matrícula pode multiplicar cada título pelas semanas de acesso. Isso inflaria os totais, mesmo que os identificadores pareçam corretos.

Neste ciclo, cada indicador é calculado **na sua tabela de origem**. Antes de uma futura junção analítica, os valores devem ser agregados ao nível necessário e a relação entre chaves deve ser testada. Uma junção não deve mudar o total financeiro nem a população acadêmica por efeito de duplicação.

## População e tempo

A abertura é 01/01/2025; o fechamento é 31/12/2025. `data_inicio` representa o início de cobertura da matrícula na base de 2025, e não a admissão original, registrada no aluno.

A elegibilidade ao churn é reconstruída com abertura e status final. Conclusões e transferências são separadas de abandono. Essa regra é retrospectiva: `elegivel_churn`, status final, saldo de dezembro e NPS de dezembro não são informações disponíveis para priorizar alunos em fevereiro.

## Evidência e limite

O [script](../scripts/reconciliar_indicadores.py) utiliza as relações necessárias ao cálculo e confronta os arquivos com seus hashes. O [relatório](../evidencias/reconciliacao.md) registra o resultado do ciclo. Este modelo é documentação das relações da base existente; não é um data warehouse, ETL ou arquitetura produtiva implantada.
