# 🛰️ Jamestown Hub - Pipeline de Big Data & Analytics

Este repositório contém a infraestrutura de Engenharia de Dados (Pipeline ETL) desenvolvida para a base lunar simulada **Jamestown Hub**. O projeto é responsável por orquestrar, tratar e armazenar dados vitais das estufas espaciais.

## 👥 Equipe Desenvolvedora - 4ESPW
* **Breno Silva** - *RM99275*
* **Eduardo Araujo** - *RM99758*
* **Gabriela Trevisan** - *RM99500*
* **Gustavo Akio** - *RM550241*
* **Rafael Franck** - *RM550875*

## 🏗️ Arquitetura do Projeto

O fluxo de dados foi construído para simular um ambiente real de tomada de decisão em Missões Espaciais (Cyber-Physical System):

1. **Extração (Extract):** - Arquivos locais (`CSV` e `JSON`) simulando a telemetria de sensores IoT e diagnósticos de Visão Computacional (IA).
   - Consumo em tempo real da **API DONKI da NASA** para monitoramento de Clima Espacial (Tempestades Solares/Radiação).
2. **Transformação (Transform):** - Utilização de `Pandas` via **Apache Airflow** para higienização de dados (tratamento de valores nulos, conversão de formatos de data/hora e cruzamento de bases).
3. **Carga (Load):** - Inserção dos dados estruturados em uma tabela Fato (`FACT_JAMESTOWN_DATA`) no banco de dados **Oracle**.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Orquestração:** Apache Airflow 2.9.1
* **Manipulação de Dados:** Pandas
* **Infraestrutura:** Docker & Docker Compose
* **Banco de Dados:** Oracle Database
* **Linguagem de Consulta:** SQL Avançado

## 📂 Estrutura do Repositório

```text
jamestown_airflow/
├── dags/
│   ├── jamestown_pipeline.py       # Código oficial da DAG do Airflow
│   ├── telemetry_greenhouse.csv    # Mock Data: Sensores IoT da estufa
│   └── vision_diagnosis.json       # Mock Data: Diagnósticos da Inteligência Artificial
├── sql/
│   └── analytical_queries.sql      # Script com DDL da tabela e as 5 consultas analíticas
├── docker-compose.yaml             # Configuração da infraestrutura do Airflow
├── .gitignore                      # Arquivos ignorados pelo Git
└── README.md                       # Documentação do projeto
```

## 🚀 Como executar este projeto localmente
Para que qualquer membro da equipe consiga rodar o Airflow e testar a DAG em sua própria máquina, siga os passos abaixo:

1. Pré-requisitos
Ter o Docker Desktop instalado e rodando.

Ter o Git instalado.

2. Clonando e Configurando
1) Clone este repositório:

```bash
git clone [https://github.com/SEU_USUARIO/jamestown_hub_bigdata.git](https://github.com/SEU_USUARIO/jamestown_hub_bigdata.git)
cd jamestown_hub_bigdata
```

2) Crie um arquivo .env na raiz do projeto. (Este arquivo é ignorado pelo Git por segurança). Ele deve conter exatamente o seguinte conteúdo:

```bash
AIRFLOW_UID=50000
_PIP_ADDITIONAL_REQUIREMENTS=apache-airflow==2.9.1 apache-airflow-providers-oracle pandas requests
```

3. Subindo a Infraestrutura
Abra o terminal na pasta do projeto e execute:

```bash
docker compose up -d
```

Nota: A primeira execução pode levar até 5 minutos para instalar as dependências do Python dentro do contêiner.

4. Acessando o Airflow e Banco de Dados
- Interface Web do Airflow: Acesse http://localhost:8080 (Usuário: airflow / Senha: airflow).
- Conexão Oracle: Antes de rodar a DAG, é necessário configurar a conexão com o banco de dados dentro do Airflow navegando até Admin > Connections e criando uma conexão ID oracle_fiap com as credenciais da FIAP.

## 📊 Análise de Dados (Business Intelligence)
Os dados gerados por este pipeline alimentam diretamente as ferramentas de BI e RPA da equipe. As consultas analíticas completas para a geração de gráficos de suporte à vida e alertas de saúde botânica encontram-se no diretório /sql.