# ==========================================================
# Buddy AI - Commands
# System Commands + Apps + Browser + Notes + Reminders
# Memory + Profile + Date/Time + AI Fallback
# ==========================================================

import os
import datetime
import socket
import platform

import psutil
import pyautogui

from modules.memory import load_memory, save_memory

from modules.apps import handle_apps
from modules.browser import handle_browser

from plugins.system import handle_system

from modules.notes import handle_notes
from modules.reminder import handle_reminder

from modules.brain import handle_brain
from modules.intent import detect_intent

from modules.history import (
    add_history,
    last_command,
    total_conversations,
    clear_history
)

from modules.profile import handle_profile
from modules.smart_memory import handle_smart_memory

from modules.ai import ask_ai, extract_memory


# ==========================================================
# MAIN COMMAND HANDLER
# ==========================================================

def handle_command(command, speak):

    previous = last_command()

    if command is None:
        return None

    command = str(command).lower().strip()

    if not command:
        return None

    intent = detect_intent(command)

    print(
        f"Detected Intent: {intent}"
    )

    # ======================================================
    # PROFILE
    # ======================================================

    reply = handle_profile(
        command,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # BUDDY BRAIN
    # ======================================================

    reply = handle_brain(
        command,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # SMART MEMORY
    # ======================================================

    reply = handle_smart_memory(
        command,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # APPLICATIONS
    # ======================================================

    reply = handle_apps(
        command,
        intent,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # BROWSER
    # ======================================================

    reply = handle_browser(
        command,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # SYSTEM
    # ======================================================

    reply = handle_system(
        command,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # NOTES
    # ======================================================

    reply = handle_notes(
        command,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # REMINDER
    # ======================================================

    reply = handle_reminder(
        command,
        speak
    )

    if reply:
        return reply

    # ======================================================
    # LOAD MEMORY
    # ======================================================

    memory = load_memory()

    # ======================================================
    # DATE & TIME
    # ======================================================

    if (
        "what time" in command
        or "time kya hai" in command
        or "abhi time" in command
        or "kitne baje" in command
        or "time batao" in command
        or "current time" in command
    ):

        now = datetime.datetime.now()

        time_now = now.strftime(
            "%I:%M %p"
        )

        reply = (
            f"Sir, abhi {time_now} ho rahe hain."
        )

        speak(reply)

        return reply

    if (
        "aaj ki date" in command
        or "aaj date kya hai" in command
        or "date kya hai" in command
        or "today date" in command
        or "aaj kya date hai" in command
        or "today ki date" in command
    ):

        now = datetime.datetime.now()

        date_now = now.strftime(
            "%d %B %Y"
        )

        day_now = now.strftime(
            "%A"
        )

        reply = (
            f"Sir, aaj {day_now}, "
            f"{date_now} hai."
        )

        speak(reply)

        return reply

    # ======================================================
    # CONVERSATION COUNT
    # ======================================================

    if (
        "kitni baat hui" in command
        or "conversation count" in command
        or "kitni conversations" in command
    ):

        total = total_conversations()

        reply = (
            f"Sir, ab tak hamari "
            f"{total} conversations save hain."
        )

        speak(reply)

        return reply

    # ======================================================
    # CLEAR CONVERSATION HISTORY
    # ======================================================

    if (
        "history clear" in command
        or "clear history" in command
    ):

        clear_history()

        reply = (
            "Sir, maine conversation "
            "history clear kar di hai."
        )

        speak(reply)

        return reply

    # ======================================================
    # OPEN DOWNLOADS
    # ======================================================

    if "downloads" in command:

        reply = (
            "Sir, Downloads folder "
            "khol raha hoon."
        )

        os.system(
            "explorer %USERPROFILE%\\Downloads"
        )

        speak(reply)

        return reply

    # ======================================================
    # OPEN DOCUMENTS
    # ======================================================

    if "documents" in command:

        reply = (
            "Sir, Documents folder "
            "khol raha hoon."
        )

        os.system(
            "explorer %USERPROFILE%\\Documents"
        )

        speak(reply)

        return reply

    # ======================================================
    # OPEN DESKTOP
    # ======================================================

    if "desktop" in command:

        reply = (
            "Sir, Desktop khol raha hoon."
        )

        os.system(
            "explorer %USERPROFILE%\\Desktop"
        )

        speak(reply)

        return reply

    # ======================================================
    # PC NAME
    # ======================================================

    if (
        "pc name" in command
        or "computer name" in command
    ):

        name = os.environ.get(
            "COMPUTERNAME",
            "Unknown"
        )

        reply = (
            f"Sir, aapke computer ka naam "
            f"{name} hai."
        )

        speak(reply)

        return reply

    # ======================================================
    # WINDOWS VERSION
    # ======================================================

    if (
        "windows version" in command
        or "pc version" in command
        or "system version" in command
    ):

        version = platform.platform()

        reply = (
            f"Sir, aap {version} "
            f"use kar rahe hain."
        )

        speak(reply)

        return reply

    # ======================================================
    # SCREENSHOT
    # ======================================================

    if "screenshot" in command:

        try:

            screenshot = pyautogui.screenshot()

            path = os.path.join(
                os.getcwd(),
                "Buddy_Screenshot.png"
            )

            screenshot.save(path)

            reply = (
                "Sir, screenshot save "
                "kar diya hai."
            )

        except Exception as e:

            print(
                "Screenshot Error:",
                repr(e)
            )

            reply = (
                "Sir, screenshot lene mein "
                "problem aa gayi."
            )

        speak(reply)

        return reply

    # ======================================================
    # VOLUME UP
    # ======================================================

    if (
        "volume up" in command
        or "volume barhao" in command
        or "volume barha do" in command
    ):

        try:

            from pycaw.pycaw import (
                AudioUtilities
            )

            devices = (
                AudioUtilities.GetSpeakers()
            )

            volume = devices.EndpointVolume

            current = (
                volume.GetMasterVolumeLevelScalar()
            )

            volume.SetMasterVolumeLevelScalar(
                min(
                    current + 0.1,
                    1.0
                ),
                None
            )

            reply = (
                "Sir, volume barha diya hai."
            )

        except Exception as e:

            print(
                "Volume Up Error:",
                repr(e)
            )

            reply = (
                "Sir, volume barhane mein "
                "problem aa gayi."
            )

        speak(reply)

        return reply

    # ======================================================
    # VOLUME DOWN
    # ======================================================

    if (
        "volume down" in command
        or "volume kam" in command
        or "volume kam karo" in command
    ):

        try:

            from pycaw.pycaw import (
                AudioUtilities
            )

            devices = (
                AudioUtilities.GetSpeakers()
            )

            volume = devices.EndpointVolume

            current = (
                volume.GetMasterVolumeLevelScalar()
            )

            volume.SetMasterVolumeLevelScalar(
                max(
                    current - 0.1,
                    0.0
                ),
                None
            )

            reply = (
                "Sir, volume kam kar diya hai."
            )

        except Exception as e:

            print(
                "Volume Down Error:",
                repr(e)
            )

            reply = (
                "Sir, volume kam karne mein "
                "problem aa gayi."
            )

        speak(reply)

        return reply

    # ======================================================
    # MUTE
    # ======================================================

    if "mute" in command:

        try:

            from pycaw.pycaw import (
                AudioUtilities
            )

            devices = (
                AudioUtilities.GetSpeakers()
            )

            volume = devices.EndpointVolume

            volume.SetMute(
                1,
                None
            )

            reply = (
                "Sir, volume mute kar diya hai."
            )

        except Exception as e:

            print(
                "Mute Error:",
                repr(e)
            )

            reply = (
                "Sir, volume mute karne mein "
                "problem aa gayi."
            )

        speak(reply)

        return reply

    # ======================================================
    # UNMUTE
    # ======================================================

    if (
        "unmute" in command
        or "volume on" in command
    ):

        try:

            from pycaw.pycaw import (
                AudioUtilities
            )

            devices = (
                AudioUtilities.GetSpeakers()
            )

            volume = devices.EndpointVolume

            volume.SetMute(
                0,
                None
            )

            reply = (
                "Sir, volume wapas on kar diya hai."
            )

        except Exception as e:

            print(
                "Unmute Error:",
                repr(e)
            )

            reply = (
                "Sir, volume on karne mein "
                "problem aa gayi."
            )

        speak(reply)

        return reply

    # ======================================================
    # INTERNET CHECK
    # ======================================================

    if (
        "internet" in command
        or "net check" in command
    ):

        try:

            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=3
            )

            reply = (
                "Sir, internet connected hai."
            )

        except Exception:

            reply = (
                "Sir, internet disconnected hai."
            )

        speak(reply)

        return reply

    # ======================================================
    # SYSTEM STATUS
    # ======================================================

    if (
        "system status" in command
        or "status" in command
    ):

        try:

            ram = psutil.virtual_memory()

            cpu = psutil.cpu_percent(
                interval=1
            )

            disk = psutil.disk_usage(
                "C:\\"
            )

            pc_name = os.environ.get(
                "COMPUTERNAME",
                "Unknown"
            )

            windows = platform.platform()

            time_now = datetime.datetime.now().strftime(
                "%I:%M %p"
            )

            free_space = round(
                disk.free / (1024 ** 3),
                2
            )

            reply = (
                f"Sir, PC Name {pc_name}. "
                f"Windows {windows}. "
                f"RAM usage {ram.percent} percent. "
                f"CPU usage {cpu} percent. "
                f"Free space {free_space} GB. "
                f"Time {time_now}."
            )

        except Exception as e:

            print(
                "System Status Error:",
                repr(e)
            )

            reply = (
                "Sir, system status "
                "read nahi ho saka."
            )

        speak(reply)

        return reply

    # ======================================================
    # BUDDY VERSION
    # ======================================================

    if (
        "buddy version" in command
        or "tumhara version" in command
    ):

        reply = (
            "Sir, main Buddy AI hoon. "
            "Mujhe Muhammad Saad aur unke Sir "
            "develop kar rahe hain."
        )

        speak(reply)

        return reply

    # ======================================================
    # MEMORY EXTRACTION
    # ======================================================

    try:

        extracted_memory = extract_memory(
            command
        )

        if extracted_memory:

            data = load_memory()

            if "profile" not in data:
                data["profile"] = {}

            if isinstance(
                data["profile"],
                dict
            ):

                data["profile"].update(
                    extracted_memory
                )

            save_memory(data)

            print(
                "Command Memory Saved:",
                extracted_memory
            )

    except Exception as e:

        print(
            "Memory Extraction Error:",
            repr(e)
        )

    # ======================================================
    # GEMINI AI FALLBACK
    # ======================================================

    try:

        reply = ask_ai(
            command,
            memory_context=str(
                load_memory().get(
                    "profile",
                    {}
                )
            )
        )

    except Exception as e:

        print(
            "AI Command Error:",
            repr(e)
        )

        reply = None

    if reply:

        reply = str(
            reply
        ).strip()

        try:

            add_history(
                command,
                reply
            )

        except Exception as e:

            print(
                "History Error:",
                repr(e)
            )

        speak(reply)

        return reply

    # ======================================================
    # NOTHING HANDLED
    # ======================================================

    return None