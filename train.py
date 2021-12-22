import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_data = np.genfromtxt('preped/train_data.npy', delimiter=',')
train_labels = np.genfromtxt('preped/train_labels.npy', delimiter=',')
val_data = np.genfromtxt('preped/val_data.npy', delimiter=',')
val_labels = np.genfromtxt('preped/val_labels.npy', delimiter=',')

#print(train_labels)


#### Setup Neural Net ####
model = keras.Sequential()
model.add(layers.Dense(units=400, activation='sigmoid'))
model.add(layers.Dense(units=400, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# print(model.summary())
# Prepare the training dataset
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
train_dataset = train_dataset.batch(16)

# Prepare the validation dataset
val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
val_dataset = val_dataset.batch(16)

#### Train Model ####
history = model.fit(train_dataset, epochs=100, validation_data=val_dataset)

predictions = model.predict(val_dataset)
print('predictions:')
print(predictions)

with open('preped/predictions.npy', "wb") as f:
  np.savetxt(f, predictions, delimiter=",")


print('Done')