import json
import os
import time
import threading
import datetime


# ----------------------------------------
# Buddy AI - Reminder Scheduler
# ----------------------------------------

MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "memory.json"
)


# ----------------------------------------
# Load Memory
# ----------------------------------------

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        print("Scheduler Memory Error:", e)
        return {}


# ----------------------------------------
# Save Memory
# ----------------------------------------

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
        print("Scheduler Save Error:", e)
        return False


# ----------------------------------------
# Parse Reminder Date/Time
# ----------------------------------------

def parse_reminder_datetime(date_value, time_value):
    """
    Supports:
    YYYY-MM-DD HH:MM AM/PM
    YYYY-MM-DD HH:MM
    """

    if not date_value or not time_value:
        return None

    date_value = str(date_value).strip()
    time_value = str(time_value).strip()

    formats = [
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d %I:%M:%S %p",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.datetime.strptime(
                f"{date_value} {time_value}",
                fmt
            )
        except ValueError:
            continue

    return None


# ----------------------------------------
# Check Reminders
# ----------------------------------------

def check_reminders(speak):

    memory = load_memory()
    reminders = memory.get("reminders", [])

    now = datetime.datetime.now()

    if not isinstance(reminders, list):
        return

    changed = False

    for reminder in reminders:

        if not isinstance(reminder, dict):
            continue

        # Completed reminders ko ignore karo
        if reminder.get("completed", False):
            continue

        task = str(
            reminder.get("task", "aapka reminder")
        ).strip()

        reminder_date = reminder.get("date", "")
        reminder_time = reminder.get("time", "")

        # Incomplete reminder ko ignore karo
        if not reminder_date or not reminder_time:
            continue

        reminder_datetime = parse_reminder_datetime(
            reminder_date,
            reminder_time
        )

        # Invalid date/time ko ignore karo
        if reminder_datetime is None:
            continue

        # Reminder ka waqt aa gaya
        if now >= reminder_datetime:

            print(f"\n🔔 REMINDER: {task}")

            try:
                speak(
                    f"Sir, reminder! "
                    f"{task} ka waqt ho gaya hai."
                )
            except Exception as e:
                print("Reminder Voice Error:", e)

            reminder["completed"] = True
            changed = True

    if changed:
        save_memory(memory)


# ----------------------------------------
# Background Scheduler
# ----------------------------------------

def reminder_loop(speak):

    print("⏰ Reminder Scheduler Started")

    while True:

        try:
            check_reminders(speak)

        except Exception as e:
            print("Scheduler Error:", e)

        # Har 20 seconds mein check
        time.sleep(20)


# ----------------------------------------
# Start Scheduler
# ----------------------------------------

def start_scheduler(speak):

    scheduler_thread = threading.Thread(
        target=reminder_loop,
        args=(speak,),
        daemon=True
    )

    scheduler_thread.start()

    return scheduler_thread