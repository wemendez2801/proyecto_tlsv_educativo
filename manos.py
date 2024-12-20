import cv2
import mediapipe as mp
import time

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

# Inicializar la cámara
cap = initialize_camera()

# Inicialización de Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, 
                      min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Variables para calcular FPS
pTime = 0

try:
    while True:
        success, img = cap.read()
        if not success:
            print("No se pudo leer la imagen de la cámara.")
            break
        
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                finger_ids = [4, 8, 12, 16, 20]  # IDs de las puntas de los dedos
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id in finger_ids:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                # Dibuja la mano y las conexiones
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # Cálculo de FPS
        """ 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime 
        """

        # Mostrar FPS en la imagen
        """ 
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, 
                    (255, 0, 255), 3) 
        """

        # Mostrar la imagen
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
