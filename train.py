import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_data = np.genfromtxt('preped/train_data.npy', delimiter=',')
train_labels = np.genfromtxt('preped/train_labels.npy', delimiter=',')
#val_data = np.load('preped/val_data.npy')
#val_labels = np.load('preped/val_labels.npy')

print(train_data.shape[0])
reshaped_train_data =  np.empty(shape=(train_data.shape[0], 20, 20))
i = 0
for row in train_data:
  reshaped_train_data[i] = train_data[i].reshape((20, 20))
  i += 1

print(reshaped_train_data[89])
#print(train_labels)

#### Setup Neural Net ####
#model = keras.Sequential()
#model.add(layers.Dense(units=400, activation='sigmoid'))
#model.add(layers.Dense(units=100, activation='sigmoid'))
#model.add(layers.Dense(units=10, activation='sigmoid'))
#model.add(layers.Dense(units=1, activation='sigmoid'))
#model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Prepare the training dataset
#train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
#train_dataset = train_dataset.batch(4)

# Prepare the validation dataset
#val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
#val_dataset = val_dataset.batch(4)

#### Train Model ####
#history = model.fit(train_dataset, epochs=2, validation_data=val_dataset)

#predictions = model.predict(train_dataset)
#print('predictions:')
#print(predictions)


#print('Done')