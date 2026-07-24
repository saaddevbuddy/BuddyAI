import os
import datetime
import webbrowser


def handle_command(command, speak):
    command = command.lower()

    

    if "notepad" in command or "pad" in command:
        reply = "Notepad khol raha hoon."
        speak(reply)
        os.system("notepad")
        return reply
 
    if "calculator" in command or "calc" in command:
        speak("Calculator khol raha hoon.")
        os.system("calc")
        return True
    if "paint" in command:
        reply = "Paint khol raha hoon."
        speak(reply)
        os.system("mspaint")
        return reply
    if "chrome" in command or "krom" in command:
        reply = "Chrome khol raha hoon."
        speak(reply)
        os.system("start chrome")
        return reply
    if "youtube" in command:
        reply = "YouTube khol raha hoon."
        speak(reply)
        webbrowser.open("https://www.youtube.com")
        return reply
    if "chatgpt" in command or "chat GPT" in command:
        reply = "ChatGPT khol raha hoon."
        speak(reply)
        webbrowser.open("https://www.chatgpt.com")
        return reply
    if "google" in command:
        reply = "Google khol raha hoon."
        speak(reply)
        webbrowser.open("https://www.google.com")
        return reply
    if "time" in command or "waqt" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        reply = "Waqt hua hai " + current_time
        speak(reply)
        return reply
    if "downloads" in command or "download" in command:
        reply = "Downloads khol raha hoon."
        speak(reply)
        os.system("explorer %USERPROFILE%\\Downloads")
        return reply
    if "documents" in command or "document" in command:
        reply = "Documents khol raha hoon."
        speak(reply)
        os.system("explorer %USERPROFILE%\\Documents")
        return reply
    if "desktop" in command:
        reply = "Desktop khol raha hoon."
        speak(reply)
        os.system("explorer %USERPROFILE%\\Desktop")
        return reply
    return False
