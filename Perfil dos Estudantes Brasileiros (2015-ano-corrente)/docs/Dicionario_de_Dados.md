# Dicionário de Dados

## Projeto

**Perfil dos Estudantes Brasileiros (2015–ano corrente)**

## Fonte dos Dados

- Base dos Dados
- INEP — Censo Escolar
- INEP — Censo da Educação Superior
- Diretório de Municípios — IBGE

---

# Objetivo

Este dicionário descreve os campos produzidos pela consulta SQL desenvolvida para integrar dados do Censo Escolar e do Censo da Educação Superior em uma única base analítica.

A base foi estruturada para apoiar projetos de Business Intelligence, Analytics, Ciência de Dados, Engenharia de Dados e avaliação de políticas públicas educacionais.

## Snapshot da estrutura observada

Na execução de referência incorporada ao notebook, a saída apresentou **54 colunas**, **4.582.798 linhas** e cobertura de **2015 a 2024**. A estrutura esperada pode variar quando a fonte for atualizada, mas os nomes documentados neste arquivo correspondem ao contrato analítico atual da consulta.

Na execução de referência, o indicador `perc_em_escola_com_internet` da Educação Básica teve cobertura observada até 2020, enquanto a base integrada alcançou 2024. Indicadores distintos podem ter períodos de disponibilidade diferentes.

## Granularidade da saída

Cada linha representa um agrupamento por ano, fonte, nível de ensino, território, unidade de ensino ou curso (quando aplicável), características demográficas disponíveis e demais dimensões institucionais. Portanto, a saída não é uma linha individual por estudante. `qtd_estudantes` representa a soma dos registros ou matrículas disponíveis na fonte para aquele agrupamento; os totais nacionais devem ser calculados a partir das contagens, nunca pela soma ou média simples dos percentuais.

---

# Dicionário de Campos

| Campo | Tipo | Descrição |
|---|---|---|
| ano | Inteiro | Ano de referência dos dados, considerando os anos disponíveis desde 2015 até o ano corrente da execução. |
| fonte | Texto | Base de origem dos dados: `CENSO_ESCOLAR` ou `CENSO_SUPERIOR`. |
| nivel_ensino | Texto | Nível de ensino analisado: Ensino Fundamental, Ensino Médio ou Ensino Superior. |
| sigla_uf | Texto | Sigla da Unidade da Federação. |
| id_municipio | Inteiro | Código IBGE do município. |
| nome_municipio | Texto | Nome do município. |
| regiao | Texto | Região geográfica do Brasil: Norte, Nordeste, Centro-Oeste, Sudeste ou Sul. |
| sexo | Texto | Sexo do estudante. Para o Ensino Superior, pode ser apresentado de forma agregada, conforme disponibilidade da base. |
| raca_cor | Texto | Raça/cor declarada pelo estudante. |
| faixa_etaria | Texto | Faixa etária construída a partir da idade do estudante. |
| nacionalidade | Texto | Nacionalidade declarada pelo estudante. |
| rede | Texto | Rede de ensino: Pública ou Privada. |
| tipo_localizacao | Texto | Localização da escola: Urbana ou Rural. |
| tipo_localizacao_diferenciada | Texto | Indica escolas localizadas em áreas indígenas, quilombolas, assentamentos ou outras localidades diferenciadas. |
| tipo_modalidade_ensino | Texto | Modalidade do curso superior: Presencial ou Educação a Distância. |
| tipo_grau_academico | Texto | Grau acadêmico do curso superior: Bacharelado, Licenciatura ou Tecnológico. |
| tipo_organizacao_academica | Texto | Organização acadêmica da Instituição de Ensino Superior. |
| tipo_organizacao_administrativa | Texto | Categoria administrativa da Instituição de Ensino Superior. |
| area_conhecimento | Texto | Área geral do conhecimento do curso superior. |

---

# Indicadores Quantitativos

