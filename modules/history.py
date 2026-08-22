import json
import os
import re

# ==========================================
# Buddy AI - Conversation History Engine
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "history.json"
)

MAX_HISTORY = 50


# ==========================================
# Load History
# ==========================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (
        json.JSONDecodeError,
        OSError
    ) as e:

        print("History Load Error:", e)

        return []


# ==========================================
# Save History
# ==========================================

def save_history(history):

    try:

        os.makedirs(
            os.path.dirname(HISTORY_FILE),
            exist_ok=True
        )

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as e:

        print("History Save Error:", e)

        return False


# ==========================================
# Add Conversation
# ==========================================

def add_history(user, buddy):

    history = load_history()

    history.append({
        "user": str(user).strip(),
        "buddy": str(buddy).strip()
    })

    # Sirf latest conversations rakho
    history = history[-MAX_HISTORY:]

    save_history(history)


# ==========================================
# Recent History
# ==========================================

def get_recent_history(limit=8):

    history = load_history()

    if not history:
        return []

    return history[-limit:]


# ==========================================
# Format Recent History
# ==========================================

def format_recent_history(limit=8):

    history = get_recent_history(limit)

    if not history:
        return ""

    lines = []

    for item in history:

        user = item.get("user", "")
        buddy = item.get("buddy", "")

        if user:
            lines.append(
                f"Saad: {user}"
            )

        if buddy:
            lines.append(
                f"Buddy: {buddy}"
            )

    return "\n".join(lines)


# ==========================================
# Relevant History
# ==========================================

def get_relevant_history(
    query,
    limit=5
):

    history = load_history()

    if not history:
        return []

    query = str(
        query
    ).lower().strip()

    if not query:
        return []

    # Query ke useful words
    words = set(
        re.findall(
            r"\b[a-zA-Z0-9_]+\b",
            query
        )
    )

    # Bohat common words ignore
    stop_words = {
        "main",
        "mein",
        "mujhe",
        "mera",
        "meri",
        "mere",
        "hai",
        "hoon",
        "hun",
        "houn",
        "aap",
        "sir",
        "ye",
        "ya",
        "aur",
        "kya",
        "ka",
        "ki",
        "ke",
        "ko",
        "se",
        "par",
        "bhi",
        "to",
        "the",
        "is",
        "it",
        "what",
        "how"
    }

    words -= stop_words

    if not words:
        return []

    scored = []

    for index, item in enumerate(history):

        user_text = item.get(
            "user",
            ""
        ).lower()

        buddy_text = item.get(
            "buddy",
            ""
        ).lower()

        combined = (
            user_text +
            " " +
            buddy_text
        )

        score = 0

        for word in words:

            if word in combined:
                score += 1

        if score > 0:

            scored.append(
                (
                    score,
                    index,
                    item
                )
            )

    # Strongest matches first
    scored.sort(
        key=lambda x: (
            x[0],
            x[1]
        ),
        reverse=True
    )

    return [
        item
        for score, index, item
        in scored[:limit]
    ]


# ==========================================
# Format Relevant History
# ==========================================

def format_relevant_history(
    query,
    limit=5
):

    history = get_relevant_history(
        query,
        limit
    )

    if not history:
        return ""

    lines = []

    for item in history:

        user = item.get(
            "user",
            ""
        )

        buddy = item.get(
            "buddy",
            ""
        )

        lines.append(
            f"Saad: {user}"
        )

        lines.append(
            f"Buddy: {buddy}"
        )

    return "\n".join(lines)


# ==========================================
# Build Conversation Context
# ==========================================

def build_context(
    query,
    recent_limit=8,
    relevant_limit=5
):

    recent = format_recent_history(
        recent_limit
    )

    relevant = format_relevant_history(
        query,
        relevant_limit
    )

    context_parts = []

    if recent:

        context_parts.append(
            "RECENT CONVERSATION:\n"
            + recent
        )

    if relevant:

        context_parts.append(
            "RELEVANT PAST CONVERSATION:\n"
            + relevant
        )

    if not context_parts:

        return "No previous conversation available."

    return "\n\n".join(
        context_parts
    )


# ==========================================
# Last Command
# ==========================================

def last_command():

    history = load_history()

    if history:

        return history[-1].get(
            "user"
        )

    return None


# ==========================================
# Last Buddy Reply
# ==========================================

def last_reply():

    history = load_history()

    if history:

        return history[-1].get(
            "buddy"
        )

    return None


# ==========================================
# Total Conversations
# ==========================================

def total_conversations():

    return len(
        load_history()
    )


# ==========================================
# Clear History
# ==========================================

def clear_history():

    return save_history([])