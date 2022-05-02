from asyncio.windows_events import NULL
from copy import copy
import os
verbose=0
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.0/bin")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf
from tensorflow import keras

tf.get_logger().setLevel('ERROR')
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
    w_board = np.where(w_board > 0, 2, w_board)
    w_board = np.where(w_board < 0, 1, w_board)
    w_board = np.where(w_board == 2, -1, w_board)    
    m[0] = tf.expand_dims(w_board, axis=-1)

  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
  tf.get_logger().setLevel('ERROR')
  # predictions_percent = model.predict(m.astype(float), verbose=0)
  predictions_percent = model(m.astype(float), training=False)
  sorted_predictions = np.argsort(predictions_percent, axis=1)[0][::-1]
  predictions = []
  n = 2
  i = 0
  for p in sorted_predictions:
    p_ravel = np.unravel_index(p, (20, 20))
    if board[p_ravel[0]][p_ravel[1]] == 0:
      predictions.append(p_ravel)
      i += 1
      if i == n:
        break
  return predictions

def predict(model, board, color):
  predictions = p(model, board, color)
  return predictions[0]
  first = minimax(model, np.copy(board), color, predictions[0], color, 3, 1, 40)
  second = minimax(model, np.copy(board), color, predictions[1], color, 3, 1, 40)

  print("p first = " + str(first))
  print("p second = " + str(second))

  if first >= second:
    return predictions[0]
  return predictions[1]

def minimax(model, board, color, prediction, initial_color, depth, i, play_outs):
  if won(prediction[0], prediction[1], 1 if color == "BLACK" else -1, board):
    return 1 if color == initial_color else -1

  board[prediction[0]][prediction[1]] = 1 if color == "BLACK" else -1
  predictions = p(model, board, "WHITE" if color == "BLACK" else "BLACK")
  if i <= depth:
    first = minimax(model, np.copy(board), "WHITE" if color == "BLACK" else "BLACK", predictions[0], color, depth, i + 1, play_outs)
    second = minimax(model, np.copy(board), "WHITE" if color == "BLACK" else "BLACK", predictions[1], color, depth, i + 1, play_outs)
    is_maximizing = color == initial_color
    print("is_maximizing = " + str(is_maximizing))
    print("first = " + str(first))
    print("second = " + str(second))

    return max([first, second]) if is_maximizing else min([first, second])
    
  return playout(model, board, "WHITE" if color == "BLACK" else "BLACK", predictions, initial_color, 1, play_outs)[1]

def playout(model, board, color, predictions, initial_color, i, play_outs):
  if not predictions:
    return (i+1, 0)
  if won(predictions[0][0], predictions[0][1], 1 if color == "BLACK" else -1, board):
    return (i+1,(1 if color == initial_color else -1))

  board[predictions[0][0]][predictions[0][1]] = 1 if color == "BLACK" else -1
  color = "WHITE" if color == "BLACK" else "BLACK"
  new_predictions = p(model, board, color)
  result_one = (0,0)
  result_two = (0,0)
  result_one = playout(model, board, color, new_predictions, initial_color, i, play_outs)
  if result_one[0] > 1 and result_one[0] <= play_outs and new_predictions and len(new_predictions) > 1 and result_one:
      result_two = playout(model, board, color, [new_predictions[1]], initial_color, result_one[0], play_outs)
  return ((result_one[0]+result_two[0]),(result_one[1]+result_two[1]))
