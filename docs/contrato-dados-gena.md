# Contrato dos dados fictícios da GENA

**Versão 1.0.0 · Cenário de 2025 · Dados inteiramente sintéticos**

[Portfólio](../README.md) · [Empresa fictícia](empresa-ficticia-grupo-educacional.md) · [Base e reprodução](../dados/gena/README.md) · [Dicionário](../dados/gena/dicionario.md)

## 1. O que esta entrega permite examinar

A base materializa o contexto do projeto de retenção EAD: identificação sintética, status de matrícula, mensalidades, pagamentos, engajamento e respostas de NPS. Um avaliador pode regenerar os arquivos, conferir as fórmulas e testar a consistência entre registros e documentos.

Isso é uma **entrega de preparação de dados**, não a execução de um piloto nem a validação de uma estratégia. Os dados foram calibrados para conservar o cenário institucional; reproduzir esses números não constitui descoberta, comprovação externa ou impacto profissional.

Os parâmetros oficiais estão em [config.json](../dados/gena/config.json). Alterações futuras devem atualizar essa configuração, regenerar a base, executar os testes e revisar todos os documentos afetados em um único lote.

## 2. População e movimento de matrículas

A fotografia de 31/12/2024, com 2.880 ativos EAD, é usada como abertura em 01/01/2025. A fotografia final continua sendo 3.120 ativos EAD em 31/12/2025.

| Movimento EAD | Matrículas | Significado |
|:---|---:|:---|
| Abertura de 2025 | 2.880 | Coorte já ativa, oriunda da fotografia de 2024 |
| Conclusões regulares | 40 | Saídas separadas de abandono |
| Transferências externas | 40 | Saídas separadas de abandono |
| Elegíveis ao churn | 2.800 | Abertura menos conclusões e transferências |
| Cancelamentos/abandono | 770 | Saídas da população elegível |
| Retidos da coorte de abertura | 2.030 | Elegíveis que permanecem ativos no fechamento |
| Novas matrículas de 2025 | 1.090 | Entradas entre março e novembro, todas ativas no cenário simplificado |
| Ativos no fechamento | **3.120** | Retidos mais novas matrículas |
| Matrículas distintas presentes no ano | **3.970** | Abertura mais entradas; não confundir com ativos finais |

A reconciliação obrigatória é:

```text
2.880 − 40 − 40 = 2.800 elegíveis
770 + 2.030 = 2.800 elegíveis
2.880 − 40 − 40 − 770 + 1.090 = 3.120 ativos finais
2.880 + 1.090 = 3.970 matrículas distintas no ano
```

Há uma matrícula por aluno nesta versão. Conclusões são atribuídas a matrículas de ingresso em 2022; transferências são externas, sem gerar outra matrícula interna. Datas de saída situam-se entre abril e dezembro, depois da janela inicial de sinais.

**Premissa simplificadora explícita:** não há abandono entre os ingressantes de 2025. Isso facilita conservar a fotografia institucional, mas torna o grupo inadequado para estimar churn de novos alunos. As quantidades de conclusões, transferências e entradas são novas premissas de modelagem, não fatos previamente existentes no perfil da empresa.

## 3. Indicadores: fórmula e janela

| Indicador | Definição nesta versão | Referência preservada |
|:---|:---|:---|
| Churn anual da abertura | Cancelados elegíveis ÷ elegíveis da abertura | 770 ÷ 2.800 = **27,5%** |
| Retenção anual da abertura | Ativos finais elegíveis ÷ elegíveis da abertura | 2.030 ÷ 2.800 = **72,5%** |
| Ticket EAD | Valor devido por parcela mensal emitida, sem bolsas nesta versão | **R$ 310** |
| Inadimplência monetária | Saldo aberto ÷ valor devido dos títulos maturados de 2025, posição em 31/12/2025 | **13,5%**, alvo calibrado em centavos |
| Adimplência monetária | Valor pago ÷ o mesmo denominador financeiro | **86,5%**, complemento após conciliação |
| NPS | 100 × (promotores − detratores) ÷ respostas válidas | 100 × (118 − 40) ÷ 200 = **39** |

Conclusões e transferências são excluídas retrospectivamente de ambos os denominadores acadêmicos e reconciliadas separadamente. As regras são fixadas antes do cálculo, mas a lista final de elegíveis depende dos status de encerramento. Portanto, `elegivel_churn` **não é uma variável disponível para priorizar alunos em fevereiro**.

Sem denominador positivo, a taxa é indefinida — não zero. Valores monetários são inteiros em centavos; o alvo financeiro é arredondado ao centavo com `ROUND_HALF_UP`. O relatório apresenta valores calculados, não apenas os parâmetros.

