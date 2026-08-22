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
# Check Reminders
# ----------------------------------------

def check_reminders(speak):

    memory = load_memory()

    reminders = memory.get("reminders", [])

    now = datetime.datetime.now()

    print(
        f"🕐 Scheduler Check: "
        f"{now.strftime('%Y-%m-%d %I:%M:%S %p')}"
    )

    if not reminders:
        print("📭 No reminders found.")
        return

    changed = False

    for reminder in reminders:

        print(
            f"📌 Reminder: "
            f"{reminder.get('task')} | "
            f"{reminder.get('date')} | "
            f"{reminder.get('time')} | "
            f"Completed: {reminder.get('completed')}"
        )

        if reminder.get("completed", False):
            continue

        reminder_date = reminder.get("date", "")
        reminder_time = reminder.get("time", "")

        if not reminder_date or not reminder_time:
            continue

        try:

            reminder_datetime = datetime.datetime.strptime(
                f"{reminder_date} {reminder_time}",
                "%Y-%m-%d %I:%M %p"
            )

        except ValueError as e:

            print("❌ Date/Time Parse Error:", e)
            continue

        print(
            f"🎯 Target: "
            f"{reminder_datetime.strftime('%Y-%m-%d %I:%M:%S %p')}"
        )

        if now >= reminder_datetime:

            task = reminder.get(
                "task",
                "aapka reminder"
            )

            print(f"\n🔔 REMINDER TRIGGERED: {task}")

            speak(
                f"Sir, reminder! "
                f"{task} ka waqt ho gaya hai."
            )

            reminder["completed"] = True
            changed = True

    if changed:
        save_memory(memory)
        print("✅ Reminder marked completed.")

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