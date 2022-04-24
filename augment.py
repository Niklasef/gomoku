import os
import sys
import numpy as np

input = np.fromstring(sys.argv[1].replace('[','').replace(']',''), dtype=int, sep='_')
board = input.reshape(20,20)
input_label = np.fromstring(sys.argv[2].replace('[','').replace(']',''), dtype=int, sep='_')
label = input_label.reshape(20,20)
silent = True

def to_string(m):
  return np.array2string(m.ravel().astype(int), max_line_width=10000, separator='_').replace(' ','')

board_rot_1 = to_string(np.rot90(board, k=1, axes=(0, 1)))
board_rot_2 = to_string(np.rot90(board, k=2, axes=(0, 1)))
board_rot_3 = to_string(np.rot90(board, k=1, axes=(1, 0)))
board_flip = to_string(np.fliplr(board))
board_flip_rot_1 = to_string(np.fliplr(np.rot90(board, k=1, axes=(0, 1))))
board_flip_rot_2 = to_string(np.fliplr(np.rot90(board, k=2, axes=(0, 1))))
board_flip_rot_3 = to_string(np.fliplr(np.rot90(board, k=1, axes=(1, 0))))

if not silent:
  os.system("python print_board.py " + board_rot_1)
  os.system("python print_board.py " + board_rot_2)
  os.system("python print_board.py " + board_rot_3)
  os.system("python print_board.py " + board_flip)
  os.system("python print_board.py " + board_flip_rot_1)
  os.system("python print_board.py " + board_flip_rot_2)
  os.system("python print_board.py " + board_flip_rot_3)


label_rot_1 = to_string(np.rot90(label, k=1, axes=(0, 1)))
label_rot_2 = to_string(np.rot90(label, k=2, axes=(0, 1)))
label_rot_3 = to_string(np.rot90(label, k=1, axes=(1, 0)))
label_flip = to_string(np.fliplr(label))
label_flip_rot_1 = to_string(np.fliplr(np.rot90(label, k=1, axes=(0, 1))))
label_flip_rot_2 = to_string(np.fliplr(np.rot90(label, k=2, axes=(0, 1))))
label_flip_rot_3 = to_string(np.fliplr(np.rot90(label, k=1, axes=(1, 0))))

if not silent:
  os.system("python print_board.py " + label_rot_1)
  os.system("python print_board.py " + label_rot_2)
  os.system("python print_board.py " + label_rot_3)
  os.system("python print_board.py " + label_flip)
  os.system("python print_board.py " + label_flip_rot_1)
  os.system("python print_board.py " + label_flip_rot_2)
  os.system("python print_board.py " + label_flip_rot_3)

original = to_string(board) + "|" + to_string(label)
aug_1 = board_rot_1 + "|" + label_rot_1
aug_2 = board_rot_2 + "|" + label_rot_2
aug_3 = board_rot_3 + "|" + label_rot_3
aug_4 = board_flip + "|" + label_flip
aug_5 = board_flip_rot_1 + "|" + label_flip_rot_1
aug_6 = board_flip_rot_2 + "|" + label_flip_rot_2
aug_7 = board_flip_rot_3 + "|" + label_flip_rot_3

print([original, aug_1, aug_2, aug_3, aug_4, aug_5, aug_6, aug_7])
