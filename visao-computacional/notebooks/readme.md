# 📉 GS_ACV - Análise e Prova Científica

Este diretório contém os estudos acadêmicos e a prova científica do nosso modelo de Deep Learning; ele é responsável por ser os "olhos" da nossa estufa lunar simulada. Através de uma **Rede Neural Convolucional (CNN)**, o modelo analisa imagens capturadas das folhas das plantas hidropônicas e realiza diagnósticos autônomos de saúde e pragas, essenciais para a sobrevivência a longo prazo no espaço.

Para testar a rede neural interativamente, faça o upload do arquivo GS_ACV.ipynb no Google Colab e siga as instruções das células.

## 👥 Equipe Desenvolvedora - 4ESPW
* **Breno Silva** - *RM99275*
* **Eduardo Araujo** - *RM99758*
* **Gabriela Trevisan** - *RM99500*
* **Gustavo Akio** - *RM550241*
* **Rafael Franck** - *RM550875*

## 🎯 Objetivo e Diagnósticos (Classes)
O modelo foi treinado com o dataset PlantVillage (via Kaggle) e mapeado para agrupar doenças em três macro-categorias críticas de risco operacional:

* `0`: **Saudável** (Planta em condições ideais)
* `1`: **Estresse Hídrico/Nutricional** (Sintomas de doenças iniciais, ácaros, manchas foliares)
* `2`: **Fungo Patógeno / Risco Crítico** (Pragas altamente infecciosas que requerem contenção imediata)

## 📂 Estrutura do Repositório

O repositório está focado na etapa de **Pesquisa e Desenvolvimento (P&D)** da Inteligência Artificial:

* `GS_ACV.ipynb`: O Jupyter Notebook principal. Contém o pipeline completo de IA: download do dataset, data augmentation, construção das camadas da CNN, treinamento, validação e matriz de confusão.
* `evidencias/`: Pasta contendo os artefatos visuais gerados pelo modelo:
  * Gráficos de Histórico de Treinamento (Acurácia e Loss).
  * Matriz de Confusão do modelo final.
  * Imagens de teste para as 3 categorias (`exemplo_saudavel.jpg`, `exemplo_estresse.jpg`, `exemplo_fungo_patogeno.jpg`).
* `jamestown_sample_output.json`: Exemplo da estrutura do payload JSON gerado pelo modelo (utilizado para integração).
* `requirements.txt`: Lista de dependências Python necessárias para rodar o notebook.

## 🚀 Como Executar o Projeto (Google Colab)

A forma mais rápida e recomendada de testar este modelo é através do Google Colab, aproveitando a aceleração de GPU em nuvem:

1. Acesse o [Google Colab](https://colab.research.google.com/).
2. Faça o upload do arquivo `GS_ACV.ipynb`.
3. **Configuração da API do Kaggle (Importante):** O notebook faz o download automático do dataset. Para isso, você precisará ter o seu arquivo de token `kaggle.json` (gerado na sua conta do Kaggle) e fazer o upload quando a célula inicial solicitar.
4. Execute as células sequencialmente (`Shift + Enter`).
5. Ao final, haverá uma célula interativa onde você poderá fazer o upload de uma folha (utilize as imagens da pasta `/evidencias`) para ver a Inteligência Artificial classificando a doença em tempo real!

## 🔗 Integração com o Ecossistema Jamestown

Este modelo de Deep Learning atua como a primeira camada de inteligência da base Jamestown. 

Na arquitetura completa do projeto, o diagnóstico (gerado em arquivo JSON) é consumido por nossa esteira de **Big Data (Apache Airflow)**. Lá, o status de saúde da planta é cruzado com métricas de Sensores IoT (Temperatura, Umidade, pH) e alertas de Clima Espacial (API da NASA), formando uma base de dados robusta para tomada de decisão do comandante e ação de robôs de contenção.