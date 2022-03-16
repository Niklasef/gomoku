import sys
from colorama import init, Fore, Back
import numpy as np

init(wrap=False)

board = np.zeros(shape=(20, 20))


x = np.fromstring(sys.argv[1].replace('[','').replace(']',''), dtype=int, sep='_')
y = x.reshape(20,20)
r = 1
print(Back.GREEN, Fore.BLACK,"      1       2       3       4       5       6       7       8       9      10      11      12      13      14      15      16      17      18      19      20   ")
for row in y:
  print(Back.GREEN, Fore.BLACK,"  ----------------------------------------------------------------------------------------------------------------------------------------------------------------")
  print(str(r).rjust(2, ' '), end='') 
  r += 1
  for cell in row:
    cell_text = str(cell).rjust(3, ' ')
    print(Back.GREEN, Fore.BLACK, '|', end='')
    if cell == 0:
      print(Back.GREEN, Fore.BLACK, '   ', end='')
    if cell > 0:
      print(Back.BLACK, Fore.WHITE, cell_text, end='')
    if cell < 0:
      print(Back.WHITE, Fore.BLACK, cell_text, end='')
  print(Back.GREEN, '|')
print(Back.GREEN, Fore.BLACK,"  ----------------------------------------------------------------------------------------------------------------------------------------------------------------")
