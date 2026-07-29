import os
import datetime
import webbrowser
from memory import load_memory, save_memory
import psutil
import platform
import pyautogui
from pycaw.pycaw import AudioUtilities
import socket
from modules.apps import handle_apps
from modules.browser import handle_browser
from modules.system import handle_system
from modules.notes import handle_notes
from modules.reminder import handle_reminder
from modules.brain import handle_brain
from modules.intent import INTENTS
from modules.intent import detect_intent
from modules.ai import ask_ai
from modules.ai import ask_ai
def handle_command(command, speak):
    command = command.lower()
    intent = detect_intent(command)
    print(f"Detected Intent: {intent}")
   # ------------------- Brain Module -------------------

    reply = handle_brain(command, speak)

    if reply:
        return reply

    # ------------------- Apps Module -------------------
    reply = handle_apps(command, intent, speak)
    if reply:
        return reply

    # ------------------- Browser Module -------------------
    reply = handle_browser(command, speak)
    if reply:
        return reply

    # ------------------- System Module -------------------
    reply = handle_system(command, speak)
    if reply:
        return reply
    # ------------------- Notes Module -------------------

    reply = handle_notes(command, speak)

    if reply:
        return reply
    # ------------------- Reminder Module -------------------

    reply = handle_reminder(command, speak)

    if reply:
        return reply
 
    memory = load_memory()
    # ------------------- Chrome -------------------
    if "chrome" in command or "krom" in command:
        reply = "Chrome khol raha hoon."
        speak(reply)
        os.system("start chrome")
        return reply



    

    # ------------------- Downloads -------------------
    if "downloads" in command or "download" in command:
        reply = "Downloads khol raha hoon."
        speak(reply)
        os.system("explorer %USERPROFILE%\\Downloads")
        return reply

    # ------------------- Documents -------------------
    if "documents" in command or "document" in command:
        reply = "Documents khol raha hoon."
        speak(reply)
        os.system("explorer %USERPROFILE%\\Documents")
        return reply

    # ------------------- Desktop -------------------
    if "desktop" in command:
        reply = "Desktop khol raha hoon."
        speak(reply)
        os.system("explorer %USERPROFILE%\\Desktop")
        return reply
    # ------------------- Memory: Favourite Game -------------------
    if "mera favourite game kya hai" in command:
        if "favourite_game" in memory:
            reply = f"Sir, aapka favourite game {memory['favourite_game']} hai."
        else:
            reply = "Sir, abhi mujhe aapka favourite game yaad nahi hai."
        speak(reply)
        return reply

    if "mera favourite game" in command and "hai" in command:
        game = command.replace("mera favourite game", "").replace("hai", "").strip()
        memory["favourite_game"] = game
        save_memory(memory)
        reply = f"Theek hai Sir, maine yaad rakh liya ke aapka favourite game {game} hai."
        speak(reply)
        return reply
    # ------------------- Battery -------------------
    if "battery" in command:

        battery = psutil.sensors_battery()

        if battery:
            percent = battery.percent
            reply = f"Sir, battery {percent} percent hai."
        else:
            reply = "Sir, battery information available nahi hai."

        speak(reply)
        return reply
        # ------------------- RAM Usage -------------------
    if "ram" in command:

        ram = psutil.virtual_memory()

        total = round(ram.total / (1024 ** 3), 2)
        used = round(ram.used / (1024 ** 3), 2)
        percent = ram.percent

        reply = (
            f"Sir, total RAM {total} GB hai. "
            f"Used RAM {used} GB hai. "
            f"RAM usage {percent} percent hai."
        )

        speak(reply)
        return reply
        # ------------------- CPU Usage -------------------
    if "cpu" in command:

        percent = psutil.cpu_percent(interval=1)

        reply = f"Sir, CPU usage {percent} percent hai."

        speak(reply)
        return reply
        # ------------------- Disk Space -------------------
    if "disk" in command or "storage" in command or "space" in command:

        disk = psutil.disk_usage("C:\\")

        total = round(disk.total / (1024 ** 3), 2)
        used = round(disk.used / (1024 ** 3), 2)
        free = round(disk.free / (1024 ** 3), 2)

        reply = (
            f"Sir, C drive ki total storage {total} GB hai. "
            f"Used {used} GB hai. "
            f"Free {free} GB hai."
        )

        speak(reply)
        return reply
        # ------------------- PC Name -------------------
    if "pc name" in command or "computer name" in command:

        pc_name = os.environ["COMPUTERNAME"]

        reply = f"Sir, aapke computer ka naam {pc_name} hai."

        speak(reply)
        return reply
        # ------------------- Windows Version -------------------
    if "windows" in command or "version" in command:

        version = platform.platform()

        reply = f"Sir, aap {version} use kar rahe hain."

        speak(reply)
        return reply
        # ------------------- System Status -------------------
    if "system status" in command or "status" in command:

        ram = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        disk = psutil.disk_usage("C:\\")
        pc_name = os.environ["COMPUTERNAME"]
        windows = platform.platform()
        current_time = datetime.datetime.now().strftime("%I:%M %p")

        reply = (
            f"Sir, PC Name: {pc_name}. "
            f"Windows: {windows}. "
            f"RAM Usage: {ram.percent} percent. "
            f"CPU Usage: {cpu} percent. "
            f"Free Disk Space: {round(disk.free / (1024**3), 2)} GB. "
            f"Current Time: {current_time}."
        )

        speak(reply)
        return reply
        # ------------------- Screenshot -------------------
    if "screenshot" in command:

        screenshot = pyautogui.screenshot()

        path = os.path.join(
            os.getcwd(),
            "Buddy_Screenshot.png"
)
        screenshot.save(path)

        reply = "Sir, screenshot desktop par save kar diya hai."

        speak(reply)
        return reply
     # ------------------- Volume Control -------------------

    if "volume up" in command or "volume barhao" in command:

        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        current = volume.GetMasterVolumeLevelScalar()

        volume.SetMasterVolumeLevelScalar(
            min(current + 0.1, 1.0),
            None
        )

        reply = "Sir, volume barha diya hai."
        speak(reply)
        return reply


    if "volume down" in command or "volume kam" in command:

        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        current = volume.GetMasterVolumeLevelScalar()

        volume.SetMasterVolumeLevelScalar(
            max(current - 0.1, 0.0),
            None
        )

        reply = "Sir, volume kam kar diya hai."
        speak(reply)
        return reply


    if "mute" in command:

        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        volume.SetMute(1, None)

        reply = "Sir, volume mute kar diya hai."
        speak(reply)
        return reply
    if "unmute" in command or "volume on" in command:

            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume

            volume.SetMute(0, None)

            reply = "Sir, volume wapas on kar diya hai."
            speak(reply)
            return reply
        # ------------------- Internet Check -------------------

    if "internet" in command or "net check" in command:

        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)

            reply = "Sir, internet connected hai."

        except:
            reply = "Sir, internet disconnected hai."

        speak(reply)
        return reply


    # ------------------- AI Fallback -------------------

    reply = ask_ai(command)

    if reply:
        speak(reply)
        return reply
    return "Sir, maaf kijiye. Mujhe jawab nahi mila."