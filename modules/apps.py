import os



def handle_apps(command, speak):

    if "notepad" in command or "pad" in command:
        reply = "Notepad khol raha hoon."
        speak(reply)
        os.system("notepad")
        return reply

    if "calculator" in command or "calc" in command:
        reply = "Calculator khol raha hoon."
        speak(reply)
        os.system("calc")
        return reply

    if "paint" in command:
        reply = "Paint khol raha hoon."
        speak(reply)
        os.system("mspaint")
        return reply

    return None