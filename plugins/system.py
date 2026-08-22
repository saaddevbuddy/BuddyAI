import os
import socket
import datetime
import psutil
import platform
import pyautogui
import subprocess
import webbrowser

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


def handle_system(command, speak):

    command = command.lower().strip()

    # ==================================================
    # TIME
    # ==================================================

    if "time" in command or "waqt" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        reply = f"Sir, waqt hua hai {current_time}."
        speak(reply)

        return reply

    # ==================================================
    # INTERNET CHECK
    # ==================================================

    if (
        "internet status" in command
        or "internet check" in command
        or "net check" in command
        or command == "internet"
    ):

        try:
            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=3
            )

            reply = "Sir, internet connected hai."

        except OSError:

            reply = "Sir, internet disconnected hai."

        speak(reply)
        return reply

    # ==================================================
    # SYSTEM STATUS
    # ==================================================

    if (
        "system status" in command
        or "system information" in command
        or "system info" in command
        or "pc information" in command
        or "pc info" in command
    ):

        uname = platform.uname()

        ram = psutil.virtual_memory()

        disk = psutil.disk_usage("C:\\")

        cpu = psutil.cpu_percent(interval=1)

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        reply = (
            f"Sir, PC Name {uname.node}. "
            f"System {uname.system}. "
            f"Windows {uname.release}. "
            f"RAM usage {ram.percent} percent. "
            f"CPU usage {cpu} percent. "
            f"C drive mein "
            f"{round(disk.free / (1024 ** 3), 2)} GB free hai. "
            f"Current time {current_time}."
        )

        speak(reply)
        return reply

    # ==================================================
    # SCREENSHOT
    # ==================================================

    if (
        "screenshot" in command
        or "screen shot" in command
    ):

        try:

            pictures = os.path.join(
                os.path.expanduser("~"),
                "Pictures"
            )

            os.makedirs(
                pictures,
                exist_ok=True
            )

            filename = datetime.datetime.now().strftime(
                "Buddy_Screenshot_%Y%m%d_%H%M%S.png"
            )

            path = os.path.join(
                pictures,
                filename
            )

            screenshot = pyautogui.screenshot()
            screenshot.save(path)

            reply = (
                f"Ji Sir, screenshot save kar diya hai."
            )

        except Exception as e:

            print("Screenshot Error:", e)

            reply = (
                "Sir, screenshot save karne mein "
                "problem aa gayi."
            )

        speak(reply)
        return reply

    # ==================================================
    # MUTE
    # ==================================================

    if (
        command == "mute"
        or "volume mute" in command
        or "sound mute" in command
    ):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

        volume.SetMute(1, None)

        reply = "Sir, volume mute kar diya hai."

        speak(reply)
        return reply

    # ==================================================
    # UNMUTE
    # ==================================================

    if (
        command == "unmute"
        or "volume unmute" in command
        or "sound unmute" in command
    ):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

        volume.SetMute(0, None)

        reply = "Sir, volume unmute kar diya hai."

        speak(reply)
        return reply

    # ==================================================
    # VOLUME UP
    # ==================================================

    if (
        "volume up" in command
        or "increase volume" in command
        or "volume barhao" in command
    ):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

        current = volume.GetMasterVolumeLevelScalar()

        volume.SetMasterVolumeLevelScalar(
            min(current + 0.10, 1.0),
            None
        )

        reply = "Sir, volume barha diya hai."

        speak(reply)
        return reply

    # ==================================================
    # VOLUME DOWN
    # ==================================================

    if (
        "volume down" in command
        or "decrease volume" in command
        or "volume kam" in command
    ):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

        current = volume.GetMasterVolumeLevelScalar()

        volume.SetMasterVolumeLevelScalar(
            max(current - 0.10, 0.0),
            None
        )

        reply = "Sir, volume kam kar diya hai."

        speak(reply)
        return reply

    # ==================================================
    # BATTERY
    # ==================================================

    if "battery" in command:

        battery = psutil.sensors_battery()

        if battery:

            charging = (
                "aur charging par hai"
                if battery.power_plugged
                else "aur charging par nahi hai"
            )

            reply = (
                f"Sir, battery {battery.percent} percent hai "
                f"{charging}."
            )

        else:

            reply = (
                "Sir, battery information available nahi hai."
            )

        speak(reply)
        return reply

    # ==================================================
    # RAM
    # ==================================================

    if (
        command == "ram"
        or "ram status" in command
        or "ram kitni" in command
    ):

        ram = psutil.virtual_memory()

        total = round(
            ram.total / (1024 ** 3),
            2
        )

        used = round(
            ram.used / (1024 ** 3),
            2
        )

        available = round(
            ram.available / (1024 ** 3),
            2
        )

        reply = (
            f"Sir, total RAM {total} GB hai. "
            f"Used RAM {used} GB hai. "
            f"Available RAM {available} GB hai. "
            f"Usage {ram.percent} percent hai."
        )

        speak(reply)
        return reply

    # ==================================================
    # CPU
    # ==================================================

    if (
        command == "cpu"
        or "cpu status" in command
        or "cpu usage" in command
    ):

        cpu = psutil.cpu_percent(interval=1)

        reply = (
            f"Sir, CPU usage {cpu} percent hai."
        )

        speak(reply)
        return reply

    # ==================================================
    # DISK / STORAGE
    # ==================================================

    if (
        "disk" in command
        or "storage" in command
        or "space" in command
    ):

        disk = psutil.disk_usage("C:\\")

        total = round(
            disk.total / (1024 ** 3),
            2
        )

        used = round(
            disk.used / (1024 ** 3),
            2
        )

        free = round(
            disk.free / (1024 ** 3),
            2
        )

        reply = (
            f"Sir, C drive total {total} GB hai. "
            f"Used {used} GB hai. "
            f"Free space {free} GB hai."
        )

        speak(reply)
        return reply

    # ==================================================
    # PC NAME
    # ==================================================

    if (
        "pc name" in command
        or "computer name" in command
    ):

        name = os.environ.get(
            "COMPUTERNAME",
            platform.node()
        )

        reply = (
            f"Sir, aapke computer ka naam {name} hai."
        )

        speak(reply)
        return reply

    # ==================================================
    # WINDOWS VERSION
    # ==================================================

    if (
        "windows version" in command
        or "pc version" in command
        or "system version" in command
    ):

        version = platform.platform()

        reply = (
            f"Sir, aap {version} use kar rahe hain."
        )

        speak(reply)
        return reply

    # ==================================================
    # OPEN CHROME
    # ==================================================

    if (
        "chrome kholo" in command
        or "chrome open" in command
    ):

        speak("Ji Sir, Chrome khol raha hoon.")

        subprocess.Popen(
            "start chrome",
            shell=True
        )

        return True

    # ==================================================
    # OPEN NOTEPAD
    # ==================================================

    if (
        "notepad kholo" in command
        or "notepad open" in command
    ):

        speak("Ji Sir, Notepad khol raha hoon.")

        subprocess.Popen(
            "notepad.exe"
        )

        return True

    # ==================================================
    # OPEN CALCULATOR
    # ==================================================

    if (
        "calculator kholo" in command
        or "calculator open" in command
        or "calc kholo" in command
    ):

        speak("Ji Sir, Calculator khol raha hoon.")

        subprocess.Popen(
            "calc.exe"
        )

        return True

    # ==================================================
    # OPEN FILE EXPLORER
    # ==================================================

    if (
        "file explorer kholo" in command
        or "explorer kholo" in command
    ):

        speak(
            "Ji Sir, File Explorer khol raha hoon."
        )

        subprocess.Popen(
            "explorer.exe"
        )

        return True

    # ==================================================
    # OPEN VS CODE
    # ==================================================

    if (
        "vs code kholo" in command
        or "visual studio code kholo" in command
    ):

        speak("Ji Sir, VS Code khol raha hoon.")

        subprocess.Popen(
            "code",
            shell=True
        )

        return True

    # ==================================================
    # YOUTUBE
    # ==================================================

    if "youtube kholo" in command:

        speak(
            "Ji Sir, YouTube khol raha hoon."
        )

        webbrowser.open(
            "https://www.youtube.com"
        )

        return True

    # ==================================================
    # GOOGLE
    # ==================================================

    if "google kholo" in command:

        speak(
            "Ji Sir, Google khol raha hoon."
        )

        webbrowser.open(
            "https://www.google.com"
        )

        return True

    # ==================================================
    # CHATGPT
    # ==================================================

    if "chatgpt kholo" in command:

        speak(
            "Ji Sir, ChatGPT khol raha hoon."
        )

        webbrowser.open(
            "https://chatgpt.com"
        )

        return True

    # ==================================================
    # DESKTOP
    # ==================================================

    if "desktop kholo" in command:

        desktop = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        speak(
            "Ji Sir, Desktop khol raha hoon."
        )

        os.startfile(desktop)

        return True

    # ==================================================
    # DOWNLOADS
    # ==================================================

    if "downloads kholo" in command:

        downloads = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        speak(
            "Ji Sir, Downloads folder khol raha hoon."
        )

        os.startfile(downloads)

        return True

    # ==================================================
    # DOCUMENTS
    # ==================================================

    if "documents kholo" in command:

        documents = os.path.join(
            os.path.expanduser("~"),
            "Documents"
        )

        speak(
            "Ji Sir, Documents folder khol raha hoon."
        )

        os.startfile(documents)

        return True

    # ==================================================
    # NOTHING MATCHED
    # ==================================================

    return None