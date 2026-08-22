# ==========================================
# Buddy AI - Context Engine 2.0
# ==========================================

import re
from datetime import datetime


# ==========================================
# Context State
# ==========================================

_current_topic = None
_current_subtopic = None
_last_user_message = ""
_last_buddy_reply = ""

_topic_history = []


# ==========================================
# Topic Keywords
# ==========================================

TOPIC_KEYWORDS = {

    "buddy_ai": [
        "buddy",
        "buddy ai",
        "buddy ka",
        "buddy ko",
        "buddy mein",
        "buddy ban",
        "buddy banana"
    ],

    "coding": [
        "code",
        "coding",
        "python",
        "file",
        "function",
        "error",
        "bug",
        "programming",
        "script",
        "module"
    ],

    "gui": [
        "gui",
        "interface",
        "window",
        "button",
        "chat box",
        "screen",
        "tkinter",
        "design"
    ],

    "voice": [
        "voice",
        "awaaz",
        "bol",
        "bolna",
        "sun",
        "listening",
        "microphone",
        "mic",
        "tts",
        "speech"
    ],

    "camera": [
        "camera",
        "webcam",
        "face",
        "chehra",
        "dekh",
        "detect",
        "expression"
    ],

    "memory": [
        "memory",
        "yaad",
        "yaad rakh",
        "bhool",
        "remember",
        "history",
        "purani baat"
    ],

    "mood": [
        "mood",
        "khush",
        "udaas",
        "sad",
        "gussa",
        "excited",
        "tired",
        "expression"
    ],

    "gaming": [
        "game",
        "gaming",
        "ets",
        "ready or not",
        "mission",
        "pistol"
    ],

    "islamic": [
        "quran",
        "hadith",
        "islam",
        "allah",
        "namaz",
        "naat",
        "dua",
        "surah"
    ]
}


# ==========================================
# Normalize Text
# ==========================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower().strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ==========================================
# Detect Topic
# ==========================================

def detect_topic(text):

    text = normalize_text(text)

    if not text:
        return None

    scores = {
        topic: 0
        for topic in TOPIC_KEYWORDS
    }

    for topic, keywords in TOPIC_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                scores[topic] += 1

    strongest_topic = max(
        scores,
        key=scores.get
    )

    if scores[strongest_topic] == 0:

        return None

    return strongest_topic


# ==========================================
# Topic Confidence
# ==========================================

def get_topic_confidence(text):

    text = normalize_text(text)

    if not text:
        return 0

    topic = detect_topic(text)

    if not topic:
        return 0

    matches = 0

    for keyword in TOPIC_KEYWORDS[topic]:

        if keyword in text:

            matches += 1

    if matches >= 3:
        return 90

    if matches == 2:
        return 75

    return 60


# ==========================================
# Update Context
# ==========================================

def update_context(
    user_message,
    buddy_reply=""
):

    global _current_topic
    global _current_subtopic
    global _last_user_message
    global _last_buddy_reply

    user_message = str(
        user_message or ""
    ).strip()

    buddy_reply = str(
        buddy_reply or ""
    ).strip()

    detected_topic = detect_topic(
        user_message
    )

    # --------------------------------------
    # Topic found
    # --------------------------------------

    if detected_topic:

        if detected_topic != _current_topic:

            if _current_topic:

                _topic_history.append(
                    _current_topic
                )

            _current_topic = detected_topic

    _last_user_message = user_message
    _last_buddy_reply = buddy_reply

    return get_context()


# ==========================================
# Get Current Context
# ==========================================

def get_context():

    return {

        "current_topic":
            _current_topic,

        "current_subtopic":
            _current_subtopic,

        "last_user_message":
            _last_user_message,

        "last_buddy_reply":
            _last_buddy_reply,

        "topic_history":
            _topic_history[-5:]
    }


# ==========================================
# Get Current Topic
# ==========================================

def get_current_topic():

    return _current_topic


# ==========================================
# Get Last User Message
# ==========================================

def get_last_user_message():

    return _last_user_message


# ==========================================
# Get Last Buddy Reply
# ==========================================

def get_last_buddy_reply():

    return _last_buddy_reply


# ==========================================
# Is Same Topic?
# ==========================================

def is_same_topic(text):

    topic = detect_topic(text)

    if not topic:
        return False

    return topic == _current_topic


# ==========================================
# Context Reference Detection
# ==========================================

def is_context_reference(text):

    text = normalize_text(text)

    if not text:
        return False

    reference_words = [

        "ye",
        "yeh",
        "woh",
        "wo",
        "is",
        "us",
        "iske",
        "uske",
        "isi",
        "usi",
        "ye wala",
        "woh wala",
        "yeh wala",
        "wo wala",
        "us wala",
        "is wala",
        "isko",
        "usko",
        "iske andar",
        "uske andar",
        "phir",
        "aagay",
        "continue",
        "continue karo",
        "aage karo",
        "wahi",
        "wahi wala"
    ]

    return any(
        word in text
        for word in reference_words
    )


# ==========================================
# Build Context Prompt
# ==========================================

def build_context_prompt():

    context = get_context()

    topic = context.get(
        "current_topic"
    )

    last_user = context.get(
        "last_user_message"
    )

    last_buddy = context.get(
        "last_buddy_reply"
    )

    history = context.get(
        "topic_history",
        []
    )

    return f"""
CURRENT BUDDY CONTEXT

Current Topic:
{topic or "Unknown"}

Previous Topics:
{", ".join(history) if history else "None"}

Last User Message:
{last_user or "None"}

Last Buddy Reply:
{last_buddy or "None"}

Use this context only when it is relevant.
If the user's current message refers to
"ye", "woh", "wahi", "is ko", "us ko",
"ye wala" or similar wording, use the
current conversation context to understand
what they mean.
""".strip()


# ==========================================
# Reset Context
# ==========================================

def reset_context():

    global _current_topic
    global _current_subtopic
    global _last_user_message
    global _last_buddy_reply
    global _topic_history

    _current_topic = None
    _current_subtopic = None
    _last_user_message = ""
    _last_buddy_reply = ""

    _topic_history = []


# ==========================================
# Context Status
# ==========================================

def context_status():

    return {

        "active": bool(
            _current_topic
            or _last_user_message
        ),

        "topic":
            _current_topic,

        "history_count":
            len(_topic_history),

        "last_activity":
            datetime.now().isoformat(
                timespec="seconds"
            )
    }