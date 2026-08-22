# ==========================================
# Buddy AI - Background Wake Listener
# ==========================================

import threading
import time

from voice import listen, speak
from modules.wake import check_wake_word, get_wake_response
from commands import handle_command


running = False


# ==========================================
# Start Wake Listener
# ==========================================

def start_wake_listener():

    global running

    if running:
        return

    running = True

    thread = threading.Thread(
        target=_wake_loop,
        daemon=True
    )

    thread.start()

    print("🎙️ Buddy Wake Listener Started")


# ==========================================
# Stop Wake Listener
# ==========================================

def stop_wake_listener():

    global running

    running = False

    print("🎙️ Buddy Wake Listener Stopped")


# ==========================================
# Wake Loop
# ==========================================

def _wake_loop():

    global running

    while running:

        try:

            # -------------------------------
            # Wait for wake word
            # -------------------------------

            text = listen()

            if not text:
                continue


            # -------------------------------
            # Check wake word
            # -------------------------------

            if not check_wake_word(text):
                continue


            # -------------------------------
            # Buddy response
            # -------------------------------

            reply = get_wake_response()

            speak(reply)


            # -------------------------------
            # Listen for command
            # -------------------------------

            print("🎙️ Buddy: Command ka wait kar raha hoon...")

            command = listen()

            if not command:
                continue


            # -------------------------------
            # Execute command
            # -------------------------------

            try:

                response = handle_command(
                    command,
                    speak
                )

                # IMPORTANT:
                # handle_command ke modules khud
                # speak() kar sakte hain.
                #
                # Isliye yahan response ko dobara
                # speak nahi karna.

                if response:
                    pass


            except Exception as command_error:

                print(
                    "Command Error:",
                    command_error
                )

                speak(
                    "Sir, command process karte waqt "
                    "ek masla aa gaya."
                )


        except Exception as e:

            print(
                "Wake Listener Error:",
                e
            )

            time.sleep(2)