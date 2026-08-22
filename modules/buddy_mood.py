# ==========================================
# Buddy AI - Buddy Mood Engine 1.0
# ==========================================

import json
import os
from datetime import datetime


# ==========================================
# Mood File
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MOOD_FILE = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "buddy_mood.json"
)


# ==========================================
# Default Buddy Mood
# ==========================================

DEFAULT_MOOD = {
    "mood": "normal",
    "intensity": 0,
    "reason": "Buddy started normally",
    "updated_at": ""
}


# ==========================================
# Load Mood
# ==========================================

def load_buddy_mood():

    try:

        if not os.path.exists(MOOD_FILE):

            save_buddy_mood(
                DEFAULT_MOOD
            )

            return DEFAULT_MOOD.copy()

        with open(
            MOOD_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):

            return data

        return DEFAULT_MOOD.copy()

    except Exception as e:

        print(
            "Buddy Mood Load Error:",
            e
        )

        return DEFAULT_MOOD.copy()


# ==========================================
# Save Mood
# ==========================================

def save_buddy_mood(mood_data):

    try:

        folder = os.path.dirname(
            MOOD_FILE
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        with open(
            MOOD_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                mood_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        print(
            "Buddy Mood Save Error:",
            e
        )

        return False


# ==========================================
# Set Mood
# ==========================================

def set_buddy_mood(
    mood,
    intensity=0,
    reason=""
):

    mood_data = {
        "mood": mood,
        "intensity": intensity,
        "reason": reason,
        "updated_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    return save_buddy_mood(
        mood_data
    )


# ==========================================
# Get Current Mood
# ==========================================

def get_buddy_mood():

    return load_buddy_mood()


# ==========================================
# Change Mood
# ==========================================

def change_buddy_mood(
    mood,
    amount=10,
    reason=""
):

    current = load_buddy_mood()

    current_mood = current.get(
        "mood",
        "normal"
    )

    current_intensity = current.get(
        "intensity",
        0
    )

    # Agar mood same hai to intensity increase
    if current_mood == mood:

        new_intensity = (
            current_intensity + amount
        )

    else:

        new_intensity = amount

    # Intensity ko 0-100 ke andar rakho
    new_intensity = max(
        0,
        min(
            100,
            new_intensity
        )
    )

    return set_buddy_mood(
        mood,
        new_intensity,
        reason
    )


# ==========================================
# Reset Mood
# ==========================================

def reset_buddy_mood():

    return set_buddy_mood(
        "normal",
        0,
        "Buddy mood reset"
    )


# ==========================================
# Mood Style
# ==========================================

def get_buddy_mood_style():

    mood_data = get_buddy_mood()

    mood = mood_data.get(
        "mood",
        "normal"
    )

    intensity = mood_data.get(
        "intensity",
        0
    )

    styles = {

        "normal":
            "Normal, friendly aur balanced andaaz mein jawab do.",

        "happy":
            "Khush aur warm andaaz mein jawab do.",

        "excited":
            "Energetic aur excited andaaz mein jawab do.",

        "annoyed":
            "Halka annoyed andaaz rakho, lekin respectful raho.",

        "angry":
            "Firm aur visibly naraz andaaz rakho, lekin abusive mat ho.",

        "sad":
            "Soft aur thoda udaas andaaz mein jawab do.",

        "confused":
            "Confused lekin helpful andaaz mein jawab do.",

        "tired":
            "Short aur calm andaaz mein jawab do.",

        "thinking":
            "Thoughtful aur focused andaaz mein jawab do.",

        "playful":
            "Light-hearted aur playful andaaz mein jawab do.",

        "proud":
            "Confident aur khush andaaz mein jawab do."
    }

    style = styles.get(
        mood,
        styles["normal"]
    )

    return {
        "mood": mood,
        "intensity": intensity,
        "style": style
    }