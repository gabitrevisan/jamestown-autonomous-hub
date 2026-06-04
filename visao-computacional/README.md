# 👁️ Visão Computacional - Diagnóstico Botânico

Módulo responsável pela classificação de saúde das plantas da Estufa Jamestown.

## 👥 Equipe Desenvolvedora - 4ESPW
* **Breno Silva** - *RM99275*
* **Eduardo Araujo** - *RM99758*
* **Gabriela Trevisan** - *RM99500*
* **Gustavo Akio** - *RM550241*
* **Rafael Franck** - *RM550875*

## 🛠️ Tecnologias
- Python 3.12, TensorFlow/Keras, OpenCV.

## 🚀 Como Executar
1. **Ambiente:** Ative seu venv e instale os requisitos: `pip install -r notebooks/requirements.txt`
2. **Treinamento:** Execute `python main.py` para treinar a CNN.
3. **Inferência:** Utilize `python predict.py <caminho_da_imagem>` para diagnosticar uma planta. 
   - *O resultado é gerado automaticamente em `../big-data/dags/vision_diagnosis.json` para integração com o pipeline de Big Data.*