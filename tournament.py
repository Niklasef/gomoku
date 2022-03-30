import subprocess
import os

# All Setup Moves 2021
# setups = [
#     "6-7_5-7_8-3_7-8_13-6_9-4", 
#     "4-16_5-15_8-13_7-14_12-11_11-12", 
#     "12-18_12-12_17-16_17-17_18-18",
#     "15-13_16-14_16-16_17-17_18-16",
#     "20-1_19-1_18-1_17-1_16-1_15-1_15-2_15-3_15-4_15-5_20-2_20-3_20-4_20-5_20-6_19-6_18-6_17-6_16-6_15-6",
#     "9-7_8-9_10-8_9-9_10-10_9-11_11-11_10-11_11-9_12-10",
#     "2-20_2-19_2-18_2-17_2-16_2-15_2-14_2-13_2-12_2-11_2-10_2-9_2-8_2-7_2-6_2-5_2-4_2-3_2-2_2-1_5-10_5-12_4-13",
#     "4-4_5-5_17-4_16-5_17-17_16-16_4-17_5-16",
#     "8-9_9-9_10-9_11-9_12-9_13-9_13-10_12-10_11-10_10-10_9-10_8-10_7-9_7-10_7-11_8-11_9-11_10-11_11-11_12-11_13-11",
#     "2-14_3-16_6-17_8-12_7-12",
#     "7-3_8-4_9-5_10-6_11-7_8-6_7-7_10-4_11-3_7-9_8-10_9-11_10-12_11-13_8-12_7-13_10-10_11-9_7-15_8-15_9-15_10-15_11-15_7-18_11-18_10-18_9-18_8-18",
#     "3-10_5-10_11-3_11-5_18-11_16-11_10-18_10-16"]

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