| Campo | Tipo | Descrição |
|---|---|---|
| qtd_estudantes | Inteiro | Quantidade total de estudantes ou matrículas no agrupamento. |
| qtd_com_deficiencia | Inteiro | Quantidade de estudantes com deficiência. |
| qtd_usa_transporte_publico | Inteiro | Quantidade de estudantes que utilizam transporte escolar público. |
| qtd_em_escola_com_agua_potavel | Inteiro | Estudantes matriculados em escolas com água potável. |
| qtd_em_escola_com_energia_rede_publica | Inteiro | Estudantes matriculados em escolas com energia da rede pública. |
| qtd_em_escola_com_esgoto_rede_publica | Inteiro | Estudantes matriculados em escolas com rede pública de esgoto. |
| qtd_em_escola_com_internet | Inteiro | Estudantes matriculados em escolas com acesso à internet. |
| qtd_em_escola_com_internet_alunos | Inteiro | Estudantes matriculados em escolas com internet disponível para alunos. |
| qtd_em_escola_com_biblioteca | Inteiro | Estudantes matriculados em escolas com biblioteca. |
| qtd_em_escola_com_biblioteca_sala_leitura | Inteiro | Estudantes matriculados em escolas com biblioteca ou sala de leitura. |
| qtd_em_escola_com_lab_informatica | Inteiro | Estudantes matriculados em escolas com laboratório de informática. |
| qtd_em_escola_com_lab_ciencias | Inteiro | Estudantes matriculados em escolas com laboratório de ciências. |
| qtd_em_escola_com_quadra | Inteiro | Estudantes matriculados em escolas com quadra esportiva. |
| qtd_financiamento | Inteiro | Matrículas do Ensino Superior com financiamento estudantil. |
| qtd_reserva_vaga | Inteiro | Matrículas realizadas por reserva de vagas. |
| qtd_apoio_social | Inteiro | Matrículas de estudantes beneficiados por programas de apoio social. |
| qtd_atividade_extracurricular | Inteiro | Matrículas de estudantes participantes de atividades extracurriculares. |
| qtd_mobilidade_academica | Inteiro | Matrículas de estudantes participantes de programas de mobilidade acadêmica. |

---

# Indicadores Percentuais

| Campo | Tipo | Fórmula Base | Descrição |
|---|---|---|---|
| perc_com_deficiencia | Decimal | `qtd_com_deficiencia / qtd_estudantes` | Percentual de estudantes com deficiência em relação ao total de estudantes. |
| perc_usa_transporte_publico | Decimal | `qtd_usa_transporte_publico / qtd_estudantes` | Percentual de estudantes que utilizam transporte escolar público. |
| perc_em_escola_com_agua_potavel | Decimal | `qtd_em_escola_com_agua_potavel / qtd_estudantes` | Percentual de estudantes em escolas com água potável. |
| perc_em_escola_com_energia_rede_publica | Decimal | `qtd_em_escola_com_energia_rede_publica / qtd_estudantes` | Percentual de estudantes em escolas com energia da rede pública. |
| perc_em_escola_com_esgoto_rede_publica | Decimal | `qtd_em_escola_com_esgoto_rede_publica / qtd_estudantes` | Percentual de estudantes em escolas com esgoto da rede pública. |
| perc_em_escola_com_internet | Decimal | `qtd_em_escola_com_internet / qtd_estudantes` | Percentual de estudantes matriculados em escolas com acesso à internet. |
| perc_em_escola_com_internet_alunos | Decimal | `qtd_em_escola_com_internet_alunos / qtd_estudantes` | Percentual de estudantes em escolas em que a internet está disponível para alunos. |
| perc_em_escola_com_biblioteca | Decimal | `qtd_em_escola_com_biblioteca / qtd_estudantes` | Percentual de estudantes matriculados em escolas com biblioteca. |
| perc_em_escola_com_biblioteca_sala_leitura | Decimal | `qtd_em_escola_com_biblioteca_sala_leitura / qtd_estudantes` | Percentual de estudantes em escolas com biblioteca ou sala de leitura. |
| perc_em_escola_com_lab_informatica | Decimal | `qtd_em_escola_com_lab_informatica / qtd_estudantes` | Percentual de estudantes matriculados em escolas com laboratório de informática. |
| perc_em_escola_com_lab_ciencias | Decimal | `qtd_em_escola_com_lab_ciencias / qtd_estudantes` | Percentual de estudantes em escolas com laboratório de ciências. |
| perc_em_escola_com_quadra | Decimal | `qtd_em_escola_com_quadra / qtd_estudantes` | Percentual de estudantes matriculados em escolas com quadra esportiva. |
| perc_financiamento | Decimal | `qtd_financiamento / qtd_estudantes` | Percentual de matrículas do Ensino Superior com financiamento estudantil. |
| perc_reserva_vaga | Decimal | `qtd_reserva_vaga / qtd_estudantes` | Percentual de matrículas realizadas por reserva de vagas. |
| perc_apoio_social | Decimal | `qtd_apoio_social / qtd_estudantes` | Percentual de matrículas beneficiadas por programas de apoio social. |
| perc_atividade_extracurricular | Decimal | `qtd_atividade_extracurricular / qtd_estudantes` | Percentual de matrículas com participação em atividades extracurriculares. |
| perc_mobilidade_academica | Decimal | `qtd_mobilidade_academica / qtd_estudantes` | Percentual de matrículas com participação em programas de mobilidade acadêmica. |

