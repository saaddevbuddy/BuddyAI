import json
import os
import datetime
import re


# ----------------------------------------
# Buddy AI - Smart Reminder System
# ----------------------------------------

MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "memory.json"
)


# ----------------------------------------
# Memory Functions
# ----------------------------------------

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        print("Memory Load Error:", e)
        return {}


def save_memory(memory):

    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as e:
        print("Memory Save Error:", e)
        return False


# ----------------------------------------
# Date Detection
# ----------------------------------------

def get_reminder_date(command):

    today = datetime.date.today()

    if "kal" in command:
        return today + datetime.timedelta(days=1)

    return today


# ----------------------------------------
# Time Detection
# ----------------------------------------
def get_reminder_time(command):

    command = command.lower().strip()

    # 9:13 am / 9:13 pm
    match = re.search(
        r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b",
        command
    )

    if match:

        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        period = match.group(3)

        if hour == 12:
            hour = 0

        if period == "pm":
            hour += 12

        return datetime.time(hour, minute)

    # 24-hour format: 21:30
    match = re.search(
        r"\b(\d{1,2}):(\d{2})\b",
        command
    )

    if match:

        hour = int(match.group(1))
        minute = int(match.group(2))

        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return datetime.time(hour, minute)

    # 8 baje
    match = re.search(
        r"\b(\d{1,2})\s*baje\b",
        command
    )

    if match:

        hour = int(match.group(1))
        minute = 0

        if "shaam" in command or "raat" in command:
            if hour < 12:
                hour += 12

        elif "dopahar" in command:
            if hour < 12:
                hour += 12

        return datetime.time(hour, minute)

    return None


# ----------------------------------------
# Clean Reminder Text
# ----------------------------------------

def clean_reminder_text(command):

    text = command

    # Reminder keyword remove
    text = re.sub(
        r"^\s*reminder\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Date/time phrases remove
    phrases = [
        "kal subah",
        "kal shaam",
        "kal dopahar",
        "kal raat",
        "kal",
        "aaj subah",
        "aaj shaam",
        "aaj dopahar",
        "aaj raat",
        "aaj",
    ]

    for phrase in phrases:
        text = text.replace(phrase, "")

        # Time remove
    text = re.sub(
        r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm)?\s*baje\b",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm)\b",
        "",
        text,
        flags=re.IGNORECASE
    )
    # Reminder phrases remove
    phrases = [
        "yaad dilana",
        "yaad dila dena",
        "yaad dila do",
        "ka reminder lagao",
        "reminder lagao",
        "reminder laga do",
    ]

    for phrase in phrases:
        text = text.replace(phrase, "")

    text = re.sub(r"\s+", " ", text).strip()

    return text


# ----------------------------------------
# Handle Reminder
# ----------------------------------------

