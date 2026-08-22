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
from modules.intent import detect_intent, has_intent

from modules.ai import ask_ai
from modules.history import add_history, last_command, total_conversations, clear_history
from modules.profile import handle_profile
from modules.smart_memory import handle_smart_memory
from modules.ai import ask_ai, extract_memory
from modules.memory import load_memory, save_memory

def handle_command(command, speak):
    previous = last_command()

    command = command.lower().strip()

    intent = detect_intent(command)

    print(f"Detected Intent: {intent}")

    # =========================
    # Profile
    # =========================

    reply = handle_profile(command, speak)

    if reply:
        return reply


    # =========================
    # Buddy Brain
    # =========================

    reply = handle_brain(command, speak)

    if reply:
        return reply

    reply = handle_smart_memory(command, speak)

    if reply:
        return reply

    # =========================
    # Applications
    # =========================

    reply = handle_apps(command, intent, speak)

    if reply:
        return reply



    # =========================
    # Browser
    # =========================

    reply = handle_browser(command, speak)

    if reply:
        return reply



    # =========================
    # System
    # =========================

    reply = handle_system(command, speak)

    if reply:
        return reply



    # =========================
    # Notes
    # =========================

    reply = handle_notes(command, speak)

    if reply:
        return reply

    
    # =========================
    # Reminder
    # =========================

    reply = handle_reminder(command, speak)

    if reply:
        return reply



    memory = load_memory()


    # =========================
    # Conversation Count
    # =========================

    if "kitni baat hui" in command or "conversation count" in command:

        total = total_conversations()

        reply = f"Sir, ab tak hamari {total} conversations save hain."

        speak(reply)
        return reply

    # =========================
    # Clear Conversation History
    # =========================

    if "history clear" in command or "clear history" in command:

        clear_history()

        reply = "Sir, maine conversation history clear kar di hai."

        speak(reply)

        return reply

    # =========================
    # Open Folders
    # =========================

    if "downloads" in command:

        reply = "Sir, Downloads folder khol raha hoon."

        os.system("explorer %USERPROFILE%\\Downloads")

        speak(reply)

        return reply



    if "documents" in command:

        reply = "Sir, Documents folder khol raha hoon."

        os.system("explorer %USERPROFILE%\\Documents")

        speak(reply)

        return reply



    if "desktop" in command:

        reply = "Sir, Desktop khol raha hoon."

        os.system("explorer %USERPROFILE%\\Desktop")

        speak(reply)

        return reply
   


    # =========================
    # PC Name
    # =========================

    if "pc name" in command or "computer name" in command:

        name = os.environ["COMPUTERNAME"]

        reply = (
            f"Sir, aapke computer ka naam {name} hai."
        )

        speak(reply)
        return reply


    # =========================
    # Windows Version
    # =========================

    if (
        "windows version" in command
        or "pc version" in command
        or "system version" in command
    ):

        version = platform.platform()

        reply = f"Sir, aap {version} use kar rahe hain."

        speak(reply)

        return reply



    # =========================
    # Screenshot
    # =========================

    if "screenshot" in command:

        screenshot = pyautogui.screenshot()

        path = os.path.join(
            os.getcwd(),
            "Buddy_Screenshot.png"
        )

        screenshot.save(path)

        reply = (
            "Sir, screenshot save kar diya hai."
        )

        speak(reply)
        return reply



    # =========================
    # Volume Control
    # =========================

    if "volume up" in command or "volume barhao" in command:

        from pycaw.pycaw import AudioUtilities

        devices = AudioUtilities.GetSpeakers()

        volume = devices.EndpointVolume

        current = volume.GetMasterVolumeLevelScalar()

        volume.SetMasterVolumeLevelScalar(
            min(current + 0.1, 1.0),
            None
        )

        reply = (
            "Sir, volume barha diya hai."
        )

        speak(reply)
        return reply



    if "volume down" in command or "volume kam" in command:

        from pycaw.pycaw import AudioUtilities

        devices = AudioUtilities.GetSpeakers()

        volume = devices.EndpointVolume

        current = volume.GetMasterVolumeLevelScalar()

        volume.SetMasterVolumeLevelScalar(
            max(current - 0.1, 0.0),
            None
        )

        reply = (
            "Sir, volume kam kar diya hai."
        )

        speak(reply)
        return reply



    if "mute" in command:

        from pycaw.pycaw import AudioUtilities

        devices = AudioUtilities.GetSpeakers()

        volume = devices.EndpointVolume

        volume.SetMute(1, None)

        reply = (
            "Sir, volume mute kar diya hai."
        )

        speak(reply)
        return reply



    if "unmute" in command or "volume on" in command:

        from pycaw.pycaw import AudioUtilities

        devices = AudioUtilities.GetSpeakers()

        volume = devices.EndpointVolume

        volume.SetMute(0, None)

        reply = (
            "Sir, volume wapas on kar diya hai."
        )

        speak(reply)
        return reply
    # =========================
    # Internet Check
    # =========================

    if "internet" in command or "net check" in command:

        try:

            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=3
            )

            reply = "Sir, internet connected hai."

        except:

            reply = "Sir, internet disconnected hai."


        speak(reply)
        return reply



    # =========================
    # System Status
    # =========================

    if "system status" in command or "status" in command:

        ram = psutil.virtual_memory()

        cpu = psutil.cpu_percent(interval=1)

        disk = psutil.disk_usage("C:\\")

        pc_name = os.environ["COMPUTERNAME"]

        windows = platform.platform()

        time_now = datetime.datetime.now().strftime(
            "%I:%M %p"
        )


        reply = (
            f"Sir, PC Name {pc_name}. "
            f"Windows {windows}. "
            f"RAM usage {ram.percent} percent. "
            f"CPU usage {cpu} percent. "
            f"Free space {round(disk.free/(1024**3),2)} GB. "
            f"Time {time_now}."
        )


        speak(reply)
        return reply
    # =========================
    # Buddy Version
    # =========================

    if (
        "version" in command
        or "buddy version" in command
        or "tumhara version" in command
    ):

        reply = "Sir, main Buddy AI Version 0.3 hoon. Muhammad Saad aur unke Sir mujhe develop kar rahe hain."

        speak(reply)

        return reply

    # =========================
    # Gemini Memory
    # =========================

    memory = extract_memory(command)

    if memory:

        data = load_memory()

        if "profile" not in data:
            data["profile"] = {}

        data["profile"].update(memory)

        save_memory(data)


    # =========================
    # Gemini AI Fallback
    # =========================

    reply = ask_ai(
        command,
        memory_context=str(load_memory().get("profile", {}))
    )

    if reply:
        add_history(command, reply)
        speak(reply)
        return reply