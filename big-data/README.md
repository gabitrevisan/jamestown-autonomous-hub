# 📊 Big Data - Pipeline de Telemetria

Orquestração de dados da base lunar utilizando Apache Airflow, PostgreSQL e Redis.

## 👥 Equipe Desenvolvedora - 4ESPW
* **Breno Silva** - *RM99275*
* **Eduardo Araujo** - *RM99758*
* **Gabriela Trevisan** - *RM99500*
* **Gustavo Akio** - *RM550241*
* **Rafael Franck** - *RM550875*

## 🏗️ Arquitetura de Pipeline
Este pipeline ingere dados de sensores IoT, o JSON gerado pela Visão Computacional e monitora alertas climáticos da API da NASA.

## 🚀 Como Executar
1. Garanta que o Docker Desktop esteja em execução.
2. Na pasta raiz deste módulo, suba o ambiente: `docker compose up -d`
3. Acompanhe a orquestração: Acesse `http://localhost:8081` (Usuário: `airflow` / Senha: `airflow`).
4. **Configuração:** Em *Admin > Connections*, crie a conexão `oracle_fiap` para persistência dos dados.