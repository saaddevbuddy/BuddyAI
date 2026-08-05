INTENTS = {

    # ------------------- Apps -------------------

    "calculator": [
        "calculator",
        "calc",
        "calculate",
        "math",
        "hisab",
        "hisaab",
        "hissab",
        "hisab karo",
        "hisaab karo",
        "jama karo"
    ],

    "notepad": [
        "notepad",
        "notes",
        "pad"
    ],

    "paint": [
        "paint",
        "drawing",
        "draw"
    ],

    # ------------------- Browser -------------------

    "youtube": [
        "youtube",
        "yt"
    ],

    "google": [
        "google",
        "search"
    ],

    "chatgpt": [
        "chatgpt",
        "gpt"
    ],

    # ------------------- System -------------------

    "time": [
        "time",
        "waqt",
        "clock"
    ],

    "screenshot": [
        "screenshot",
        "screen shot",
        "capture screen"
    ],

    "internet": [
        "internet",
        "internet status",
        "net check"
    ],

    "system_status": [
        "system status",
        "pc status",
        "computer status"
    ],

    "mute": [
        "mute",
        "volume off"
    ],

    "unmute": [
        "unmute",
        "volume on"
    ],

    # ------------------- Memory -------------------

    "name_save": [
        "mera naam",
        "my name is"
    ],

    "name_ask": [
        "mera naam kya hai",
        "naam kya hai",
        "what is my name"
    ],

    "game_save": [
        "mera favourite game",
        "my favourite game"
    ],


    "game_ask": [
    "mera favourite game kya hai",
    "mera favourite game kya ha",
    "favourite game kya hai",
    "favourite game kya ha"
    ],
    "colour_save": [
        "mera favourite colour",
        "my favourite colour"
    ],

    "colour_ask": [
        "favourite colour kya hai"
    ],

    "food_save": [
        "mera favourite food",
        "my favourite food"
    ],

    "food_ask": [
        "favourite food kya hai"
    ],

    "hobby_save": [
        "meri hobby",
        "my hobby"
    ],

    "hobby_ask": [
        "meri hobby kya hai",
        "hobby kya hai"
    ],

    "profile": [
        "meri profile",
        "profile dikhao",
        "my profile"
    ],

    # ------------------- Conversation -------------------

    "greeting": [
        "hello",
        "hi",
        "assalam",
        "slam"
    ],

    "how_are_you": [
        "how are you",
        "kaise ho"
    ],

    "thanks": [
        "thank",
        "thanks",
        "shukriya"
    ],

    "sad": [
        "sad",
        "udaas",
        "dukhi",
        "depressed",
        "tension",
        "pareshan"
    ],

    "happy": [
        "happy",
        "khush",
        "excited",
        "bohot khushi"
    ],

    # ------------------- Notes -------------------

    "note": [
        "note",
        "likh lo",
        "save note"
    ],

    # ------------------- Reminder -------------------

    "reminder": [
        "reminder",
        "yaad dilana",
        "remind me"
    ]
}


def detect_intent(command):

    command = command.lower()

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in command:
                return intent

    return None

def has_intent(command, intent):

    detected = detect_intent(command)

    return detected == intent