---

# Regras de Negócio

- O campo `ano` representa o ano de referência da informação educacional.
- O campo `fonte` identifica se o registro pertence ao Censo Escolar ou ao Censo da Educação Superior.
- O campo `nivel_ensino` padroniza os níveis educacionais para facilitar análises integradas.
- Os indicadores quantitativos são calculados por agrupamento analítico.
- Os indicadores percentuais são calculados com base no total de estudantes ou matrículas do respectivo agrupamento.
- As divisões percentuais devem utilizar tratamento contra divisão por zero, preferencialmente com `SAFE_DIVIDE()` no BigQuery.
- Valores nulos devem ser tratados conforme a regra de cada indicador, utilizando `COALESCE()`, `CASE WHEN` ou regra equivalente.
- Nem todos os campos possuem disponibilidade simultânea para Educação Básica e Ensino Superior.
- Campos específicos do Ensino Superior podem aparecer nulos para registros do Censo Escolar.
- Campos específicos de infraestrutura escolar podem aparecer nulos para registros do Ensino Superior.

---

# Aplicação da Base

A base analítica produzida por esta consulta foi desenvolvida para apoiar análises sobre o perfil dos estudantes brasileiros e pode ser utilizada em:

- Business Intelligence;
- Power BI;
- Tableau;
- Looker Studio;
- Qlik Sense;
- Análise Exploratória de Dados;
- Estudos acadêmicos;
- Projetos de Ciência de Dados;
- Projetos de Engenharia de Dados;
- Planejamento e monitoramento de políticas públicas;
- Produção de indicadores educacionais;
- Dashboards gerenciais;
- Análises estatísticas e temporais.

---

# Observações Técnicas

- O período analisado começa em **2015** e termina no ano corrente da execução, usando `EXTRACT(YEAR FROM CURRENT_DATE())`.
- Os dados são provenientes exclusivamente de bases públicas oficiais disponibilizadas pela **Base dos Dados**.
- A consulta integra múltiplas tabelas utilizando **CTEs**, **JOINs**, **agregações**, **tratamento de valores nulos** e **indicadores percentuais**.
- A base foi projetada para consumo analítico em ferramentas de BI.
- O modelo permite análises por ano, região, estado, município, nível de ensino, rede, sexo, raça/cor, faixa etária e demais dimensões disponíveis.
- O desenvolvimento contou com apoio de **Inteligência Artificial** para revisão da lógica, identificação de inconsistências, melhoria da estrutura SQL e documentação técnica.
- A validação final das consultas e dos resultados foi realizada manualmente no Google BigQuery.

---

# Autor

**Marcelo dos Santos Sampaio**

Projeto desenvolvido para fins de estudo e portfólio em SQL Analítico, Engenharia de Dados, Business Intelligence e análise de dados públicos brasileiros.
