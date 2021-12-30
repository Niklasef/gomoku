import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

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

# Setup Neural Net
model = keras.Sequential()
model.add(layers.Dense(units=400, activation='relu'))
model.add(layers.Dense(units=1000, activation='relu'))
model.add(layers.Dense(units=400, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# print(model.summary())

# Prepare the training dataset
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
train_dataset = train_dataset.batch(32)

# Prepare the validation dataset
val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
val_dataset = val_dataset.batch(32)

#### Train Model ####
history = model.fit(train_dataset, epochs=10, validation_data=val_dataset)
model.save('model')

print('Done')
