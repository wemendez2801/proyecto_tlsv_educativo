import numpy as np
import mediapipe as mp
import cv2

# Función para inicializar la cámara con diferentes backends
def initialize_camera(camera_index=0):
    """ cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot access camera.")
        exit() """

    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF]
    cap = None

    for backend in backends:
        temp_cap = cv2.VideoCapture(camera_index, backend)
        if temp_cap.isOpened():
            print(f"Cámara inicializada con backend {backend}.")
            cap = temp_cap
            break
        else:
            temp_cap.release()  # Libera el recurso si falla

    if cap is None:
        print("Error: No se puede acceder a la cámara con ninguno de los backends disponibles.")
        exit()
    
    return cap

# Dibuja los landmarks detectados en la imagen
def draw_landmarks(image, results):
    # Landmarks de mano izquierda
    mp.solutions.drawing_utils.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
    # Landmarks de mano derecha
    mp.solutions.drawing_utils.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)

# Procesa las imagenes para obtener los landmarks de la seña realizada
def image_process(image, model):

    def image_process(image, model):
        if image is None:
            print("Error: La imagen recibida no es valida")
            return None  # Devuelve None en lugar de fallar

    image.flags.writeable = False 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return results

# Extrae puntos clave de los landmarks de las manos
def keypoint_extraction(results):
    # Extrae los puntos de la mano izquierda o devolvera ceros
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(63)
    # Extrae los puntos de la mano derecha o devolvera ceros
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(63)
    # Concatena los puntos clave para cada mano
    keypoints = np.concatenate([lh, rh])
    return keypoints