import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json
import sys
import os

def predict_image(img_path, model_path='cnn_jamestown.keras'):
    print(f"Analisando a imagem: {img_path}...")
    
    # 1. carrega o "cérebro" que foi treinado
    if not os.path.exists(model_path):
        print(f"Erro: Modelo {model_path} não encontrado. Rode o main.py primeiro!")
        return

    model = tf.keras.models.load_model(model_path)
    
    # 2. prepara a imagem exatamente como foi feito no treino
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # normaliza os pixels

    # 3. predição matemática
    predictions = model.predict(img_array)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))
    
    '''IMPORTANTE!!! a ordem das classes costuma ser alfabética no Keras, ou seja: estresse (0), fungo_patogeno (1), saudavel (2)
    por outro lado, Big Data espera: 0=Saudável, 1=Estresse, 2=Fungo; esse bloco faz uma tradução para o Airflow não quebrar'''
    
    if predicted_class_idx == 2:   # Keras achou Saudável
        bd_class_id = 0
        status = "Saudável"
    elif predicted_class_idx == 0: # Keras achou Estresse
        bd_class_id = 1
        status = "Estresse Hídrico/Nutricional"
    else:                          # Keras achou Fungo
        bd_class_id = 2
        status = "Fungo Patógeno"

    # 4. gera o arquivo JSON exato que o Airflow está esperando ler
    resultado = {
        "module_id": "GH-01", 
        "timestamp": "2026-05-28T12:00:00Z", # mock datatime
        "predicted_class": bd_class_id,
        "confidence": round(confidence, 4)
    }
    
    # salva o JSON na mesma pasta (ou joga direto na pasta /data do Airflow)
    with open('vision_diagnosis.json', 'w') as f:
        json.dump(resultado, f, indent=4)
        
    print(f"\n--- DIAGNÓSTICO CONCLUÍDO ---")
    print(f"Resultado: {status} (Confiança: {confidence*100:.2f}%)")
    print(f"O arquivo 'vision_diagnosis.json' foi gerado e está pronto para o Airflow!")

if __name__ == "__main__":
    # como rodar no terminal: python predict.py folha_teste.jpg
    if len(sys.argv) > 1:
        caminho_da_foto = sys.argv[1]
        predict_image(caminho_da_foto)
    else:
        print("Uso correto: python predict.py caminho/para/imagem.jpg")