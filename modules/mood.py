# ==========================================
# Buddy AI - Advanced Mood Engine
# ==========================================

import re


# ==========================================
# Mood Definitions
# ==========================================

MOOD_INFO = {

    "excited": {
        "emoji": "🤩",
        "name": "Excited",
        "style": "Buddy energetic, cheerful aur friendly tone mein baat kare.",
    },

    "sad": {
        "emoji": "😔",
        "name": "Sad",
        "style": "Buddy soft, caring aur supportive tone mein baat kare.",
    },

    "frustrated": {
        "emoji": "😤",
        "name": "Frustrated",
        "style": "Buddy calm, patient aur solution-focused tone mein baat kare.",
    },

    "worried": {
        "emoji": "😟",
        "name": "Worried",
        "style": "Buddy reassuring, gentle aur supportive tone mein baat kare.",
    },

    "confused": {
        "emoji": "🤔",
        "name": "Confused",
        "style": "Buddy simple, clear aur step-by-step tareeqe se samjhaye.",
    },

    "tired": {
        "emoji": "😴",
        "name": "Tired",
        "style": "Buddy relaxed, short aur easy responses de.",
    },

    "neutral": {
        "emoji": "🙂",
        "name": "Normal",
        "style": "Buddy normal dostana tone mein baat kare.",
    }
}


# ==========================================
# Mood Keywords
# ==========================================

MOOD_WORDS = {

    # --------------------------------------
    # Excited / Happy
    # --------------------------------------

    "excited": [
        "wah",
        "wow",
        "zabardast",
        "awesome",
        "mazay",
        "maza aa gaya",
        "khush",
        "khushi",
        "khushi ho rahi",
        "khush hoon",
        "khush hun",
        "happy",
        "great",
        "nice",
        "hahaha",
        "haha",
        "lets go",
        "let's go",
        "chalo",
        "yes",
        "yay",
        "kamal",
        "shabash",
        "maza aa gaya"
    ],

    # --------------------------------------
    # Sad / Low
    # --------------------------------------

    "sad": [
        "udaas",
        "udas",
        "sad",
        "dukhi",
        "bura lag",
        "dil kharab",
        "akela",
        "akeli",
        "lonely",
        "mann nahi",
        "man nahi",
        "mood off",
        "dil udaas",
        "dil udaas hai"
    ],

    # --------------------------------------
    # Angry / Frustrated
    # --------------------------------------

    "frustrated": [
        "gussa",
        "ghussa",
        "tang aa gaya",
        "tang agya",
        "tang aa gya",
        "bekar",
        "bakwas",
        "frustrate",
        "frustrated",
        "nahi chal raha",
        "kaam nahi kar raha",
        "kaam nhi kar raha",
        "error aa raha",
        "error agaya",
        "error a gaya",
        "error baar baar",
        "baar baar error",
        "problem aa rahi",
        "problem agayi",
        "problem a gayi",
        "masla aa raha",
        "masla agaya",
        "masla a gaya",
        "baar baar masla"
    ],

    # --------------------------------------
    # Worried
    # --------------------------------------

    "worried": [
        "fikar",
        "fikr",
        "dar",
        "darr",
        "worry",
        "worried",
        "ghabra",
        "ghabrahat",
        "pareshan",
        "pareshan hoon",
        "pareshani",
        "tension",
        "tension ho rahi",
        "tension hai",
        "darr lag raha",
        "fikr ho rahi",
        "fikar ho rahi"
    ],

    # --------------------------------------
    # Confused
    # --------------------------------------

    "confused": [
        "samajh nahi",
        "samajh nhi",
        "samajh nahi aa raha",
        "samajh nhi aa raha",
        "confuse",
        "confused",
        "pata nahi",
        "kya karun",
        "kya karoon",
        "kya karna hai",
        "samajh nahi araha",
        "samajh nhi araha"
    ],

    # --------------------------------------
    # Tired
    # --------------------------------------

    "tired": [
        "neend",
        "so jana",
        "sona hai",
        "tired",
        "thakawat",
        "bohat thak",
        "bahut thak",
        "energy nahi",
        "energy nhi",
        "thak gaya",
        "thak gya",
        "thak gayi"
    ]
}


