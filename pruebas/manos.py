import cv2
import mediapipe as mp
from funciones import *

# Inicializar la cámara
cap = initialize_camera()

# Inicialización de Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, 
                      min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

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

        # Mostrar la imagen
        cv2.imshow("Image", img)
        
        # Detectar cierre de ventana o tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()