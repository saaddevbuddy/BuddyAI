# ==========================================
# Buddy AI - Mood Triggers 1.1
# ==========================================

from modules.buddy_mood import (
    change_buddy_mood,
    get_buddy_mood,
    set_buddy_mood
)


# ==========================================
# Trigger Words
# ==========================================

PRAISE_WORDS = [
    "good job",
    "great job",
    "well done",
    "amazing",
    "excellent",
    "zabardast",
    "shabash",
    "wah buddy",
    "nice buddy",
    "acha buddy",
    "bohot acha",
    "bohat acha",
    "great",
    "best buddy"
]


INSULT_WORDS = [
    "stupid",
    "useless",
    "bekar",
    "bakwass",
    "bewaqoof",
    "pagal",
    "nikamma",
    "ghatiya"
]


EXCITED_WORDS = [
    "wow",
    "waah",
    "yess",
    "yes",
    "yay",
    "kamal",
    "awesome"
]


SAD_WORDS = [
    "sorry buddy",
    "tumse naraz hoon",
    "main naraz hoon",
    "you failed",
    "tum fail ho gaye",
    "galat jawab"
]


# ==========================================
# Buddy Mood Escalation
# ==========================================

def apply_mood_escalation():

    current = get_buddy_mood()

    mood = current.get(
        "mood",
        "normal"
    )

    intensity = current.get(
        "intensity",
        0
    )

    # --------------------------------------
    # Annoyed → Angry
    # --------------------------------------

    if mood == "annoyed" and intensity >= 75:

        set_buddy_mood(
            "angry",
            intensity,
            "Buddy became more annoyed"
        )

        return "angry"


    # --------------------------------------
    # Happy → Excited
    # --------------------------------------

    if mood == "happy" and intensity >= 75:

        set_buddy_mood(
            "excited",
            intensity,
            "Buddy became more excited"
        )

        return "excited"


    # --------------------------------------
    # Sad → Tired
    # --------------------------------------

    if mood == "sad" and intensity >= 80:

        set_buddy_mood(
            "tired",
            intensity,
            "Buddy became emotionally tired"
        )

        return "tired"


    return mood


# ==========================================
# Detect Mood Trigger
# ==========================================

def detect_buddy_mood_trigger(user_input):

    text = user_input.lower().strip()


    # --------------------------------------
    # Praise
    # --------------------------------------

    for word in PRAISE_WORDS:

        if word in text:

            change_buddy_mood(
                "happy",
                20,
                f"User praised Buddy: {word}"
            )

            apply_mood_escalation()

            return "happy"


    # --------------------------------------
    # Insult
    # --------------------------------------

    for word in INSULT_WORDS:

        if word in text:

            change_buddy_mood(
                "annoyed",
                25,
                f"User insulted Buddy: {word}"
            )

            apply_mood_escalation()

            return "annoyed"


    # --------------------------------------
    # Excited
    # --------------------------------------

    for word in EXCITED_WORDS:

        if word in text:

            change_buddy_mood(
                "excited",
                20,
                f"User sounded excited: {word}"
            )

            apply_mood_escalation()

            return "excited"


    # --------------------------------------
    # Sad / Disappointed
    # --------------------------------------

    for word in SAD_WORDS:

        if word in text:

            change_buddy_mood(
                "sad",
                20,
                f"Conversation caused disappointment: {word}"
            )

            apply_mood_escalation()

            return "sad"


    # --------------------------------------
    # No Trigger
    # --------------------------------------

    return None