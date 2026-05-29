import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

IMG_SIZE = (128, 128)
BATCH_SIZE = 32

def create_data_generators(split_path='./jamestown_split'):
    # cria lotes de imagens alimentando-os diretamente pro Keras
    train_datagen = ImageDataGenerator(
        rescale=1./255, rotation_range=15, zoom_range=0.1, 
        horizontal_flip=True, brightness_range=[0.8, 1.2]
    )
    val_test_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        f'{split_path}/train', target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', seed=42)
    val_gen = val_test_datagen.flow_from_directory(
        f'{split_path}/val', target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', seed=42)
    test_gen = val_test_datagen.flow_from_directory(
        f'{split_path}/test', target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', shuffle=False, seed=42)
    
    return train_gen, val_gen, test_gen

def build_model():
    # arquitetura da CNN
    cnn = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.4),
        Dense(3, activation='softmax')
    ], name='CNN_A_Leve')

    cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return cnn

def train_and_save(model, train_gen, val_gen, save_path='cnn_jamestown.keras'):
    # loop de treino da IA com salvamento do arquivo treinado
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
    
    print("Iniciando treinamento da CNN...")
    history = model.fit(train_gen, epochs=30, validation_data=val_gen, callbacks=[early_stop], verbose=1)
    
    model.save(save_path)
    print(f"Modelo salvo em {save_path}!")
    return history