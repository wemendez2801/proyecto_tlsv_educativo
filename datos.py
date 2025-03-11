import os
import numpy as np
import cv2
import mediapipe as mp
import keyboard
from itertools import product
from funciones import *

# Define las acciones (señas) de las que se capturaran las imagenes
actions = np.array([
    'yo','tu', 'el', 'nosotros', 'ustedes', 
    'hola','adios','gracias', 'buen', 'dia', 'por favor', 'permiso', 'perdon', 'bienvenidos',
    'que','quien','por que', 'cuando', 'cuanto', 'como','cual','pregunta', 'respuesta',
    'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo',
    'enero','febrero', 'marzo','abril','mayo','junio', 'julio', 'agosto', 'septiembre','octubre', 'noviembre','diciembre',
    'hoy', 'ayer', 'semana',
    'materia','biologia','fisica','matematica','castellano','geografia', 'informatica','ingles',
    'estudiar','aprender','aprobar', 'ayuda', 'entender', 'explicar', 'haber', 'hacer', 'ir','saber',
    'practicar', 'prestar', 'poder','leer','repetir','usar','tener','tengo','ver','necesitar','encontrar',
    'profesor','grupo','coordinador','director',
    'cuaderno','hoja','notas', 'transporte', 'lapiz', 'libro', 'lista',
    'casa','universidad',
    'educacion','tareas','proyecto','semestre','certificado','clase','examen','exposicion','ejemplo','experimento'
    ])

# Define el numero de secuencias y frames que se capturaran por cada accion
sequences = 30
frames = 20

# Ruta de almacenamiento del dataset
PATH = os.path.join('data')

# Directorios para cada accion, secuencia y frame
for action, sequence in product(actions, range(sequences)):
    try:
        os.makedirs(os.path.join(PATH, action, str(sequence)))
    except:
        pass

# Inicializar la cámara
cap = initialize_camera()
if cap is None:
    print("Error: No se pudo inicializar la cámara.")
    exit()

# Creacion de objeto de Mediapipe Holistic para deteccion de las manos
DETECTION_CONFIDENCE = 0.75
TRACKING_CONFIDENCE = 0.75

with mp.solutions.holistic.Holistic(
    min_detection_confidence=DETECTION_CONFIDENCE, 
    min_tracking_confidence=TRACKING_CONFIDENCE
) as holistic:

    # Bucle en cada accion, secuencia y frame para captar datos
    for action, sequence, frame in product(actions, range(sequences), range(frames)):
        # Se espera por la barra espaciadora para empezar
        if frame == 0: 
            while True:
                if keyboard.is_pressed(' '):
                    break
                _, image = cap.read()
                if image is None:
                    print("Error: No se pudo capturar un frame de la cámara.")
                    break

                results = image_process(image, holistic)
                image.flags.writeable = True
                draw_landmarks(image, results)

                cv2.putText(image, 'Guardando datos para "{}". Secuencia numero {}.'.format(action, sequence),
                            (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                cv2.putText(image, 'Pausa.', (20,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Presiona Espacio cuando estes listo', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.imshow('Camera', image)
                cv2.waitKey(1)
                
                # Revisa si la camara esta cerrada para continuar o romper el ciclo
                if cv2.getWindowProperty('Camera',cv2.WND_PROP_VISIBLE) < 1:
                    break
        else:
            # Para frames posteriores, se lee la imagen captada en camara
            _, image = cap.read()
            # Procesa la imagen y extrae los landmarks
            results = image_process(image, holistic)
            image.flags.writeable = True  # Habilitar escritura para OpenCV
            # Dibuja los landmarks de la mano captada
            draw_landmarks(image, results)

            # Texto para indicar la imagen y secuencia grabada
            cv2.putText(image, 'Guardando datos para "{}". Secuencia numero {}.'.format(action, sequence),
                (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow('Camera', image)
            cv2.waitKey(1)

        if cv2.getWindowProperty('Camera',cv2.WND_PROP_VISIBLE) < 1:
             break

        # Extrae landmarks de ambas manos y los guarda en arreglos
        keypoints = keypoint_extraction(results)
        frame_path = os.path.join(PATH, action, str(sequence), str(frame))
        np.save(frame_path, keypoints)

    cap.release()
    cv2.destroyAllWindows()