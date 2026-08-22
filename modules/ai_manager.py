# ==========================================
# Buddy AI - AI Manager
# ==========================================

from modules.ai import ask_ai


def get_ai_response(user_message, memory_context=""):

    try:

        response = ask_ai(
            user_message,
            memory_context
        )

        # Gemini ne proper response diya
        if response and not response.startswith("Gemini Error:"):

            return response

        # Gemini unavailable
        return None

    except Exception as e:

        print("AI Manager Error:", e)

        return None