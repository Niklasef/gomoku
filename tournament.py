import subprocess
import os
import sys

import numpy

#All 2021 openings 
openings = [
    "8,-3, 6,-4, 5,-4, 4,-3, 2,-8, -1,-5",
    "6,6, 4,6, 6,4, 4,4, 6,2, 4,2",
    "-1,3, -1,5, 3,5, 4,4, 6,1",
    "-4,1, -4,2, -4,-1, -4,0, -2,0, -3,0, 0,0, -1,0, 0,2, 0,1, -1,-2, 0,-1, -2,-3, -3,-2, 3,-2, 3,-3, 3,0, 3,-1, 3,1, 3,2",
    "-8,9, -7,7, -5,5",
    "-2,8, -3,6, -1,6",
    "-8,7, -6,7, -5,5, -7,3, -7,2",
    "-5,8, -5,6, -6,6",
    "2,9, -2,8, -3,5",
    "7,7, 3,4, 2,5, -2,4, 1,1",
    "-10,8, -9,9, -10,7, -8,9, -10,6, -7,9, -5,9, -10,4, -4,9, -10,3, -3,9, -10,2, -10,0, -1,9, -10,-1, 0,9, -10,-2, 1,9, 3,9, -10,-4, 4,9, -10,-5, 5,9, -10,-6, -10,-8, 7,9, -8,7",
    "-5,9, -3,9, -1,7, 1,9, 3,9, -1,5"
]

non_historic_index_models = []
if len(sys.argv) > 1:
    non_historic_index_models = sys.argv[1]

models = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
opponents = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
results = {}
for model in models:
    results[model] = 0
print(models)

for model in models:
    opponents = list(filter(lambda x: x != model, opponents))
    for opponent in opponents:
        for opening in openings:
            print(f'"{model}" vs "{opponent}"')
            winner = int(subprocess.check_output(["py.exe", "play.py", model, opponent, opening, "silent", non_historic_index_models]).decode("utf-8").strip())
            if winner == 1:
                results[model] += 1
                print(f'"{model}" won')
            elif winner == -1:
                results[opponent] += 1
                print(f'"{opponent}" won')
            print(f'"{opponent}" vs "{model}"')
            winner = int(subprocess.check_output(["py.exe", "play.py", opponent, model, opening, "silent", non_historic_index_models]).decode("utf-8").strip())
            if winner == 1:
                results[opponent] += 1
                print(f'"{opponent}" won')
            elif winner == -1:
                results[model] += 1
                print(f'"{model}" won')

print(sorted(results.items(), key=lambda x:x[1], reverse=True))
