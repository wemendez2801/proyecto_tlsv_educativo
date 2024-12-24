import os
import cv2

# Creación de carpeta
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 3
dataset_size = 100

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

# Colección de imágenes
for j in range(number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Recolectando datos para la clase: {}'.format(j))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame.")
            break

        frame = cv2.flip(frame, 1)  # Invertir la imagen horizontalmente
        cv2.putText(frame, 'Presiona Q para empezar :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame.")
            break

        frame = cv2.flip(frame, 1)  # Invertir la imagen horizontalmente
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

        counter += 1

cap.release()
cv2.destroyAllWindows()