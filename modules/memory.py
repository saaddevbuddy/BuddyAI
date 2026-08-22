import json
import os


# ==========================================
# Buddy AI - Persistent Memory 2.0
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

MEMORY_FILE = os.path.join(
    DATA_DIR,
    "memory.json"
)


# ==========================================
# Load Memory
# ==========================================

def load_memory():

    try:

        os.makedirs(
            DATA_DIR,
            exist_ok=True
        )

        if not os.path.exists(MEMORY_FILE):

            with open(
                MEMORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {},
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return {}

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except (
        json.JSONDecodeError,
        OSError
    ) as e:

        print(
            "Memory Load Error:",
            e
        )

        return {}


# ==========================================
# Save Memory
# ==========================================

def save_memory(memory):

    try:

        os.makedirs(
            DATA_DIR,
            exist_ok=True
        )

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as e:

        print(
            "Memory Save Error:",
            e
        )

        return False


# ==========================================
# Get Memory
# ==========================================

def get_memory(key, default=None):

    memory = load_memory()

    return memory.get(
        key,
        default
    )


# ==========================================
# Set Memory
# ==========================================

def set_memory(key, value):

    memory = load_memory()

    memory[key] = value

    return save_memory(memory)


# ==========================================
# Update Memory
# ==========================================

def update_memory(data):

    if not isinstance(data, dict):
        return False

    memory = load_memory()

    memory.update(data)

    return save_memory(memory)


# ==========================================
# Delete Memory
# ==========================================

def delete_memory(key):

    memory = load_memory()

    if key not in memory:
        return False

    del memory[key]

    return save_memory(memory)


# ==========================================
# Clear Memory
# ==========================================

def clear_memory():

    return save_memory({})


# ==========================================
# Get All Memory
# ==========================================

def get_all_memory():

    return load_memory()

# ==========================================
# Save Extracted Memory
# ==========================================

def save_extracted_memory(data):

    if not isinstance(data, dict):
        return False

    if not data:
        return False

    memory = load_memory()

    memory.update(data)

    return save_memory(memory)

def search_memory(query):
    memory = get_all_memory()

    query = query.lower()

    results = {}

    keywords = {
        "phone": ["phone", "mobile", "samsung", "iphone"],
        "game": ["game", "gaming", "khel"],
        "food": ["food", "khana", "biryani"],
        "car": ["car", "gaari", "hilux"],
        "ai": ["ai", "artificial intelligence"],
        "youtuber": ["youtube", "youtuber"],
        "hobby": ["hobby", "shoq"],
        "dream": ["dream", "khwab"],
        "goal": ["goal", "maqsad"]
    }

    for memory_key, words in keywords.items():

        for word in words:

            if word in query:

                if memory_key == "phone":
                    if "favorite_phone" in memory:
                        results["favorite_phone"] = memory["favorite_phone"]

                elif memory_key == "game":
                    if "favorite_game" in memory:
                        results["favorite_game"] = memory["favorite_game"]

                elif memory_key == "food":
                    if "favorite_food" in memory:
                        results["favorite_food"] = memory["favorite_food"]

                elif memory_key == "car":
                    if "favorite_car" in memory:
                        results["favorite_car"] = memory["favorite_car"]

                elif memory_key == "ai":
                    if "favorite_ai" in memory:
                        results["favorite_ai"] = memory["favorite_ai"]

                elif memory_key == "youtuber":
                    if "favorite_youtuber" in memory:
                        results["favorite_youtuber"] = memory["favorite_youtuber"]

                elif memory_key == "hobby":
                    if "hobby" in memory:
                        results["hobby"] = memory["hobby"]

                elif memory_key == "dream":
                    if "dream" in memory:
                        results["dream"] = memory["dream"]

                elif memory_key == "goal":
                    if "goal" in memory:
                        results["goal"] = memory["goal"]

                break

    return results