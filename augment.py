import os
import sys
import numpy as np

# input = np.fromstring(sys.argv[1].replace('[','').replace(']',''), dtype=int, sep='_')
# board = input.reshape(20,20)
# input_label = np.fromstring(sys.argv[2].replace('[','').replace(']',''), dtype=int, sep='_')
# label = input_label.reshape(20,20)
# silent = True

def to_string(m):
  return np.array2string(m.ravel().astype(int), max_line_width=10000, separator='_').replace(' ','')

def aug(board, label):

  board_rot_1 = np.rot90(board, k=1, axes=(0, 1))
  board_rot_2 = np.rot90(board, k=2, axes=(0, 1))
  board_rot_3 = np.rot90(board, k=1, axes=(1, 0))
  board_flip = np.fliplr(board)
  board_flip_rot_1 = np.fliplr(np.rot90(board, k=1, axes=(0, 1)))
  board_flip_rot_2 = np.fliplr(np.rot90(board, k=2, axes=(0, 1)))
  board_flip_rot_3 = np.fliplr(np.rot90(board, k=1, axes=(1, 0)))


  label_rot_1 = np.rot90(label, k=1, axes=(0, 1))
  label_rot_2 = np.rot90(label, k=2, axes=(0, 1))
  label_rot_3 = np.rot90(label, k=1, axes=(1, 0))
  label_flip = np.fliplr(label)
  label_flip_rot_1 = np.fliplr(np.rot90(label, k=1, axes=(0, 1)))
  label_flip_rot_2 = np.fliplr(np.rot90(label, k=2, axes=(0, 1)))
  label_flip_rot_3 = np.fliplr(np.rot90(label, k=1, axes=(1, 0)))

  return [
    [board, label],
    [board_rot_1, label_rot_1],
    [board_rot_2, label_rot_2],
    [board_rot_3, label_rot_3],
    # [board_flip, label_flip],
    # [board_flip_rot_1, label_flip_rot_1],
    # [board_flip_rot_2, label_flip_rot_2],
    # [board_flip_rot_3, label_flip_rot_3]
  ]
