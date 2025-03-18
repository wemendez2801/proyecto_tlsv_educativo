import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from itertools import product
from sklearn import metrics

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Ruta de los datos
PATH = os.path.join('data')

# Se crea un arreglo de etiquetas de señas
actions = np.array(os.listdir(PATH))

sequences = 30
frames = 20

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
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(20, 126)))
model.add(Dropout(0.2))  # Evita sobreajuste
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(BatchNormalization())  # Mejora estabilidad
model.add(Dense(actions.shape[0], activation='softmax'))

# Compila el modelo con optimizador Adam y perdida categorica cross-entropy
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# Callbacks para mejorar el entrenamiento
early_stopping = EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)
model_checkpoint = ModelCheckpoint('best_model.keras', monitor='val_loss', save_best_only=True)

# Entrena el modelo con validación
history = model.fit(
    X_train, Y_train,
    epochs=300,
    validation_split=0.1, # Usa 10% de los datos de entrenamiento para validación 
    callbacks=[early_stopping, model_checkpoint]
)

# Carga el mejor modelo guardado
model.load_weights('best_model.keras')

# Se guarda el modelo final
model.save('modelo.keras')

# Hacer predicciones con el set de prueba
predictions = np.argmax(model.predict(X_test), axis=1)
test_labels = np.argmax(Y_test, axis=1)

# Calcula la precision de las predicciones
accuracy = metrics.accuracy_score(test_labels, predictions)

print(f'Precisión del modelo: {accuracy * 100:.2f}%')