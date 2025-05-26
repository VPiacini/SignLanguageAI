import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

# Carrega o modelo treinado
model = load_model("asl_model.keras")

# Tamanho esperado pelo modelo
IMG_SIZE = (224, 224)

# Classes (ordenadas alfabeticamente)
class_names = sorted([
    folder for folder in os.listdir("asl_dataset")
    #folder for folder in os.listdir("dataset/asl_alphabet_train/asl_alphabet_train")
    if not folder.startswith(".")
])

def preprocess_frame(frame):
    img = cv2.resize(frame, IMG_SIZE)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Inicia webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

frame_count = 0  # contador de frames

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Região de interesse
    x1, y1, x2, y2 = 100, 100, 300, 300
    roi = frame[y1:y2, x1:x2]

    # Só processa a cada 5 frames
    if frame_count % 5 == 0:
        img_input = preprocess_frame(roi)
        predictions = model.predict(img_input)[0]
        top_indices = predictions.argsort()[-3:][::-1]
        top_preds = [(class_names[i], predictions[i]) for i in top_indices]

    # Mostra predições mais recentes (a cada 5 frames)
    if frame_count >= 5:
        for i, (label, prob) in enumerate(top_preds):
            text = f"{label}: {prob:.2f}"
            cv2.putText(frame, text, (x1, y2 + 30 + i*30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("ASL Recognition - Top 3", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
