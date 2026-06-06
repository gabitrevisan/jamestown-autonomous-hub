# 📊 Big Data - Pipeline de Telemetria e Integração Jamestown

Este módulo é o coração analítico do projeto, responsável pela ingestão, processamento e persistência dos dados de telemetria da estufa e dos diagnósticos gerados pela Visão Computacional.

## 👥 Equipe Desenvolvedora - 4ESPW
* **Breno Silva** - *RM99275*
* **Eduardo Araujo** - *RM99758*
* **Gabriela Trevisan** - *RM99500*
* **Gustavo Akio** - *RM550241*
* **Rafael Franck** - *RM550875*

## 🏗️ Arquitetura do Pipeline (ETL)
O fluxo de dados foi desenhado para ser resiliente e automatizado:
1. **Extração (E):** Ingestão de telemetria bruta via CSV (`telemetry_greenhouse.csv`) e diagnósticos de pragas via JSON (`vision_diagnosis.json`).
2. **Transformação (T):** Utilização de Pandas para realizar a limpeza, tratamento de valores nulos e merge entre os dados de sensores IoT e o status da planta (CNN).
3. **Carga (L):** Persistência dos dados consolidados no banco de dados relacional **Oracle** (servidor FIAP), garantindo a integridade histórica.



## 🛠️ Tecnologias Utilizadas
* **Orquestração:** Apache Airflow.
* **Processamento:** Python (Pandas).
* **Infraestrutura:** Docker e Docker Compose.
* **Banco de Dados:** Oracle SQL (persistência final).

## 🚀 Como Executar
1. **Setup:** Garanta que o Docker Desktop esteja em execução.
2. **Ambiente:** Na pasta `big-data/`, suba os serviços:
   ```bash
   docker compose up -d
   ```

3. **Orquestração:** Acesse o painel do Airflow em http://localhost:8081.
- Usuário/Senha: airflow.
- Ative a DAG jamestown_mission_pipeline para iniciar o fluxo ETL.
4. **Verificação:** Consulte a tabela FACT_JAMESTOWN_DATA no Oracle para validar a carga.

## 📈 Validação de Dados
Os dados processados são auditados via SQL para garantir a integridade da Estufa Lunar. Consultas analíticas (incluindo cruzamento com alertas da NASA) estão disponíveis no arquivo `schema.sql`.

## 🖼️ Evidências de Funcionamento
As evidências de execução da pipeline e a persistência no banco de dados encontram-se na pasta `evidencias/`.