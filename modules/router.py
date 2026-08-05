from commands import handle_command
from modules.brain import handle_brain
from modules.ai import ask_ai


def route(user_input, speak):
    """
    Buddy AI Router
    Decides which module should handle the user's message.
    """

    # 1. Commands
    if handle_command(user_input, speak):
        return None

    # 2. Brain
    reply = handle_brain(user_input)
    if reply:
        return reply

    # 3. Gemini AI (Fallback)
    reply = ask_ai(user_input)
    return reply