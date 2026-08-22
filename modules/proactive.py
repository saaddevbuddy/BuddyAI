# ==========================================
# Buddy AI - Proactive Presence Engine 2.0
# Smart Busy-Aware Edition
# ==========================================

import random
import time
import threading


# ==========================================
# Settings
# ==========================================

MIN_INTERVAL = 45
MAX_INTERVAL = 90


# ==========================================
# Proactive Messages
# ==========================================

PROACTIVE_MESSAGES = [

    "Sir, main yahin hoon 😎 Jab koi kaam ho bata dein.",

    "Sir? 👀 Buddy standby par hai.",

    "Kaafi khamoshi hai Sir 😄 Sab theek chal raha hai?",

    "Sir, Buddy online hai 🤖",

    "Aaj ka mission kya hai Sir? 😎",

    "Sir, agar koi task ho to bata dein.",

    "Buddy standby duty par hai Sir 🫡",

    "Main yahin hoon Sir. Jab zarurat ho bula lena."

]


# ==========================================
# State
# ==========================================

_running = False

_last_activity_time = time.time()

_callback = None

_busy_checker = None

_thread = None


# ==========================================
# Register User Activity
# ==========================================

def register_activity():

    global _last_activity_time

    _last_activity_time = time.time()


# ==========================================
# Set Proactive Callback
# ==========================================

def set_proactive_callback(callback):

    global _callback

    _callback = callback


# ==========================================
# Set Busy Checker
# ==========================================

def set_busy_checker(callback):

    """
    GUI Buddy ki current processing state
    yahan provide karegi.

    Example:

        set_busy_checker(
            lambda: processing
        )
    """

    global _busy_checker

    _busy_checker = callback


# ==========================================
# Check Buddy Busy State
# ==========================================

def is_buddy_busy():

    if _busy_checker is None:
        return False

    try:

        return bool(
            _busy_checker()
        )

    except Exception as e:

        print(
            "Busy Checker Error:",
            repr(e)
        )

        return False


# ==========================================
# Send Proactive Message
# ==========================================

def send_proactive_message():

    if _callback is None:
        return

    # --------------------------------------
    # Buddy busy hai → message nahi
    # --------------------------------------

    if is_buddy_busy():
        return

    message = random.choice(
        PROACTIVE_MESSAGES
    )

    try:

        _callback(message)

    except Exception as e:

        print(
            "Proactive Callback Error:",
            repr(e)
        )


# ==========================================
# Background Loop
# ==========================================

def _proactive_loop():

    global _running

    while _running:

        wait_time = random.randint(
            MIN_INTERVAL,
            MAX_INTERVAL
        )

        time.sleep(
            wait_time
        )

        if not _running:
            break

        # ----------------------------------
        # Buddy currently processing
        # ----------------------------------

        if is_buddy_busy():

            continue

        # ----------------------------------
        # User activity check
        # ----------------------------------

        inactive_time = (
            time.time()
            -
            _last_activity_time
        )

        if inactive_time < MIN_INTERVAL:

            continue

        # ----------------------------------
        # Final busy check
        # ----------------------------------

        if is_buddy_busy():

            continue

        send_proactive_message()


# ==========================================
# Start
# ==========================================

def start_proactive():

    global _running
    global _thread

    if _running:
        return

    _running = True

    _thread = threading.Thread(
        target=_proactive_loop,
        daemon=True
    )

    _thread.start()

    print(
        "Buddy Proactive Presence Started"
    )


# ==========================================
# Stop
# ==========================================

def stop_proactive():

    global _running

    _running = False

    print(
        "Buddy Proactive Presence Stopped"
    )


# ==========================================
# Status
# ==========================================

def is_proactive_running():

    return _running