import webbrowser
import os

def handle_browser(command, speak):

    # ------------------- YouTube Search -------------------

    if "youtube" in command and "search" in command:

        query = (
            command.replace("youtube par", "")
                   .replace("youtube per", "")
                   .replace("youtube pe", "")
                   .replace("youtube", "")
                   .replace("search karo", "")
                   .replace("search", "")
                   .strip()
        )

        reply = f"YouTube par {query} search kar raha hoon."
        speak(reply)

        webbrowser.open(
            f"https://www.youtube.com/results?search_query={query}"
        )

        return reply

    # ------------------- YouTube -------------------

    if "youtube" in command:
        reply = "YouTube khol raha hoon."
        speak(reply)
        webbrowser.open("https://www.youtube.com")
        return reply

    # ------------------- Google Search -------------------

    if "google" in command and "search" in command:

        query = (
            command.replace("google par", "")
                   .replace("google per", "")
                   .replace("google pe", "")
                   .replace("google", "")
                   .replace("search karo", "")
                   .replace("search", "")
                   .strip()
        )

        reply = f"Google par {query} search kar raha hoon."
        speak(reply)

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )

        return reply


    # ------------------- Google -------------------

    if "google" in command:

        reply = "Google khol raha hoon."
        speak(reply)

        webbrowser.open("https://www.google.com")

        return reply


    # ------------------- ChatGPT -------------------

    if "chatgpt" in command:

        reply = "ChatGPT khol raha hoon."
        speak(reply)

        webbrowser.open("https://chatgpt.com")

        return reply
    
    return None