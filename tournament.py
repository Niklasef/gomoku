import subprocess
import os


models = [f.path for f in os.scandir("models") if f.is_dir()]
print(models)

winner = subprocess.check_output(["py.exe", "play.py", "cnn-64_5-64_2-64_2-400", "cnn-64_5-64_2-64_2-400-2-g4cb5cfe", "silent"]).decode("utf-8").strip()
print(winner)