import os
import numpy as np
import cv2
import mediapipe as mp
import keyboard
from itertools import product
from funciones import *

# Define the actions (signs) that will be recorded and stored in the dataset
actions = np.array(['a','b'])

# Define the number of sequences and frames to be recorded for each action
sequences = 30
frames = 10

# Set the path where the dataset will be stored
PATH = os.path.join('data')

# Create directories for each action, sequence, and frame in the dataset
for action, sequence in product(actions, range(sequences)):
    try:
        os.makedirs(os.path.join(PATH, action, str(sequence)))
    except:
        pass

# Inicializar la cámara
cap = initialize_camera()

# Create a MediaPipe Holistic object for hand tracking and landmark extraction
with mp.solutions.holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
    # Loop through each action, sequence, and frame to record data
    for action, sequence, frame in product(actions, range(sequences), range(frames)):
        # If it is the first frame of a sequence, wait for the spacebar key press to start recording
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

                cv2.putText(image, 'Guardandos datos para "{}". Secuencia numero {}.'.format(action, sequence),
                            (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                cv2.putText(image, 'Pausa.', (20,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Presiona Espacio cuando estes listo', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                cv2.imshow('Camera', image)
                cv2.waitKey(1)
                
                # Check if the 'Camera' window was closed and break the loop
                if cv2.getWindowProperty('Camera',cv2.WND_PROP_VISIBLE) < 1:
                    break
        else:
            # For subsequent frames, directly read the image from the camera
            _, image = cap.read()
            # Process the image and extract hand landmarks using the MediaPipe Holistic pipeline
            results = image_process(image, holistic)
            image.flags.writeable = True  # Habilitar escritura para OpenCV
            # Draw the hand landmarks on the image
            draw_landmarks(image, results)

            # Display text on the image indicating the action and sequence number being recorded
            cv2.putText(image, 'Guardando datos para "{}". Secuencia numero {}.'.format(action, sequence),
                (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow('Camera', image)
            cv2.waitKey(1)

        # Check if the 'Camera' window was closed and break the loop
        if cv2.getWindowProperty('Camera',cv2.WND_PROP_VISIBLE) < 1:
             break

        # Extract the landmarks from both hands and save them in arrays
        keypoints = keypoint_extraction(results)
        frame_path = os.path.join(PATH, action, str(sequence), str(frame))
        np.save(frame_path, keypoints)

    # Release the camera and close any remaining windows
    cap.release()
    cv2.destroyAllWindows()