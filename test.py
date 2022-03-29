import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Load data
# input_format = 'TXT'
input_format = 'BIN'
if input_format == 'TXT':
  test_data = np.genfromtxt('preped/test_data.npy', delimiter=',')
else:
  test_data = np.load('preped/test_data.npy')
if input_format == 'TXT':
  test_labels = np.genfromtxt('preped/test_labels.npy', delimiter=',')
else:
  test_labels = np.load('preped/test_labels.npy')

# Load model
model = keras.models.load_model('models/' + sys.argv[1])

#### Test Model ####
predictions_percent = model.predict(tf.expand_dims(test_data, axis=-1))
predictions = np.argmax(predictions_percent, axis=1)
answers =  np.argmax(test_labels, axis=1)
correct = 0
illegal_move = 0
for i in range(predictions.shape[0]):
  if test_data[i].ravel().astype(int)[answers[i]] != 0:
    illegal_move += 1
  if predictions[i] == answers[i]:
    correct += 1

print('Test Accuracy:')
print(correct/predictions.shape[0])
print('Illegal Moves:')
print(illegal_move/predictions.shape[0])

print('Done')
