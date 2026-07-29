import os
import datetime
import socket
import platform

import psutil
import pyautogui

from memory import load_memory, save_memory

from modules.apps import handle_apps
from modules.browser import handle_browser
from modules.system import handle_system
from modules.notes import handle_notes
from modules.reminder import handle_reminder

from modules.brain import handle_brain
from modules.intent import detect_intent

from modules.ai import ask_ai
from modules.history import add_history, last_command, total_conversations, clear_history

def handle_command(command, speak):
    previous = last_command()

    command = command.lower().strip()

    intent = detect_intent(command)

    print(f"Detected Intent: {intent}")


    # =========================
    # Buddy Brain
    # =========================

    reply = handle_brain(command, speak)

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
    # Favourite Game Memory
    # =========================

    if (
        "mera favourite game" in command
        and (
                "kya hai" in command
                or "kon sa" in command
                or "kaun sa" in command
                or "yaad hai" in command
            )
    ):
        if "favourite_game" in memory:
            reply = f"Sir, aapka favourite game {memory['favourite_game']} hai."
        else:
            reply = "Sir, mujhe abhi aapka favourite game yaad nahi hai."

        speak(reply)
        return reply



    if "mera favourite game" in command and "hai" in command:

        game = (
            command
            .replace("mera favourite game", "")
            .replace("hai", "")
            .strip()
        )

        memory["favourite_game"] = game

        save_memory(memory)

        reply = (
            f"Theek hai Sir, maine yaad rakh liya "
            f"ke aapka favourite game {game} hai."
        )

        speak(reply)
        return reply



    # =========================
    # Battery Information
    # =========================

    if "battery" in command:

        battery = psutil.sensors_battery()

        if battery:

            reply = (
                f"Sir, battery {battery.percent} percent hai."
            )

        else:

            reply = (
                "Sir, battery information available nahi hai."
            )

        speak(reply)
        return reply



    # =========================
    # RAM Information
    # =========================

    if "ram" in command:

        ram = psutil.virtual_memory()

        total = round(
            ram.total / (1024 ** 3), 2
        )

        used = round(
            ram.used / (1024 ** 3), 2
        )

        reply = (
            f"Sir, total RAM {total} GB hai. "
            f"Used RAM {used} GB hai. "
            f"RAM usage {ram.percent} percent hai."
        )

        speak(reply)
        return reply



    # =========================
    # CPU Usage
    # =========================

    if "cpu" in command:

        cpu = psutil.cpu_percent(interval=1)

        reply = (
            f"Sir, CPU usage {cpu} percent hai."
        )

        speak(reply)
        return reply



    # =========================
    # Disk Storage
    # =========================

    if (
        "disk" in command
        or "storage" in command
        or "space" in command
    ):

        disk = psutil.disk_usage("C:\\")

        total = round(
            disk.total / (1024 ** 3), 2
        )

        free = round(
            disk.free / (1024 ** 3), 2
        )


        reply = (
            f"Sir, C drive total {total} GB hai. "
            f"Free space {free} GB hai."
        )

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

    if "windows" in command or "version" in command:

        version = platform.platform()

        reply = (
            f"Sir, aap {version} use kar rahe hain."
        )

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
    # Gemini AI Fallback
    # =========================

    reply = ask_ai(command)

    if reply:
        add_history(command, reply)
        speak(reply)
        return reply

    # =========================
    # No Answer
    # =========================

    reply = "Sir, mujhe is baat ka jawab nahi mila."

    speak(reply)

    return reply