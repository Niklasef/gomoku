import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_data = np.genfromtxt('preped/train_data.npy', delimiter=',')
train_labels = np.genfromtxt('preped/train_labels.npy', delimiter=',')
val_data = np.genfromtxt('preped/val_data.npy', delimiter=',')
val_labels = np.genfromtxt('preped/val_labels.npy', delimiter=',')
test_data = np.genfromtxt('preped/test_data.npy', delimiter=',')
test_labels = np.genfromtxt('preped/test_labels.npy', delimiter=',')

#print(train_labels)


#### Setup Neural Net ####
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
history = model.fit(train_dataset, epochs=100, validation_data=val_dataset)

predictions_percent = model.predict(test_data)
predictions = np.argmax(predictions_percent, axis=1)
answers =  np.argmax(test_labels, axis=1)
correct = 0
illegal_move = 0
for i in range(predictions.shape[0]):
  if test_data[i][answers[i]] != 0:
    illegal_move += 1
  if predictions[i] == answers[i]:
    correct += 1

print('predictions:')
print(predictions)
print('answers:')
print(answers)
print('correct:')
print(correct)
print(correct/predictions.shape[0])
print('illegal_move:')
print(illegal_move)
print(illegal_move/predictions.shape[0])

print('Done')