import pickle
import cv2
import mediapipe as mp
import numpy as np
from funciones import *

# Cargar el modelo entrenado
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Inicializar la cámara
cap = initialize_camera()

# Configuración de MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Diccionario de etiquetas
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

# Bucle de captura de video
while True:
    data_aux = []
    x_ = []
    y_ = []

    # Capturar un frame de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame.")
        break

    # Voltear la imagen horizontalmente para corregir inversión
    frame = cv2.flip(frame, 1)  # Eliminar esta línea si la cámara ya no invierte la imagen

    H, W, _ = frame.shape

    # Convertir a RGB para MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen para detectar manos
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar los landmarks de la mano
            mp_drawing.draw_landmarks(
                frame,  # Imagen donde se dibuja
                hand_landmarks,  # Output del modelo
                mp_hands.HAND_CONNECTIONS,  # Conexiones de la mano
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        # Normalizar las coordenadas
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        # Calcular la caja delimitadora (bounding box)
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Hacer la predicción del modelo
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]

        # Dibujar el rectángulo y el texto de la predicción
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 250, 0), 3,
                    cv2.LINE_AA)

    # Mostrar el frame procesado
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir con 'q'
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()