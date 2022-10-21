import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import subprocess

# Load data
# input_format = 'TXT'
input_format = 'BIN'
if input_format == 'TXT':
    train_data = np.genfromtxt('preped/train_data.npy', delimiter=',')
else:
    train_data = np.load('preped/train_data.npy')
if input_format == 'TXT':
    train_labels = np.genfromtxt('preped/train_labels.npy', delimiter=',')
else:
    train_labels = np.load('preped/train_labels.npy')
if input_format == 'TXT':
    val_data = np.genfromtxt('preped/val_data.npy', delimiter=',')
else:
    val_data = np.load('preped/val_data.npy')
if input_format == 'TXT':
    val_labels = np.genfromtxt('preped/val_labels.npy', delimiter=',')
else:
    val_labels = np.load('preped/val_labels.npy')

train_data = tf.expand_dims(train_data, axis=-1)
val_data = tf.expand_dims(val_data, axis=-1)

print(train_data.shape)
print(train_labels.shape)

# Setup Neural Net
model = keras.models.Sequential([
    keras.layers.Conv2D(filters=64, kernel_size=(7,7), strides=(1,1), activation='relu', padding="same", input_shape=(20,20,1)),
    keras.layers.Conv2D(filters=128, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same"),
    keras.layers.Conv2D(filters=128, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
    keras.layers.Conv2D(filters=512, kernel_size=(2,2), strides=(1,1), activation='relu', padding="same"),    
    keras.layers.Flatten(),
    keras.layers.Dense(400, activation='softmax')    
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# Prepare the training dataset
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
train_dataset = train_dataset.batch(16)

# Prepare the validation dataset
val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
val_dataset = val_dataset.batch(16)

#### Train Model ####
history = model.fit(train_dataset, epochs=2, validation_data=val_dataset)

label = subprocess.check_output(["git", "describe"]).decode("utf-8").strip()
print(label)
model.save('models/' + label)

print('Done')
