import os
from dataset_handler import download_dataset, prepare_and_split_data
from model import create_data_generators, build_model, train_and_save

def main():
    print("--- Pipeline de Treinamento Jamestown Hub ACV ---")
    
    # 1. preparação dos Dados
    if not os.path.exists('./plantvillage'):
        download_dataset()
    if not os.path.exists('./jamestown_split'):
        prepare_and_split_data()

    # 2. configuração dos geradores e rede neural
    train_gen, val_gen, test_gen = create_data_generators()
    print("Classes Mapeadas:", train_gen.class_indices)

    model = build_model()
    model.summary()

    # 3. execução
    train_and_save(model, train_gen, val_gen)

if __name__ == '__main__':
    main()