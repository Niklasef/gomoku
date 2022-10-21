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
CPU_CORES = 10

models = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
opponents = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
results = {}
for model in models:
    results[model] = 0
print(models)

matches = []
for model in models:
    opponents = list(filter(lambda x: x != model, opponents))
    for opponent in opponents:
        for opening in openings:
            matches.append((model, opponent, opening))
            matches.append((opponent, model, opening))


grouped_matches = [matches[i:i + CPU_CORES] for i in range(0, len(matches), CPU_CORES)]

for match_group in grouped_matches:
    processes = []
    for match in match_group:
        print(f'"{match[0]}" vs "{match[1]}"')
        p = subprocess.Popen(["python.exe", "play.py", match[0], match[1], match[2], "silent"], stdout=subprocess.PIPE)
        processes.append(p)
    for p in processes:
        out, err = p.communicate()
        winner = int(out.decode("utf-8").strip())
        if winner == 1:
            results[match[0]] += 1
            print(sorted(results.items(), key=lambda x:x[1], reverse=True))
        elif winner == -1:
            results[match[1]] += 1
            print(sorted(results.items(), key=lambda x:x[1], reverse=True))