# ==========================================
# Text Normalization
# ==========================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower().strip()

    # Extra spaces remove
    text = re.sub(r"\s+", " ", text)

    return text


# ==========================================
# Internal Mood Scoring
# ==========================================

def _calculate_mood_scores(text):

    scores = {
        mood: 0
        for mood in MOOD_WORDS
    }

    matched_words = {
        mood: []
        for mood in MOOD_WORDS
    }

    for mood, words in MOOD_WORDS.items():

        for word in words:

            if word in text:

                scores[mood] += 1
                matched_words[mood].append(word)

    return scores, matched_words


# ==========================================
# Detect Mood
# ==========================================

def detect_mood(text):

    text = normalize_text(text)

    if not text:
        return "neutral"

    scores, matched_words = _calculate_mood_scores(text)

    if max(scores.values()) == 0:
        return "neutral"

    strongest_mood = max(
        scores,
        key=scores.get
    )

    return strongest_mood


# ==========================================
# Detailed Mood Detection
# ==========================================

def analyze_mood(text):

    text = normalize_text(text)

    if not text:

        return {
            "mood": "neutral",
            "name": "Normal",
            "emoji": "🙂",
            "confidence": 0,
            "matched_words": [],
            "style": get_mood_style("neutral")
        }

    scores, matched_words = _calculate_mood_scores(text)

    # --------------------------------------
    # No mood detected
    # --------------------------------------

    if max(scores.values()) == 0:

        return {
            "mood": "neutral",
            "name": MOOD_INFO["neutral"]["name"],
            "emoji": MOOD_INFO["neutral"]["emoji"],
            "confidence": 0,
            "matched_words": [],
            "style": MOOD_INFO["neutral"]["style"]
        }

    # --------------------------------------
    # Strongest mood
    # --------------------------------------

    mood = max(
        scores,
        key=scores.get
    )

    score = scores[mood]

    # --------------------------------------
    # Confidence
    # --------------------------------------

    if score >= 3:
        confidence = 90

    elif score == 2:
        confidence = 75

    else:
        confidence = 60

    return {
        "mood": mood,
        "name": MOOD_INFO[mood]["name"],
        "emoji": MOOD_INFO[mood]["emoji"],
        "confidence": confidence,
        "matched_words": matched_words[mood],
        "style": MOOD_INFO[mood]["style"]
    }


# ==========================================
# Get Mood Style
# ==========================================

def get_mood_style(mood):

    return MOOD_INFO.get(
        mood,
        MOOD_INFO["neutral"]
    )["style"]


# ==========================================
# Get Mood Emoji
# ==========================================

def get_mood_emoji(mood):

    return MOOD_INFO.get(
        mood,
        MOOD_INFO["neutral"]
    )["emoji"]


# ==========================================
# Get Mood Name
# ==========================================

def get_mood_name(mood):

    return MOOD_INFO.get(
        mood,
        MOOD_INFO["neutral"]
    )["name"]

# ==========================================
# AI Mood Analysis Prompt
# ==========================================

def build_mood_prompt(text, context=""):

    return f"""
You are Buddy AI's mood understanding system.

Analyze the user's message and determine their likely emotional state.

Possible moods:
- excited
- sad
- frustrated
- worried
- confused
- tired
- neutral

User message:
{text}

Previous conversation context:
{context}

Rules:
1. Understand the meaning, not just keywords.
2. Roman Urdu, Urdu and English may be mixed.
3. Do not assume a negative mood without evidence.
4. If the message is ambiguous, choose neutral.
5. Return ONLY one mood name from the allowed moods.

Mood:
""".strip()


# ==========================================
# Validate AI Mood
# ==========================================

def validate_mood(mood):

    if not mood:
        return "neutral"

    mood = str(mood).lower().strip()

    if mood in MOOD_INFO:
        return mood

    return "neutral"