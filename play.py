from asyncio.windows_events import NULL
import os
import subprocess
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from gomoku import predict, won

board = np.zeros(shape=(20, 20))

# Load models
model_black_name = sys.argv[1]
model_black = keras.models.load_model('models/' + model_black_name)
model_white_name = ''
model_white = NULL
silent = False
human_player_exists = False
non_historic_index_models = []
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
    if len(sys.argv) >= 5:
      silent = sys.argv[4] == 'silent'
      if len(sys.argv) >= 6:
        non_historic_index_models = sys.argv[5].split(',')

opening_moves = (board != 0).sum()
starting_color = "BLACK"
if opening_moves % 2 != 0:
  starting_color = "WHITE"
  temp = model_black
  model_black = model_white
  model_white = temp

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
    (row, col) = predict(model_black if player == "BLACK" else model_white, board, player)
  if won(row, col, 1 if player == "BLACK" else -1, board):
    board[row][col] = 1 if player == "BLACK" else -1
    if not silent:
      os.system("python print_board.py " + np.array2string(board.ravel().astype(int), max_line_width=10000, separator='_').replace(' ',''))
    break
  board[row][col] = 1 if player == "BLACK" else -1
  if not silent:
    os.system("python print_board.py " + np.array2string(board.ravel().astype(int), max_line_width=10000, separator='_').replace(' ',''))
  player = "WHITE" if player == "BLACK" else "BLACK"
