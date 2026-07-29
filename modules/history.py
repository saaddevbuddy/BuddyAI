import json
import os

HISTORY_FILE = "data/history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


def add_history(user, buddy):
    history = load_history()

    history.append({
        "user": user,
        "buddy": buddy
    })

    # Sirf last 20 conversations rakhna
    history = history[-20:]

    save_history(history)
def last_command():
    history = load_history()

    if history:
        return history[-1]["user"]

    return None

def total_conversations():
    history = load_history()
    return len(history)
def clear_history():
    save_history([])