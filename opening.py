import os
import sys
import numpy

moves = sys.argv[1]
silent = True if len(sys.argv) == 3 and sys.argv[2] == "silent" else False
opening = numpy.zeros(shape=(20, 20))

player = 1
for move in moves.split(' '):
    opening[int(move.split(',')[1])+10][int(move.split(',')[0])+10] = player
    player *= -1
    if player > 0:
        player += 1
opening_ser = numpy.array2string(opening.ravel().astype(int), max_line_width=10000, separator='_').replace(' ','')
if silent:
    print(opening_ser)
else:
    os.system("python print_board.py " + opening_ser)
