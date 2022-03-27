import subprocess
import os


models = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
opponents = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
results = {}
for model in models:
    results[model] = 0
print(models)

for model in models:
    opponents = list(filter(lambda x: x != model, opponents))
    for opponent in opponents:
        print(f'"{model}" vs "{opponent}"')
        winner = int(subprocess.check_output(["py.exe", "play.py", model, opponent, "silent"]).decode("utf-8").strip())
        if winner == 1:
            results[model] += 1
            print(f'"{model}" won')
        elif winner == -1:
            results[opponent] += 1
            print(f'"{opponent}" won')
        print(f'"{opponent}" vs "{model}"')
        winner = int(subprocess.check_output(["py.exe", "play.py", opponent, model, "silent"]).decode("utf-8").strip())
        if winner == 1:
            results[opponent] += 1
            print(f'"{opponent}" won')
        elif winner == -1:
            results[model] += 1
            print(f'"{model}" won')

print(sorted(results.items(), key=lambda x:x[1], reverse=True))