### Ajuste semântico do indicador financeiro

O perfil anterior usava “inadimplência média” sem definir média, período e ponderação. Nesta versão, preserva-se 13,5%, mas o conceito EAD passa a ser **posição monetária em 31/12/2025 sobre os títulos vencidos de 2025**. Não é média das taxas mensais, taxa de alunos devedores nem proporção da receita futura.

As mensalidades são emitidas de janeiro até dezembro para a coorte ativa, encerrando-se no mês da saída. Para ingressantes, a emissão começa no mês de entrada. Não há cobrança posterior à saída, títulos futuros no denominador, bolsas, descontos, multas ou reativações nesta versão. O valor devido não é denominado receita contábil, e o saldo não comprova perda definitiva.

O pagamento é alocado ao título; pode ser integral, parcial ou inexistente. Sem pagamento, a data permanece vazia, não recebe uma data falsa. A posição de dezembro não reconstitui automaticamente a inadimplência em fevereiro.

## 4. Abrangência do universo

| Frente | Cobertura da entrega |
|:---|:---|
| Graduação EAD | Microdados de alunos, matrículas, financeiro, engajamento e NPS |
| Educação Básica | Apenas linha de referência institucional; 3.340 ativos finais |
| Graduação presencial | Apenas linha de referência institucional; 2.560 ativos finais |
| Pós-graduação/extensão | Apenas linha de referência institucional; 1.020 ativos finais |
| Total institucional | 10.040 ativos finais, conciliados entre os quatro segmentos |

O gerador não inventa históricos individuais para os outros segmentos nem pretende validar toda a série de 2021–2025. Os demais indicadores permanecem referências macro do universo fictício.

A oferta EAD desta amostra usa Administração, Pedagogia e Gestão Pública. Essa escolha é uma premissa didática dentro do portfólio da GENA, não autorização real de oferta nem indicação de que Direito ou Enfermagem sejam oferecidos em EAD. Os polos são Cidade Nova, Cruzeiro do Sul e Sena Madureira, preservando os nomes institucionais.

## 5. Sinais iniciais e prevenção de vazamento temporal

O engajamento contém oito janelas semanais de 06/01 a 28/02/2025 para as 2.880 matrículas de abertura. A última janela é parcial e termina em 28/02. Zero acesso é um valor observado na simulação; não representa campo ausente. Ingressantes posteriores não recebem registros iniciais inventados.

A geração do engajamento usa um fluxo aleatório independente dos desfechos. Cancelamentos não são atribuídos aos alunos de baixo acesso para confirmar a hipótese. As diferenças eventualmente encontradas são propriedades artificiais da amostra, não evidências de causas reais de evasão.

Para qualquer futura classificação com corte em 28/02/2025, não usar status final, elegibilidade retrospectiva, motivo/data de saída, posição financeira de dezembro, nota NPS de dezembro nem rótulos de retenção. Reconstruir os estados históricos a partir de informações efetivamente disponíveis no corte antes de utilizar sinais financeiros.

## 6. NPS e calibração

São 200 respostas únicas de alunos ativos no fechamento: 118 promotores, 42 passivos e 40 detratores. A composição é calibrada para NPS 39. Não se trata de pesquisa realizada, amostra representativa ou estimativa da satisfação de uma população real.

Churn, fotografia final, mensalidade, posição financeira e composição de NPS são **restrições de geração deliberadas**. Curso, polo e sinais semanais são sintéticos. Calibração não equivale a validação de negócio e não autoriza avaliar poder preditivo ou efeito de intervenção.

## 7. Reprodutibilidade e atualização

A geração usa apenas a biblioteca padrão do Python. A semente e a configuração tornam os bytes dos arquivos e seus hashes reproduzíveis no ambiente suportado. O [manifesto](../dados/gena/csv/manifesto.json) registra contagens e SHA-256, sem carimbo de tempo variável.

A rotina obrigatória de mudança é: modificar configuração ou gerador; regenerar em pasta limpa; executar testes e reconciliação; registrar a mudança; atualizar o perfil institucional, os cases, a síntese e o estado das entregas; publicar tudo em conjunto.

## 8. Limites desta primeira melhoria

Não foram gerados dados pessoais reais, atendimento, notas acadêmicas, intervenção, custos, margens, grupos de controle ou efeitos de retenção. Não há dashboard, modelo preditivo treinado nem ROI. Esses itens não devem aparecer como concluídos no portfólio.

Os artefatos são estruturados com apoio de IA. O que se demonstra aqui é um contrato de dados consistente, geração reproduzível e controles testáveis para uma empresa fictícia.
