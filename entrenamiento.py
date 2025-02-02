import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from itertools import product
from sklearn import metrics

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Ruta de los datos
PATH = os.path.join('data')

# Se crea un arreglo de etiquetas de señas
actions = np.array(os.listdir(PATH))

sequences = 30
frames = 10

# Se crea un mapa de etiquetas para que cada etiqueta sea un número
label_map = {label:num for num, label in enumerate(actions)}

# Inicializa de landmarks y etiquetas
landmarks, labels = [], []

# Itera sobre acciones y secuencias para cargar landmarks y etiquetas correspondientes
for action, sequence in product(actions, range(sequences)):
    temp = []
    for frame in range(frames):
        npy = np.load(os.path.join(PATH, action, str(sequence), str(frame) + '.npy'))
        temp.append(npy)
    landmarks.append(temp)
    labels.append(label_map[action])

# Convierte landmarks y etiquetas a numpy
X, Y = np.array(landmarks), to_categorical(labels).astype(int)

# Separacion en datasets de entrenamiento y prueba
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=34, stratify=Y)

# Arquitectura del modelo
model = Sequential()
model.add(LSTM(32, return_sequences=True, activation='relu', input_shape=(10,126)))
model.add(LSTM(64, return_sequences=True, activation='relu'))
model.add(LSTM(32, return_sequences=False, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

# Compila el modelo con optimizador Adam y perdida categorica cross-entropy
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
# Entrena el modelo
model.fit(X_train, Y_train, epochs=100)

# Se guarda el modelo
model.save('my_model.keras')

# Hacer predicciones con el set de prueba
predictions = np.argmax(model.predict(X_test), axis=1)
# Get the true labels from the test set
test_labels = np.argmax(Y_test, axis=1)

# Calcula la precision de las predicciones
accuracy = metrics.accuracy_score(test_labels, predictions)