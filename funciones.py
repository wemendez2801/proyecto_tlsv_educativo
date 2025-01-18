import cv2

# Función para inicializar la cámara con diferentes backends
def initialize_camera(camera_index=0):
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF]
    for backend in backends:
        cap = cv2.VideoCapture(camera_index, backend)
        if cap.isOpened():
            print(f"Cámara inicializada con backend {backend}.")
            return cap
    print("Error: No se puede acceder a la cámara con ninguno de los backends disponibles.")
    exit()