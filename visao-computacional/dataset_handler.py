import os
import shutil
import random
import subprocess
from pathlib import Path

def download_dataset():
    # baixando dataset pela API do Kaggle nativa via linha de comando
    print("Iniciando download do dataset do Kaggle...")
    # roda o comando nativo do sistema
    subprocess.run(["kaggle", "datasets", "download", "-d", "emmarex/plantdisease", "-p", "./plantvillage", "--unzip", "-q"])
    print("Download concluído!")

def prepare_and_split_data():
    # organiza as pastas originais para as 3 categorias e cria os splits
    random.seed(42)
    
    mapeamento = {
        'saudavel': ['Pepper__bell___healthy', 'Potato___healthy', 'Tomato_healthy'],
        'estresse': ['Potato___Early_blight', 'Potato___Late_blight', 'Tomato_Early_blight', 
                     'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Spider_mites_Two_spotted_spider_mite'],
        'fungo_patogeno': ['Pepper__bell___Bacterial_spot', 'Tomato_Bacterial_spot', 'Tomato_Septoria_leaf_spot', 
                           'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus']
    }

    base_path = './plantvillage/PlantVillage'
    source_path = './jamestown_dataset'
    split_path = './jamestown_split'
    classes = ['saudavel', 'estresse', 'fungo_patogeno']

    # 1. copiar as imagens mapeadas
    print("Unificando as classes...")
    for classe in mapeamento:
        Path(f'{source_path}/{classe}').mkdir(parents=True, exist_ok=True)

    for classe, pastas in mapeamento.items():
        for pasta in pastas:
            origem = f'{base_path}/{pasta}'
            if os.path.exists(origem):
                for img in os.listdir(origem):
                    if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                        shutil.copy(f'{origem}/{img}', f'{source_path}/{classe}/{img}')

    # 2. fazer o split
    MAX_POR_CLASSE = 3000
    SPLIT = {'train': 0.70, 'val': 0.15, 'test': 0.15}

    print("Criando diretórios de Treino, Validação e Teste...")
    for split in SPLIT:
        for classe in classes:
            Path(f'{split_path}/{split}/{classe}').mkdir(parents=True, exist_ok=True)

    for classe in classes:
        imagens = os.listdir(f'{source_path}/{classe}')
        imagens = [i for i in imagens if i.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(imagens)
        imagens = imagens[:MAX_POR_CLASSE] 

        n = len(imagens)
        n_train = int(n * 0.70)
        n_val   = int(n * 0.15)

        splits = {
            'train': imagens[:n_train],
            'val':   imagens[n_train:n_train + n_val],
            'test':  imagens[n_train + n_val:]
        }

        for split, arquivos in splits.items():
            for arquivo in arquivos:
                shutil.copy(f'{source_path}/{classe}/{arquivo}', f'{split_path}/{split}/{classe}/{arquivo}')
                
    print("Separação das imagens concluída!")