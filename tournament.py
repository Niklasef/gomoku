import subprocess
import os


models = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
opponents = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
results = {}
for model in models:
    results[model] = 0
print(models)
setups = [
    "6-7_5-7_8-3_7-8_13-6_9-4", 
    "4-16_5-15_8-13_7-14_12-11_11-12", 
    "3-10_5-10_11-3_11-5_18-11_16-11_10-18_10-16"]

for model in models:
    opponents = list(filter(lambda x: x != model, opponents))
    for opponent in opponents:
        for setup in setups:
            print(f'"{model}" vs "{opponent}"')
            winner = int(subprocess.check_output(["py.exe", "play.py", setup, model, opponent, "silent"]).decode("utf-8").strip())
            if winner == 1:
                results[model] += 1
                print(f'"{model}" won')
            elif winner == -1:
                results[opponent] += 1
                print(f'"{opponent}" won')
            print(f'"{opponent}" vs "{model}"')
            winner = int(subprocess.check_output(["py.exe", "play.py", setup, opponent, model, "silent"]).decode("utf-8").strip())
            if winner == 1:
                results[opponent] += 1
                print(f'"{opponent}" won')
            elif winner == -1:
                results[model] += 1
                print(f'"{model}" won')

print(sorted(results.items(), key=lambda x:x[1], reverse=True))
