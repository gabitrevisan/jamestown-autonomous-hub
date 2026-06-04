# 🛰️ Jamestown Hub - Generative AI for Engineering

Este módulo atua como o "Conselheiro" e Assistente Especialista da base lunar Jamestown. 

Ao invés de depender exclusivamente de dashboards estáticos, a tripulação pode interagir em linguagem natural com este agente de Inteligência Artificial. Ele consome os dados físicos da estufa e os diagnósticos botânicos e utiliza **Large Language Models (LLMs)** para gerar relatórios e recomendações científicas instantâneas.

## 👥 Equipe Desenvolvedora - 4ESPW
* **Breno Silva** - *RM99275*
* **Eduardo Araujo** - *RM99758*
* **Gabriela Trevisan** - *RM99500*
* **Gustavo Akio** - *RM550241*
* **Rafael Franck** - *RM550875*

## 📂 Organização do Módulo

Para demonstrar o ciclo de vida completo de desenvolvimento de IA, dividimos o projeto em:

* **`/notebooks`**: Contém o Jupyter Notebook de prototipação original (`Cópia de Untitled16.ipynb`). Nele constam os testes iniciais com geração de dados sintéticos via Pandas e deploy via LocalTunnel/Streamlit.
* **`assistant.py`**: O script de Produção refatorado. Este código foi otimizado para a arquitetura em **Monorepo**.

## 🔗 Integração no Ecossistema

O diferencial arquitetural deste módulo é que ele **não utiliza dados fictícios**. O script `assistant.py` está configurado para ler automaticamente o arquivo de predição (`vision_diagnosis.json`) gerado na pasta `/big-data/dags` pelo módulo de **Visão Computacional**. 

Isso garante que quando a tripulação pergunta à IA: *"Como estão as plantas do módulo GH-01?"*, o modelo **Gemini** (Google) constrói sua resposta embasado nos dados exatos capturados pelas câmeras e higienizados pelo **Apache Airflow**.

## 🚀 Como testar localmente

1. Certifique-se de ter instalado os pacotes: `pip install -r requirements.txt`
2. Configure sua chave do Google Gemini (adicione a chave na variável do código ou crie um arquivo `.env`).
3. Execute no terminal:
   ```bash
   python assistant.py
```