import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "data", "memory.json")


def load_memory():
    try:
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as file:
                json.dump({}, file, indent=4)

        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except Exception:
        return {}


def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w") as file:
            json.dump(memory, file, indent=4)

    except Exception as e:
        print("Memory Error:", e)