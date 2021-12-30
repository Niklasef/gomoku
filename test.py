import numpy as np
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