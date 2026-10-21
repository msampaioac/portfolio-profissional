# Reconciliação e testes — GENA fictícia

**Versão 1.0.0 · Cenário de 2025 · Conferência de dados sintéticos**

[Base e reprodução](README.md) · [Contrato](../docs/contrato-dados.md) · [Dicionário](dicionario.md)

Esta reconciliação foi recalculada a partir dos CSV. A base é calibrada: o resultado demonstra consistência técnica, não descoberta, execução operacional, validade empírica ou efeito de retenção.

## População e indicadores acadêmicos

| Item | Valor calculado |
|:---|---:|
| Abertura em 01/01/2025 | 2.880 |
| Conclusões separadas | 40 |
| Transferências externas separadas | 40 |
| Elegíveis ao churn | 2.800 |
| Cancelados elegíveis | 770 |
| Retidos elegíveis | 2.030 |
| Novas matrículas | 1.090 |
| Ativos no fechamento | 3.120 |
| Matrículas distintas no ano | 3.970 |
| Churn anual da abertura | 27,5% |
| Retenção anual da abertura | 72,5% |

Conclusões/transferências são excluídas retrospectivamente de ambos os denominadores. Os ingressantes estão todos ativos por simplificação; não se estima churn desse grupo.

## Financeiro na posição de 31/12/2025

| Item | Valor calculado |
|:---|---:|
| Títulos vencidos de 2025 | 37.742 |
| Valor devido | R$ 11.700.020,00 |
| Valor pago até o snapshot | R$ 10.120.517,30 |
| Saldo aberto | R$ 1.579.502,70 |
| Inadimplência monetária | 13,5% |
| Adimplência monetária | 86,5% |

Não são média de taxas mensais, receita contábil ou benefício de intervenção. O saldo-alvo é arredondado ao centavo; os títulos incluem o mês da saída, nunca meses posteriores.

## NPS e cobertura

O NPS calculado é **39**, com 200 respostas únicas: 118 promotores, 42 passivos e 40 detratores. A composição foi calibrada; não é pesquisa real ou estimativa representativa.

Há 23.040 registros de engajamento nas oito janelas iniciais de 2.880 matrículas. O total institucional de referência é 10.040 ativos; somente EAD possui microdados.

## Arquivos conferidos

| Arquivo | Linhas de dados | SHA-256 abreviado |
|:---|---:|:---|
| [alunos_ead.csv](csv/alunos_ead.csv) | 3.970 | `b4c61c4d334051f4…` |
| [engajamento_semanal_ead.csv](csv/engajamento_semanal_ead.csv) | 23.040 | `35e03dde7f1ab293…` |
| [financeiro_ead.csv](csv/financeiro_ead.csv) | 37.742 | `a043ff6c8abf5ba4…` |
| [matriculas_ead.csv](csv/matriculas_ead.csv) | 3.970 | `fc00679dbbb9fd0e…` |
| [pesquisa_nps_ead.csv](csv/pesquisa_nps_ead.csv) | 200 | `b73848de17410486…` |
| [referencias_segmentos.csv](csv/referencias_segmentos.csv) | 4 | `6b7bf5385a766dfb…` |

Hashes completos e tamanhos estão em [manifesto.json](csv/manifesto.json). A configuração utilizada foi conferida pelo seu hash.

## Controles executados

**13 testes automatizados aprovados**, além da conferência dos CSV publicados e do manifesto. Os testes regeneram o cenário em pasta temporária e verificam:

- Chaves, vínculos, status, populações, fórmulas e emissão de títulos.
- Centavos inteiros, reconciliação de pagamentos e ausência de datas falsas para não pagos.
- Janelas iniciais sem campos de desfecho e invariância dos sinais quando os desfechos são alterados.
- Composição do NPS, referência institucional e identificação de simulação.
- Reprodução byte a byte e rejeição de configuração incoerente.

Os testes de contrato validam as regras sintéticas, não predizem evasão nem homologam a operação de uma instituição real. Reexecute após qualquer alteração.

A partir da raiz do repositório, entre na pasta do projeto:

```bash
cd cases/gena/projetos/retencao-ead
python3 scripts/gerar_dados_gena.py
python3 -m unittest discover -s tests -v
python3 scripts/validar_dados_gena.py
```

[Testes](../tests/test_dados_gena.py) · [Validador](../scripts/validar_dados_gena.py) · [Registro de mudanças](../docs/registro-mudancas.md)

**Próxima etapa, ainda não realizada:** análise diagnóstica, consultas SQL, painel e desenho detalhado de avaliação do piloto. Não há resultado de intervenção, ROI ou modelo treinado.
