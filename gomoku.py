from asyncio.windows_events import NULL
from copy import copy
import os

import numpy as np
import tensorflow as tf
from tensorflow import keras

def won(row, col, color, board):
  # board_copy = np.copy(board)
  # board_copy[row][col] = 1 if color == "BLACK" else -1
  w = connected(row, col, color, 'horizontal', board, True) >= 5 or connected(row, col, color, 'vertical', board, True) >= 5 or connected(row, col, color, 'diagonal-1', board, True) >= 5 or connected(row, col, color, 'diagonal-2', board, True) >= 5
  if w:
    print(color)
  return w

def same_color(first, second):
  return True if (first < 0 and second < 0) or (first > 0 and second > 0) else False

def connected(row, col, color, direction, board, initial):
  if row >= 20 or col >= 20 or row < 0 or col < 0 or (not same_color(board[row][col], color) and not initial):
    return 0
  if direction == 'horizontal':
    return 1 + connected(row, col - 1, color, 'left', board, False) + connected(row, col + 1, color, 'right', board, False)
  if direction == 'left':
    return 1 + connected(row, col - 1, color, direction, board, False)
  if direction == 'right':
    return 1 + connected(row, col + 1, color, direction, board, False)

  if direction == "diagonal-1":
    return 1 + connected(row + 1, col + 1, color, 'right-down', board, False) + connected(row - 1, col - 1, color, 'left-up', board, False)
  if direction == 'right-down':
    return 1 + connected(row + 1, col + 1, color, direction, board, False)
  if direction == 'left-up':
    return 1 + connected(row - 1, col - 1, color, direction, board, False)
  
  if direction == "diagonal-2":
    return 1 + connected(row + 1, col - 1, color, 'left-down', board, False) + connected(row - 1, col + 1, color, 'right-up', board, False)
  if direction == 'left-down':
    return 1 + connected(row + 1, col - 1, color, direction, board, False)
  if direction == 'right-up':
    return 1 + connected(row - 1, col + 1, color, direction, board, False)

  if direction == 'vertical':
    return 1 + connected(row + 1, col, color, 'down', board, False) + connected(row - 1, col, color, 'up', board, False)
  if direction == 'down':
    return 1 + connected(row + 1, col, color, direction, board, False)
  if direction == 'up':
    return 1 + connected(row - 1, col, color, direction, board, False)

def p(model, board, color):
  board_copy = np.copy(board)
  m = np.zeros(shape=(1, 20, 20, 1))
  if color == 'BLACK':
    m[0] = tf.expand_dims(board_copy, axis=-1)
  elif color == 'WHITE':
    w_board = board_copy
    w_board = np.where(w_board > 0, 1000+w_board, w_board)
    w_board = np.where(w_board < 0, (w_board*-1), w_board)
    w_board = np.where(w_board > 1000, ((w_board-1000)*-1), w_board)    
    m[0] = tf.expand_dims(w_board, axis=-1)

  predictions_percent = model.predict(m.astype(float))
  sorted_predictions = np.argsort(predictions_percent, axis=1)[0][::-1]
  prediction = (0, 0)
  for p in sorted_predictions:
    p_ravel = np.unravel_index(p, (20, 20))
    if board[p_ravel[0]][p_ravel[1]] == 0:
      prediction = p_ravel
      break
  return prediction

def predict(model, board, color):
  prediction = p(model, board, color)
  minimax(model, np.copy(board), color, prediction, color, 2, 1)

  return prediction

def minimax(model, board, color, prediction, initial_color, play_outs, i):
  while not won(prediction[0], prediction[1], 1 if color == "BLACK" else -1, board):
      board[prediction[0]][prediction[1]] = 1 if color == "BLACK" else -1
      # os.system("python print_board.py " + np.array2string(board.ravel().astype(int), max_line_width=10000, separator='_').replace(' ',''))
      color = "WHITE" if color == "BLACK" else "BLACK"
      prediction = p(model, board, color)
