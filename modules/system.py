import os
import socket
import datetime
import psutil
import platform
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

def handle_system(command, speak):

    # ------------------- Time -------------------

    if "time" in command or "waqt" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        reply = f"Waqt hua hai {current_time}"
        speak(reply)

        return reply
    # ------------------- Internet Check -------------------

    if "internet" in command or "internet status" in command or "net check" in command:

        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)

            reply = "Sir, internet connected hai."

        except OSError:

            reply = "Sir, internet disconnected hai."

        speak(reply)
        return reply

    # ------------------- System Status -------------------

    if "system status" in command:

        uname = platform.uname()

        ram = psutil.virtual_memory()

        disk = psutil.disk_usage("/")

        cpu = psutil.cpu_percent(interval=1)

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        reply = (
            f"Sir, PC Name: {uname.node}. "
            f"Windows: {uname.system}. "
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
            os.path.expanduser("~"),
            "Pictures",
            "Buddy_Screenshot.png"
        )

        screenshot.save(path)

        reply = f"Sir, screenshot save kar diya hai. {path}"

        speak(reply)
        return reply
    # ------------------- Mute -------------------

    if "mute" in command:

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)

        reply = "Sir, volume mute kar diya hai."
        speak(reply)
        return reply


    # ------------------- Unmute -------------------

    if "unmute" in command:

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)

        reply = "Sir, volume unmute kar diya hai."
        speak(reply)
        return reply
    # ------------------- Volume Up -------------------

    if "volume up" in command or "increase volume" in command:

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)

        reply = "Sir, volume barha diya hai."
        speak(reply)
        return reply


    # ------------------- Volume Down -------------------

    if "volume down" in command or "decrease volume" in command:

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)

        reply = "Sir, volume kam kar diya hai."
        speak(reply)
        return reply
    return None
    # ------------------- Battery -------------------

    if "battery" in command:

        battery = psutil.sensors_battery()

        if battery:
            reply = f"Sir, battery {battery.percent} percent hai."
        else:
            reply = "Sir, battery information available nahi hai."

        speak(reply)
        return reply
    # ------------------- RAM -------------------

    if "ram" in command:

        ram = psutil.virtual_memory()

        total = round(ram.total / (1024 ** 3), 2)
        used = round(ram.used / (1024 ** 3), 2)

        reply = (
            f"Sir, total RAM {total} GB hai. "
            f"Used RAM {used} GB hai. "
            f"RAM usage {ram.percent} percent hai."
        )

        speak(reply)
        return reply
    # ------------------- CPU -------------------

    if "cpu" in command:

        cpu = psutil.cpu_percent(interval=1)

        reply = f"Sir, CPU usage {cpu} percent hai."

        speak(reply)

        return reply
    # ------------------- Disk -------------------

    if (
        "disk" in command
        or "storage" in command
        or "space" in command
    ):

        disk = psutil.disk_usage("C:\\")

        total = round(disk.total / (1024 ** 3), 2)
        free = round(disk.free / (1024 ** 3), 2)

        reply = (
            f"Sir, C drive total {total} GB hai. "
            f"Free space {free} GB hai."
        )

        speak(reply)

        return reply
    # ------------------- PC Name -------------------

    if "pc name" in command or "computer name" in command:

        name = os.environ["COMPUTERNAME"]

        reply = f"Sir, aapke computer ka naam {name} hai."

        speak(reply)

        return reply


    # ------------------- Windows Version -------------------

    if (
        "windows version" in command
        or "pc version" in command
        or "system version" in command
    ):

        version = platform.platform()

        reply = f"Sir, aap {version} use kar rahe hain."

        speak(reply)

        return reply