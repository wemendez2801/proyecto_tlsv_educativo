import numpy as np
import os
import string
import mediapipe as mp
import cv2
import keyboard
from tensorflow.keras.models import load_model
from funciones import *

PATH = os.path.join('data')

actions = np.array(os.listdir(PATH))

# Carga el modelo entrenado
model = load_model('my_model.keras')

# Inicializa las listas
sentence, keypoints, last_prediction = [], [], []

# Abre la camara
cap = initialize_camera()

# Crea un objeto holistico para reconocer señas
with mp.solutions.holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
    # Bucle mientras la camara este activa
    while cap.isOpened():
        # Lee un frame de la camara
        _, image = cap.read()
        # Procesa la imagen y obtiene los landmarks
        results = image_process(image, holistic)
        # Dibuja los landmarks de la imagen
        image = image.copy()  
        draw_landmarks(image, results)
        # Extrae puntos claves de los landmarks
        keypoints.append(keypoint_extraction(results))

        # Revisa si se acumularon 10 frames
        if len(keypoints) == 10:
            # Convierte lista de keypoints en arreglo numpy
            keypoints = np.array(keypoints)
            # Predice en base de los keypoints guardados
            prediction = model.predict(keypoints[np.newaxis, :, :])
            # Limpia la lista de keypoints para la siguiente prediccion
            keypoints = []

            # Revisa si el valor maximo de prediccion es mayor a 0.9
            if np.amax(prediction) > 0.9:
                # Revisa si la seña predicha es diferente a la anterior
                if last_prediction != actions[np.argmax(prediction)]:
                    sentence.append(actions[np.argmax(prediction)])
                    last_prediction = actions[np.argmax(prediction)]

        # Limita la oracion a 7 palabras
        if len(sentence) > 5:
            sentence = sentence[-5:]

        # Resetea si se presiona Espacio 
        if keyboard.is_pressed(' '):
            sentence, keypoints, last_prediction = [], [], []

        if sentence:
            # Primera letra mayuscula
            sentence[0] = sentence[0].capitalize()

        if len(sentence) >= 2:
            # Revisa si el ultimo elemento de una oracion pertenece al alfabeto
            if sentence[-1] in string.ascii_lowercase or sentence[-1] in string.ascii_uppercase:
                # Revisa si el penultimo elemento de una oracion pertenece al alfabeto o es una nueva palabra
                if sentence[-2] in string.ascii_lowercase or sentence[-2] in string.ascii_uppercase or (sentence[-2] not in actions and sentence[-2] not in list(x.capitalize() for x in actions)):
                    # Combina los ultimos dos elementos
                    sentence[-1] = sentence[-2] + sentence[-1]
                    sentence.pop(len(sentence) - 2)
                    sentence[-1] = sentence[-1].capitalize()
        
        textsize = cv2.getTextSize(' '.join(sentence), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_X_coord = (image.shape[1] - textsize[0]) // 2

        image = image.copy()

        # Dibujar el texto en la imagen
        cv2.putText(image, ' '.join(sentence), (text_X_coord, 470),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Se muestra la imagen en camara
        cv2.imshow('Camera', image)

        cv2.waitKey(1)

        if cv2.getWindowProperty('Camera',cv2.WND_PROP_VISIBLE) < 1:
            break

    # Se cierran las ventanas
    cap.release()
    cv2.destroyAllWindows()