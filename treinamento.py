import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from modelo import build_model  # modelo será definido em model.py
from tensorflow.keras.callbacks import EarlyStopping

# Caminhos dos dados
BASE_TRAIN_DIR = "asl_dataset"
#BASE_TRAIN_DIR = "dataset/asl_alphabet_train/asl_alphabet_train"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50

# Gerador de imagens com divisão treino/validação
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=EPOCHS // 10,
        restore_best_weights=True
    )

train_generator = train_datagen.flow_from_directory(
    BASE_TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = train_datagen.flow_from_directory(
    BASE_TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)

# Modelo
model = build_model(
    input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    num_classes=train_generator.num_classes
)

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    callbacks=[early_stopping]
)

# Salvar
model.save("asl_model.keras")
print("Modelo salvo como asl_model.keras")
