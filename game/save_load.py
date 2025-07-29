import os
SAVE_FILE = "save.txt"

def save_level(level):
    with open(SAVE_FILE, "w") as f:
        f.write(str(level))

def load_level():
    if not os.path.exists(SAVE_FILE):
        return 1
    with open(SAVE_FILE, "r") as f:
        return int(f.read().strip())
