import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_data = np.load('preped/train_data.npy')
train_labels = np.load('preped/train_labels.npy')
val_data = np.load('preped/val_data.npy')
val_labels = np.load('preped/val_labels.npy')

print(train_data)
print(train_labels)

#### Setup Neural Net ####
model = keras.Sequential()
model.add(layers.Dense(units=400, activation='relu'))
model.add(layers.Dense(units=400, activation='relu'))
model.add(layers.Dense(units=400, activation='relu'))
model.add(layers.Dense(units=400, activation='relu'))
model.add(layers.Dense(units=400, activation='relu'))
model.add(layers.Dense(units=1, activation='sigmoid'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

input_shape = train_data.shape
model.build(input_shape)
model.summary()

# Prepare the training dataset
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
train_dataset = train_dataset.batch(64)

# Prepare the validation dataset
val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
val_dataset = val_dataset.batch(64)

#### Train Model ####
history = model.fit(train_dataset, epochs=10, validation_data=val_dataset)

print('Hello world')