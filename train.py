import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_data = np.genfromtxt('preped/train_data.npy', delimiter=',')
train_labels = np.genfromtxt('preped/train_labels.npy', delimiter=',')
#val_data = np.load('preped/val_data.npy')
#val_labels = np.load('preped/val_labels.npy')

#print(train_labels)


#### Setup Neural Net ####
model = keras.Sequential()
model.add(layers.Dense(units=400, activation='relu'))
model.add(layers.Dense(units=400, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# print(model.summary())
# Prepare the training dataset
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
train_dataset = train_dataset.batch(32)

# Prepare the validation dataset
#val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
#val_dataset = val_dataset.batch(4)

#### Train Model ####
history = model.fit(train_dataset, epochs=60)

#predictions = model.predict(train_dataset)
#print('predictions:')
#print(predictions)


#print('Done')