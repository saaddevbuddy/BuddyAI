# ==========================================
# Buddy AI - Living Presence Engine 1.0
# ==========================================

import time
import threading
from datetime import datetime


# ==========================================
# Configuration
# ==========================================

STARTUP_DELAY = 3

MIN_INACTIVE_TIME = 60

CHECK_INTERVAL = 10


# ==========================================
# State
# ==========================================

_running = False

_started = False

_last_activity = time.time()

_callback = None


# ==========================================
# Presence State
# ==========================================

_presence_state = {
    "online": False,
    "user_active": True,
    "inactive_seconds": 0,
    "last_activity": None,
    "started_at": None
}


# ==========================================
# Set Callback
# ==========================================

def set_presence_callback(callback):

    global _callback

    _callback = callback


# ==========================================
# Safe Callback
# ==========================================

def _send(message):

    if _callback is None:
        return

    try:

        _callback(message)

    except Exception as e:

        print(
            "Presence Callback Error:",
            repr(e)
        )


# ==========================================
# Register User Activity
# ==========================================

def register_activity():

    global _last_activity

    _last_activity = time.time()

    _presence_state["user_active"] = True

    _presence_state["inactive_seconds"] = 0

    _presence_state["last_activity"] = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )


# ==========================================
# Get Presence State
# ==========================================

def get_presence_state():

    inactive = (
        time.time()
        -
        _last_activity
    )

    _presence_state["inactive_seconds"] = int(
        inactive
    )

    _presence_state["user_active"] = (
        inactive < MIN_INACTIVE_TIME
    )

    return _presence_state.copy()


# ==========================================
# Startup Greeting
# ==========================================

def startup_greeting():

    messages = [

        "Assalam-o-Alaikum Sir ❤️ Buddy online hai.",

        "Assalam-o-Alaikum Sir 😎 Buddy ready hai.",

        "Welcome back Sir 🤖 Aaj ka mission kya hai?",

        "Sir, Buddy online hai. Chaliye aaj kuch zabardast banate hain."
    ]

    import random

    _send(
        random.choice(messages)
    )


# ==========================================
# Inactivity Check
# ==========================================

def _check_inactivity():

    state = get_presence_state()

    inactive = state["inactive_seconds"]

    if inactive < MIN_INACTIVE_TIME:

        return

    # --------------------------------------
    # Sirf ek baar trigger
    # --------------------------------------

    global _started

    if _started:

        return

    _started = True

    messages = [

        "Sir? Kaafi der se khamoshi hai 😄",

        "Sir, Buddy yahin hai. Sab theek chal raha hai?",

        "Hmm... Sir kaafi der se chup hain 👀",

        "Sir, agar kisi cheez mein help chahiye ho to Buddy ready hai."
    ]

    import random

    _send(
        random.choice(messages)
    )


# ==========================================
# Background Loop
# ==========================================

def _presence_loop():

    global _running

    while _running:

        try:

            _check_inactivity()

        except Exception as e:

            print(
                "Presence Loop Error:",
                repr(e)
            )

        time.sleep(
            CHECK_INTERVAL
        )


# ==========================================
# Start Presence
# ==========================================

def start_presence():

    global _running
    global _started

    if _running:

        return

    _running = True

    _started = False

    _presence_state["online"] = True

    _presence_state["started_at"] = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    register_activity()

    # --------------------------------------
    # Startup greeting
    # --------------------------------------

    def delayed_greeting():

        time.sleep(
            STARTUP_DELAY
        )

        if _running:

            startup_greeting()

    threading.Thread(
        target=delayed_greeting,
        daemon=True
    ).start()

    # --------------------------------------
    # Presence monitor
    # --------------------------------------

    threading.Thread(
        target=_presence_loop,
        daemon=True
    ).start()

    print(
        "Buddy Living Presence Started"
    )


# ==========================================
# Stop Presence
# ==========================================

def stop_presence():

    global _running

    _running = False

    _presence_state["online"] = False

    print(
        "Buddy Living Presence Stopped"
    )


# ==========================================
# Status
# ==========================================

def is_presence_running():

    return _running


# ==========================================
# User Active?
# ==========================================

def is_user_active():

    state = get_presence_state()

    return state["user_active"]


# ==========================================
# Inactive Seconds
# ==========================================

def get_inactive_seconds():

    return int(
        time.time()
        -
        _last_activity
    )