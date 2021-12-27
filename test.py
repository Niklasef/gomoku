import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load data
test_data = np.genfromtxt('preped/test_data.npy', delimiter=',')
test_labels = np.genfromtxt('preped/test_labels.npy', delimiter=',')

# Load model
model = keras.models.load_model('model')

#### Test Model ####
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
