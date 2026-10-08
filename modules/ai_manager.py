# ==========================================================
# Buddy AI - AI Manager
# Gemini -> APInex -> OpenCode Zen
# ==========================================================

from modules.ai import ask_ai
from modules.apinex_ai import ask_apinex_ai
from modules.zen_ai import ask_zen_ai


# ==========================================================
# MAIN AI RESPONSE
# ==========================================================

def get_ai_response(user_message, memory_context=""):

    # ------------------------------------------------------
    # 1. GEMINI
    # ------------------------------------------------------

    try:

        print("\n[AI Manager] Trying Gemini...")

        response = ask_ai(
            user_message,
            memory_context
        )

        if response:
            response = str(response).strip()

        if response and not is_ai_error(response):

            print("[AI Manager] Gemini SUCCESS")

            return response

        print("[AI Manager] Gemini unavailable.")

    except Exception as e:

        print(
            "[AI Manager] Gemini Exception:",
            repr(e)
        )


    # ------------------------------------------------------
    # 2. APINEX
    # ------------------------------------------------------

    try:

        print("\n[AI Manager] Trying APInex...")

        response = ask_apinex_ai(
            user_message,
            memory_context
        )

        if response:
            response = str(response).strip()

        if response and not is_ai_error(response):

            print("[AI Manager] APInex SUCCESS")

            return response

        print("[AI Manager] APInex unavailable.")

    except Exception as e:

        print(
            "[AI Manager] APInex Exception:",
            repr(e)
        )


    # ------------------------------------------------------
    # 3. OPENCODE ZEN
    # ------------------------------------------------------

    try:

        print("\n[AI Manager] Trying OpenCode Zen...")

        response = ask_zen_ai(
            user_message,
            memory_context
        )

        if response:
            response = str(response).strip()

        if response and not is_ai_error(response):

            print("[AI Manager] OpenCode Zen SUCCESS")

            return response

        print("[AI Manager] OpenCode Zen unavailable.")

    except Exception as e:

        print(
            "[AI Manager] OpenCode Zen Exception:",
            repr(e)
        )


    # ------------------------------------------------------
    # ALL FAILED
    # ------------------------------------------------------

    print("\n[AI Manager] All AI services failed.")

    return None


# ==========================================================
# AI ERROR DETECTION
# ==========================================================

def is_ai_error(response):

    if not response:
        return True

    text = str(response).lower().strip()

    error_phrases = [

        "gemini error",
        "gemini api error",
        "gemini api key",
        "gemini unavailable",

        "authentication error",
        "authentication mein masla",

        "free-tier limit",
        "rate limit",
        "too many requests",

        "service unavailable",
        "service is unavailable",

        "response lene mein filhaal masla",
        "ai service unavailable",
        "ai brain mein filhaal masla",

        "temporarily unavailable",
        "internal server error",
        "server error"

    ]

    for phrase in error_phrases:

        if phrase in text:
            return True

    return False


# ==========================================================
# STARTUP INFORMATION
# ==========================================================

print("Buddy AI AI Manager Loaded")
print("AI Chain: Gemini -> APInex -> OpenCode Zen")