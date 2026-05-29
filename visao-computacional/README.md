# 🛰️ Jamestown Hub - Applied Computer Vision

Este repositório contém a lógica de treinamento da Rede Neural Convolucional (CNN) focada no diagnóstico botânico automatizado (identificação de fungos e estresse nas plantas) da base lunar Jamestown.

## ⚙️ Pré-Requisitos e Setup Local

Para rodar a Inteligência Artificial na sua própria máquina sem o Google Colab:

1. **Ativar o Ambiente e Instalar Bibliotecas**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # (Windows)
   pip install -r requirements.txt
   ```

2. **Configuração do Kaggle (Essencial)**:
Para que o download funcione, você precisa colocar o seu arquivo kaggle.json (gerado na sua conta Kaggle) na pasta do seu usuário do PC:
- Windows: C:\Users\SEU_USUARIO\.kaggle\kaggle.json
- Linux/Mac: ~/.kaggle/kaggle.json

3. **Rodar a Pipeline de Treinamento**:
```bash
python main.py
```

O script irá automaticamente baixar as imagens, fazer o tratamento/divisão e rodar as épocas de treinamento, gerando o arquivo cnn_jamestown.keras no final.