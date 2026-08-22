# ==========================================
# Buddy AI - Wake / Call System
# ==========================================

def check_wake_word(text):

    if not text:
        return False

    text = text.lower().strip()

    wake_words = [
        "buddy",
        "hey buddy",
        "oye buddy",
        "buddy suno",
        "buddy sun"
    ]

    for word in wake_words:
        if word in text:
            return True

    return False


def get_wake_response():

    return "Ji Sir?"