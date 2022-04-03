from asyncio.windows_events import NULL
import os
import subprocess
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras

board = np.zeros(shape=(20, 20))

# Load models
model_black_name = sys.argv[1]
model_black = keras.models.load_model('models/' + model_black_name)
model_white_name = ''
model_white = NULL
silent = False
human_player_exists = False
if len(sys.argv) >= 3:
  if sys.argv[2] == "human":
    human_player_exists = True
  else:
    model_white_name = sys.argv[2]
    model_white = keras.models.load_model('models/' + model_white_name)
  if len(sys.argv) >= 4:
    opening_ser = subprocess.check_output(["py.exe", "opening.py", sys.argv[3], "silent"]).decode("utf-8")
    opening_raveled = np.fromstring(opening_ser.replace('[','').replace(']',''), dtype=int, sep='_')
    board = opening_raveled.reshape(20,20)
    if len(sys.argv) == 5:
      silent = sys.argv[4] == 'silent'

opening_moves = (board != 0).sum()
starting_color = "BLACK"
if opening_moves % 2 != 0:
  starting_color = "WHITE"
  temp = model_black
  model_black = model_white
  model_white = temp

def won(row, col, color):
  w = connected(row, col, color, 'horizontal') >= 5 or connected(row, col, color, 'vertical') >= 5 or connected(row, col, color, 'diagonal-1') >= 5 or connected(row, col, color, 'diagonal-2') >= 5
  if w:
    print(color)
  return w

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

def predict(color):
  m = np.zeros(shape=(1, 20, 20, 1))
  m[0] = tf.expand_dims(board, axis=-1)
  if color == 'BLACK':
    predictions_percent = model_black.predict(m.astype(float))
  if color == 'WHITE':
    w_board = board
    w_board = np.where(w_board==1, 3, w_board)
    w_board = np.where(w_board==-1, 1, w_board)
    w_board = np.where(w_board==3, 1, w_board)    
    w_m = np.zeros(shape=(1, 20, 20, 1))
    w_m[0] = tf.expand_dims(w_board, axis=-1)
    predictions_percent = model_white.predict(w_m.astype(float))    
  sorted_predictions = np.argsort(predictions_percent, axis=1)[0][::-1]
  prediction = (0, 0)
  for p in sorted_predictions:
    p_ravel = np.unravel_index(p, (20, 20))
    if board[p_ravel[0]][p_ravel[1]] == 0:
      prediction = p_ravel
      break
  return prediction

row = 0
col = 0
player = starting_color

while True:
  if human_player_exists and player != starting_color:
    while True: 
      move = input('Make move:')
      row = int(move.split(',')[0]) - 1
      col = int(move.split(',')[1]) - 1
      if board[row][col] == 0:
        break    
  else:
    (row, col) = predict(player)
  board[row][col] = 1 if player == "BLACK" else -1
  if not silent:
    os.system("python print_board.py " + np.array2string(board.ravel().astype(int), max_line_width=10000, separator='_').replace(' ',''))
  if won(row, col, 1 if player == "BLACK" else -1):
    break
  player = "WHITE" if player == "BLACK" else "BLACK"
