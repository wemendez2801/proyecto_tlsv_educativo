import numpy as np
import mediapipe as mp
import cv2
import time

# Función para inicializar la cámara con diferentes backends
def initialize_camera(camera_index=0):
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
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
    
    # Espera 2 segundos para que la cámara se inicialice correctamente
    time.sleep(2)
    return cap

# Dibuja los landmarks detectados en la imagen
def draw_landmarks(image, results):
    # Landmarks de mano izquierda
    mp.solutions.drawing_utils.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
    # Landmarks de mano derecha
    mp.solutions.drawing_utils.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)

# Procesa las imagenes para obtener los landmarks de la seña realizada
def image_process(image, model):
    if image is None:
        print("Error: La imagen recibida no es válida.")
        return None
    if model is None:
        print("Error: El modelo no ha sido inicializado.")
        return None

    # Crear una copia de la imagen para no modificar la original
    image_copy = image.copy()

    # Convertir la imagen a RGB
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con el modelo de Mediapipe
    results = model.process(image_copy)

    # Convertir la imagen de vuelta a BGR
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_RGB2BGR)

    return results

# Extrae puntos clave de los landmarks de las manos
def keypoint_extraction(results):
    """Extrae los keypoints de ambas manos y devuelve un vector de tamaño fijo (126 valores)."""
    keypoints = np.zeros(126)  # Vector de ceros para asegurar tamaño constante
    
    if results.left_hand_landmarks:
        left_hand = np.array([[lmk.x, lmk.y, lmk.z] for lmk in results.left_hand_landmarks.landmark]).flatten()
        keypoints[:len(left_hand)] = left_hand  # Llenar con los valores reales
    
    if results.right_hand_landmarks:
        right_hand = np.array([[lmk.x, lmk.y, lmk.z] for lmk in results.right_hand_landmarks.landmark]).flatten()
        keypoints[63:63+len(right_hand)] = right_hand  # Colocar en la segunda mitad del vector
    
    return keypoints