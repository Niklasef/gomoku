import numpy as np
import tensorflow as tf
from tensorflow import keras

np.set_printoptions( linewidth=140)  # float arrays %.3g    

# Load model
model = keras.models.load_model('model')
board = np.zeros(shape=(20, 20))

def won(row, col, color):
  return connected(row, col, color, 'horizontal') >= 5 or connected(row, col, color, 'vertical') >= 5 or connected(row, col, color, 'diagonal-1') >= 5 or connected(row, col, color, 'diagonal-2') >= 5 

def connected(row, col, color, direction):
  if row >= 20 or col >= 20 or row < 0 or col < 0 or board[row][col] != color:
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
  m = np.zeros(shape=(1, 20, 20, 1))
  m[0] = tf.expand_dims(board, axis=-1)
  predictions_percent = model.predict(m.astype(float))
  sorted_predictions = np.argsort(predictions_percent, axis=1)[0][::-1]
  prediction = (0, 0)
  for p in sorted_predictions:
    p_ravel = np.unravel_index(p, (20, 20))
    if board[p_ravel[0]][p_ravel[1]] == 0:
      prediction = p_ravel
      break
    print('Illegal predicted move')
  # print(prediction.shape)
  return prediction

row = 0
col = 0
while not won(row, col, -1):
  (pr, pc) = predict()
  print((pr+1, pc+1))
  board[pr][pc] = 1
  if won(pr, pc, 1):
    break
  print(board)
  while True: 
    move = input('Make move:')
    row = int(move.split(',')[0]) - 1
    col = int(move.split(',')[1]) - 1
    if board[row][col] == 0:
      break
  board[row][col] = -1

print(board)
