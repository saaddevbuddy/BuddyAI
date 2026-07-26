import os
import datetime


def handle_reminder(command, speak):

    reminder_file = "reminders.txt"

    # ------------------- Save Reminder -------------------

    if command.startswith("reminder "):

        reminder = command.replace("reminder", "", 1).strip()

        current_time = datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p")

        with open(reminder_file, "a", encoding="utf-8") as file:
            file.write(f"[{current_time}] {reminder}\n")

        reply = "Sir, reminder save kar diya hai."
        speak(reply)
        return reply

    # ------------------- Show Reminders -------------------

    if (
        "show reminders" in command
        or "reminders dikhao" in command
        or "meri reminders" in command
    ):

        if not os.path.exists(reminder_file):

            reply = "Sir, abhi koi reminder save nahi hai."
            speak(reply)
            return reply

        with open(reminder_file, "r", encoding="utf-8") as file:

            reminders = file.read().strip()

        if reminders:

            reply = "Sir, ye aapke reminders hain.\n" + reminders

        else:

            reply = "Sir, reminder list khali hai."

        speak(reply)
        return reply
    # ------------------- Clear Reminders -------------------

    if (
        "clear reminders" in command
        or "delete reminders" in command
        or "remove reminders" in command
    ):

        if os.path.exists(reminder_file):
            open(reminder_file, "w", encoding="utf-8").close()

        reply = "Sir, saare reminders delete kar diye hain."
        speak(reply)
        return reply

    return None