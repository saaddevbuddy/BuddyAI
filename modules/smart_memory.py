import re

from modules.memory import load_memory, save_memory


MEMORY_PATTERNS = {

    "name": [
        r"mera naam (.+?) hai",
    ],

    "age": [
        r"main (\d+) saal ka hoon",
        r"meri age (\d+)",
        r"mera age (\d+)",
    ],

    "city": [
        r"main (.+?) se hoon",
        r"mera city (.+?) hai",
    ],

    "country": [
        r"main (.+?) country se hoon",
        r"mera country (.+?) hai",
    ],

    "favorite_game": [
        r"mera favourite game (.+?) hai",
        r"mujhe (.+?) bohot pasand hai",
    ],

    "favorite_food": [
        r"mera favourite food (.+?) hai",
        r"mujhe (.+?) khana pasand hai",
    ],

    "dream": [
        r"mera dream (.+?) hai",
    ],

    "goal": [
        r"mera goal (.+?) hai",
    ],

}

def extract_information(command):

    command = command.lower().strip()

    for key, patterns in MEMORY_PATTERNS.items():

        for pattern in patterns:

            match = re.search(pattern, command)

            if match:

                value = match.group(1).strip().title()

                return key, value

    return None, None

def save_information(key, value):

    memory = load_memory()

    if "profile" not in memory:
        memory["profile"] = {}

    memory["profile"][key] = value

    save_memory(memory)

def handle_smart_memory(command, speak):
    reply = answer_question(command)

    if reply:
        speak(reply)
        return reply
    key, value = extract_information(command)
    

    if key:

        save_information(key, value)

        labels = {
            "name": "naam",
            "age": "age",
            "city": "city",
            "country": "country",
            "favorite_game": "favourite game",
            "favorite_food": "favourite food",
            "dream": "dream",
            "goal": "goal",
        }

        field = labels.get(key, key.replace("_", " "))

        reply = (
            f"Theek hai Sir, maine yaad rakh liya "
            f"ke aapka {field} {value} hai."
        )

        speak(reply)
        return reply

    return None
def answer_question(command):

    memory = load_memory()

    profile = memory.get("profile", {})

    command = command.lower()

    QUESTIONS = {
        "mera naam kya hai": "name",
        "meri age kya hai": "age",
        "mera age kya hai": "age",
        "main kitne saal ka hoon": "age",
        "mera city kya hai": "city",
        "main kahan se hoon": "city",
        "mera country kya hai": "country",
        "mera dream kya hai": "dream",
        "mera goal kya hai": "goal",
        "mera favourite game kya hai": "favorite_game",
        "mera favourite food kya hai": "favorite_food",
    }

    for question, key in QUESTIONS.items():

        if question in command:

            value = profile.get(key)

            if value:
                return f"Sir, aapka {key.replace('_',' ')} {value} hai."

            return "Sir, mujhe iska jawab yaad nahi."

    return None
