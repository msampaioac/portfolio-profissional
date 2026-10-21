# Inventário das fontes — GENA

[Projeto de governança](../README.md) · [Modelo lógico](modelo-logico.md) · [Dicionário de indicadores](dicionario-indicadores.md)

## Fonte efetiva do estudo

Este inventário descreve os arquivos já publicados no projeto irmão [Retenção EAD](../../retencao-ead/dados/README.md). São dados fictícios, gerados por Python, não extrações de sistemas de uma instituição. A governança os consome em modo de leitura, sem duplicar ou alterar a base.

A referência é 2025, com posição final em 31/12/2025. A versão 1.0.0 e a semente estão na [configuração](../../retencao-ead/dados/config.json). A procedência é verificável pelo [gerador](../../retencao-ead/scripts/gerar_dados_gena.py) e pelos hashes do [manifesto](../../retencao-ead/dados/csv/manifesto.json).

## Arquivos disponíveis

| Fonte | Unidade e chave | Uso no estudo de governança |
|:---|:---|:---|
| [alunos_ead.csv](../../retencao-ead/dados/csv/alunos_ead.csv) | Um aluno; `student_id` | Identificação sintética e vínculo com a matrícula; não usar como tabela de títulos ou pesquisa. |
| [matriculas_ead.csv](../../retencao-ead/dados/csv/matriculas_ead.csv) | Uma matrícula por aluno; `matricula_id` | Abertura, entradas, saídas, população elegível, churn e retenção. |
| [financeiro_ead.csv](../../retencao-ead/dados/csv/financeiro_ead.csv) | Um título por matrícula/competência; `titulo_id` | Valor devido, pago e saldo aberto em centavos; adimplência e inadimplência monetárias. |
| [pesquisa_nps_ead.csv](../../retencao-ead/dados/csv/pesquisa_nps_ead.csv) | Uma resposta por matrícula amostrada; `resposta_id` | Notas, classificação e cálculo do NPS; não é censo nem medida de toda a população. |
| [engajamento_semanal_ead.csv](../../retencao-ead/dados/csv/engajamento_semanal_ead.csv) | Matrícula × semana; chave composta | Referência de sinais iniciais para outro projeto; não entra no cálculo dos cinco indicadores deste ciclo. |
| [referencias_segmentos.csv](../../retencao-ead/dados/csv/referencias_segmentos.csv) | Um segmento; `segmento` | Confrontar os parâmetros institucionais. Outros segmentos não possuem microdados nesta etapa. |

O esquema completo dos campos permanece no [dicionário da base](../../retencao-ead/dados/dicionario.md). Contagens e hashes utilizados nesta execução ficam no [resultado da reconciliação](../evidencias/resultado-reconciliacao.json).

## Responsabilidades propostas sobre as fontes

| Informação | Área que validaria o significado em uma implantação | Controle demonstrável no estudo |
|:---|:---|:---|
| Matrículas e status | Acadêmico | Unicidade, pertencimento à abertura, exclusões e movimento de matrículas |
| Títulos e pagamentos | Financeiro | Vencimento alcançado, valores em centavos e conciliação devido = pago + saldo |
| Respostas de pesquisa | Área responsável pela pesquisa de experiência | Resposta única, nota válida e categoria compatível |
| Parâmetros e versões | Coordenação, com validação das áreas | Configuração e hashes; nenhuma mudança silenciosa na fonte |

Essas áreas são papéis de uma implantação proposta, não aprovadores que participaram de uma execução empresarial real.

## Fontes ausentes e efeito sobre o escopo

Não há CRM, leads, vínculo entre concluintes do Ensino Médio e futuras matrículas, histórico de atendimento, registro de intervenção ou custos. Portanto:

- Conversão permanece uma especificação preliminar, sem cálculo ou meta.
- Não se mede efeito de atendimento preventivo, recuperação financeira ou ROI.
- Não se atribui aos arquivos um sistema de origem, uma data de carga ou uma aprovação humana inexistentes.

Uma implantação exigiria identificar sistemas, permissões, responsáveis e atualização das fontes antes de substituir esta simulação por dados operacionais.
