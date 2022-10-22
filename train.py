import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import subprocess
import os

def load_data(file_index):
    print(f"Loading files with index '{file_index}'")
    train_data = np.load(f'preped/train_data_{str(file_index)}.npy')
    train_labels = np.load(f'preped/train_labels_{str(file_index)}.npy')
    val_data = np.load(f'preped/val_data_{str(file_index)}.npy')
    val_labels = np.load(f'preped/val_labels_{str(file_index)}.npy')
    return train_data, train_labels, val_data, val_labels

# Setup Neural Net
model = keras.models.Sequential([
    keras.layers.Conv2D(filters=64, kernel_size=(11,11), strides=(1,1), activation='relu', padding="same", input_shape=(20,20,1)),
    keras.layers.Conv2D(filters=128, kernel_size=(7,7), strides=(1,1), activation='relu', padding="same"),
    keras.layers.Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same"),
    keras.layers.Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
    keras.layers.Conv2D(filters=128, kernel_size=(2,2), strides=(1,1), activation='relu', padding="same"),    
    keras.layers.Flatten(),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(400, activation='softmax'),
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

file_index_count = 0
for rootdir, dirs, files in os.walk("preped"):
    for file in files:
        if int(file.split('.')[0].split('_')[2]) > file_index_count:
            file_index_count = int(file.split('.')[0].split('_')[2])

for file_index in range(file_index_count):
    train_data, train_labels, val_data, val_labels = load_data(file_index)

    # Prepare the training dataset
    train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
    train_dataset = train_dataset.batch(16)

    # Prepare the validation dataset
    val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
    val_dataset = val_dataset.batch(16)

    #### Train Model ####
    history = model.fit(train_dataset, epochs=3, validation_data=val_dataset)

label = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode("utf-8").strip()
print(label)
model.save('models/' + label)

print('Done')
