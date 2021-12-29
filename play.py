import numpy as np
from tensorflow import keras

# Load data
test_data = np.genfromtxt('preped/test_data.npy', delimiter=',')
test_labels = np.genfromtxt('preped/test_labels.npy', delimiter=',')

# Load model
model = keras.models.load_model('model')
board = np.zeros(shape=(20, 20))

def won(row, col, color):
  return connected(row, col, color, 'horizontal') >= 5 or connected(row, col, color, 'vertical') >= 5 or connected(row, col, color, 'diagonal-1') >= 5 or connected(row, col, color, 'diagonal-2') >= 5 

def connected(row, col, color, direction):
  if board[row][col] != color:
    return 0
  if direction == 'horizontal':
    return 1 + connected(row, col - 1, color, 'left') + connected(row, col + 1, color, 'right')
  if direction == 'left':
    return 1 + connected(row, col - 1, color, direction)
  if direction == 'right':
    return 1 + connected(row, col + 1, color, direction)

  if direction == "diagonal-1":
    return 1 + connected(row + 1, col + 1, color, 'right-down') + connected(row - 1, col - 1, color, 'left-up')
  if direction == 'right-down':
    return 1 + connected(row + 1, col + 1, color, direction)
  if direction == 'left-up':
    return 1 + connected(row - 1, col - 1, color, direction)
  
  if direction == "diagonal-2":
    return 1 + connected(row + 1, col - 1, color, 'left-down') + connected(row - 1, col + 1, color, 'right-up')    
  if direction == 'left-down':
    return 1 + connected(row + 1, col - 1, color, direction)
  if direction == 'right-up':
    return 1 + connected(row - 1, col + 1, color, direction)  

  if direction == 'vertical':
    return 1 + connected(row + 1, col, color, 'down') + connected(row - 1, col, color, 'up')
  if direction == 'down':
    return 1 + connected(row + 1, col, color, direction)
  if direction == 'up':
    return 1 + connected(row - 1, col, color, direction)

def predict():
  m = np.zeros(shape=(1, 400))
  m[0] = board.ravel()
  predictions_percent = model.predict(m)
  prediction = np.argmax(predictions_percent, axis=1)[0]
  print(prediction)
  pm  = np.zeros(shape=(400))
  pm[prediction] = 1
  pm = np.reshape(pm, (20, 20))
  return pm

row = 0
col = 0
while not won(row, col, 2):
  p = predict()
  board = board + p
  print(board)
  move = input('Make move:')
  row = int(move.split(',')[0]) - 1
  col = int(move.split(',')[1]) - 1
  board[row][col] = 2