def handle_reminder(command, speak):

    command = command.lower().strip()

    memory = load_memory()

    if "reminders" not in memory:
        memory["reminders"] = []

    # ----------------------------------------
    # Show Today's Reminders
    # ----------------------------------------

    if (
        "aaj ke reminders" in command
        or "aaj k reminders" in command
    ):

        today = datetime.date.today().isoformat()

        reminders = [
            r for r in memory["reminders"]
            if r.get("date") == today
        ]

        if not reminders:

            reply = "Sir, aaj koi reminder nahi hai."
            speak(reply)
            return reply

        reply = "Sir, aaj ke reminders hain:\n"

        for index, reminder in enumerate(reminders, 1):

            task = reminder.get("task", "Unknown")
            reminder_time = reminder.get("time", "")
            completed = reminder.get("completed", False)

            status = "✅ Complete" if completed else "⏳ Pending"

            reply += (
                f"{index}. {task} — "
                f"{reminder_time} — {status}\n"
            )

        speak(reply)
        return reply

    # ----------------------------------------
    # Show Tomorrow's Reminders
    # ----------------------------------------

    if (
        "kal ke reminders" in command
        or "kal k reminders" in command
        or "kal ke mere reminders" in command
    ):

        tomorrow = (
            datetime.date.today()
            + datetime.timedelta(days=1)
        ).isoformat()

        reminders = [
            r for r in memory["reminders"]
            if r.get("date") == tomorrow
        ]

        if not reminders:

            reply = "Sir, kal koi reminder nahi hai."
            speak(reply)
            return reply

        reply = "Sir, kal ke reminders hain:\n"

        for index, reminder in enumerate(reminders, 1):

            task = reminder.get("task", "Unknown")
            reminder_time = reminder.get("time", "")
            completed = reminder.get("completed", False)

            status = "✅ Complete" if completed else "⏳ Pending"

            reply += (
                f"{index}. {task} — "
                f"{reminder_time} — {status}\n"
            )

        speak(reply)
        return reply
    # ----------------------------------------
    # Show Pending Reminders
    # ----------------------------------------

    if (
        "pending reminders" in command
        or "pending reminder" in command
        or "baqi reminders" in command
        or "remaining reminders" in command
    ):

        reminders = [
            r for r in memory.get("reminders", [])
            if not r.get("completed", False)
        ]

        if not reminders:

            reply = "Sir, koi pending reminder nahi hai."
            speak(reply)
            return reply

        reply = "Sir, aapke pending reminders hain:\n"

        for index, reminder in enumerate(reminders, 1):

            task = reminder.get("task", "Unknown")
            date = reminder.get("date", "")
            reminder_time = reminder.get("time", "")

            reply += (
                f"{index}. {task} — "
                f"{date} {reminder_time}\n"
            )

        speak(reply)
        return reply


    # ----------------------------------------
    # Complete Reminder
    # ----------------------------------------

    if (
        "complete reminder" in command
        or "reminder complete" in command
        or "reminder mukammal" in command
        or "reminder khatam" in command
    ):

        reminders = memory.get("reminders", [])

        # Number se complete
        match = re.search(r"\b(\d+)\b", command)

        if match:

            number = int(match.group(1))

            pending = [
                r for r in reminders
                if not r.get("completed", False)
            ]

            if 1 <= number <= len(pending):

                pending[number - 1]["completed"] = True

                save_memory(memory)

                task = pending[number - 1].get(
                    "task",
                    "reminder"
                )

                reply = (
                    f"Ji Sir, {task} ka reminder "
                    f"complete kar diya hai."
                )

                speak(reply)
                return reply

        reply = (
            "Sir, reminder number bhi bata dein. "
            "Misal ke taur par: reminder 1 complete kar do."
        )

        speak(reply)
        return reply


        # ----------------------------------------
    # Delete Reminder
    # ----------------------------------------

    if (
        "delete reminder" in command
        or "remove reminder" in command
        or "reminder delete" in command
        or "reminder hatao" in command
        or "reminder hata do" in command
        or re.search(r"\breminders?\s+\d+\s+(delete|remove|hata)", command)
        or re.search(r"\bmera\s+reminder\s+\d+\s+(delete|remove|hata)", command)
        or re.search(r"\bmeri\s+reminder\s+\d+\s+(delete|remove|hata)", command)
    ):

        reminders = memory.get("reminders", [])

        match = re.search(r"\b(\d+)\b", command)

        if match:

            number = int(match.group(1))

            pending = [
                r for r in reminders
                if not r.get("completed", False)
            ]

            if 1 <= number <= len(pending):

                reminder_to_delete = pending[number - 1]

                memory["reminders"].remove(
                    reminder_to_delete
                )

                save_memory(memory)

                task = reminder_to_delete.get(
                    "task",
                    "reminder"
                )

                reply = (
                    f"Ji Sir, {task} ka reminder "
                    f"delete kar diya hai."
                )

                speak(reply)
                return reply

        reply = (
            "Sir, reminder number bhi bata dein. "
            "Misal ke taur par: reminder 1 delete kar do."
        )

        speak(reply)
        return reply
    # ----------------------------------------
    # Show All Reminders
    # ----------------------------------------

    if (
        "show reminders" in command
        or "reminders dikhao" in command
        or "meri reminders" in command
        or "mere reminders" in command
        or "my reminders" in command
    ):

        reminders = memory.get("reminders", [])

        if not reminders:

            reply = "Sir, reminder list khali hai."
            speak(reply)
            return reply

        reply = "Sir, ye aapke reminders hain:\n"

        for index, reminder in enumerate(reminders, 1):

            task = reminder.get("task", "Unknown")
            date = reminder.get("date", "")
            reminder_time = reminder.get("time", "")
            completed = reminder.get("completed", False)

            status = "✅ Complete" if completed else "⏳ Pending"

            reply += (
                f"{index}. {task} — "
                f"{date} {reminder_time} — {status}\n"
            )

        speak(reply)
        return reply

    # ----------------------------------------
    # Clear Reminders
    # ----------------------------------------

    if (
        "clear reminders" in command
        or "delete reminders" in command
        or "remove reminders" in command
    ):

        memory["reminders"] = []

        if save_memory(memory):

            reply = "Sir, saare reminders delete kar diye hain."

        else:

            reply = "Sir, reminders delete karte waqt masla aa gaya."

        speak(reply)
        return reply

    # ----------------------------------------
    # Save Reminder
    # ----------------------------------------

    if (
        command.startswith("reminder ")
        or "yaad dilana" in command
        or "yaad dila do" in command
        or "reminder lagao" in command
        or "reminder laga do" in command
    ):

        reminder_text = clean_reminder_text(command)

        if not reminder_text:

            reply = "Sir, kis cheez ka reminder lagana hai?"
            speak(reply)
            return reply

        reminder_date = get_reminder_date(command)
        reminder_time = get_reminder_time(command)

        if reminder_time:
            time_text = reminder_time.strftime("%I:%M %p")
        else:
            time_text = ""

        reminder = {
            "task": reminder_text,
            "date": reminder_date.isoformat(),
            "time": time_text,
            "completed": False
        }

        memory["reminders"].append(reminder)

        if save_memory(memory):

            date_text = reminder_date.strftime("%d-%m-%Y")

            if time_text:
                reply = (
                    f"Ji Sir, {date_text} ko {time_text} "
                    f"ke liye {reminder_text} ka reminder laga diya hai."
                )
            else:
                reply = (
                    f"Ji Sir, {date_text} ke liye "
                    f"{reminder_text} ka reminder laga diya hai."
                )

        else:

            reply = "Sir, reminder save karte waqt masla aa gaya."

        speak(reply)
        return reply

    return None