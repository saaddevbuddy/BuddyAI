from commands import handle_command
from modules.brain import handle_brain
from modules.ai import ask_ai, extract_memory
from modules.intent import detect_intent
from modules.profile import handle_profile
from modules.reminder import handle_reminder
from modules.thinking import think
from plugins.system import handle_system
from modules.notes import handle_notes
from modules.mood import analyze_mood
from modules.history import add_history
from modules.memory import save_extracted_memory
from modules.weather import ask_weather
from modules.buddy_mood_triggers import detect_buddy_mood_trigger

import threading


# ==========================================================
# Buddy AI - Smart Router 3.0
# GUI + Voice + Commands + AI + Memory
# ==========================================================


def route(user_input, speak=None):

    # ======================================================
    # 1. BASIC CLEANUP
    # ======================================================

    if user_input is None:
        return None

    user_input = str(user_input).strip()

    if not user_input:
        return None

    # ======================================================
    # 2. REPLY CAPTURE SYSTEM
    #
    # Kisi module ne agar:
    #
    # speak("Hello Sir")
    #
    # kiya aur return None kiya,
    # to Buddy ka reply phir bhi GUI tak pohanch sake.
    # ======================================================

    captured_reply = {
        "text": None
    }

    def speak_proxy(text):

        if text is None:
            return

        text = str(text).strip()

        if not text:
            return

        captured_reply["text"] = text

        print(
            "Buddy Spoken Reply:",
            repr(text)
        )

        # ----------------------------------------------
        # Actual voice background mein
        # ----------------------------------------------

        if speak:

            try:

                threading.Thread(
                    target=speak,
                    args=(text,),
                    daemon=True
                ).start()

            except Exception as e:

                print(
                    "Speech Error:",
                    repr(e)
                )

    # ======================================================
    # 3. BUDDY INTERNAL MOOD
    # ======================================================

    try:

        buddy_trigger = detect_buddy_mood_trigger(
            user_input
        )

        if buddy_trigger:

            print(
                f"Buddy Mood Trigger: {buddy_trigger}"
            )

    except Exception as e:

        print(
            "Buddy Mood Trigger Error:",
            repr(e)
        )

    # ======================================================
    # 4. INTENT
    # ======================================================

    try:

        intent = detect_intent(
            user_input
        )

    except Exception as e:

        print(
            "Intent Error:",
            repr(e)
        )

        intent = None

    print(
        f"\nDetected Intent: {intent}"
    )

    # ======================================================
    # 5. MOOD
    # ======================================================

    try:

        mood_data = analyze_mood(
            user_input
        )

        mood_name = mood_data.get(
            "name",
            "Normal"
        )

        mood_emoji = mood_data.get(
            "emoji",
            "🙂"
        )

        mood_confidence = mood_data.get(
            "confidence",
            0
        )

        mood_style = mood_data.get(
            "style",
            ""
        )

        matched_words = mood_data.get(
            "matched_words",
            []
        )

    except Exception as e:

        print(
            "Mood Error:",
            repr(e)
        )

        mood_name = "Normal"
        mood_emoji = "🙂"
        mood_confidence = 0
        mood_style = ""
        matched_words = []

    print(
        f"Detected Mood: "
        f"{mood_emoji} {mood_name} "
        f"({mood_confidence}%)"
    )

    if matched_words:

        print(
            f"Matched Mood Words: "
            f"{matched_words}"
        )

    # ======================================================
    # 6. WEATHER
    # ======================================================

    weather_text = user_input.lower()

    weather_words = [
        "weather",
        "mausam",
        "mosam",
        "temperature",
        "temp",
        "barish",
        "baarish"
    ]

    weather_request = any(
        word in weather_text
        for word in weather_words
    )

    if weather_request:

        city = None

        known_cities = [
            "mianwali",
            "lahore",
            "rawalpindi",
            "islamabad",
            "karachi",
            "multan",
            "peshawar",
            "quetta",
            "faisalabad",
            "sargodha",
            "murree"
        ]

        for known_city in known_cities:

            if known_city in weather_text:

                city = known_city.title()
                break

        if city is None:

            city = "Mianwali"

        print(
            f"Weather Request: {city}"
        )

        try:

            reply = ask_weather(
                city
            )

            if reply:

                reply = str(
                    reply
                ).strip()

                speak_proxy(
                    reply
                )

                print(
                    "Weather Reply:",
                    repr(reply)
                )

                return reply

        except Exception as e:

            print(
                "Weather Router Error:",
                repr(e)
            )

            reply = (
                "Sir, weather information "
                "abhi nahi mil saki."
            )

            speak_proxy(
                reply
            )

            return reply

    # ======================================================
    # 7. COMMANDS
    # ======================================================

    try:

        captured_reply["text"] = None

        command_result = handle_command(
            user_input,
            speak_proxy
        )

        # Module ne direct reply return kiya
        if command_result:

            reply = str(
                command_result
            ).strip()

            speak_proxy(
                reply
            )

            print(
                "Command Reply:",
                repr(reply)
            )

            return reply

        # Module ne sirf speak() kiya
        if captured_reply["text"]:

            reply = captured_reply["text"]

            print(
                "Captured Command Reply:",
                repr(reply)
            )

            return reply

    except Exception as e:

        print(
            "Command Router Error:",
            repr(e)
        )

    # ======================================================
    # 8. SYSTEM
    # ======================================================

    try:

        captured_reply["text"] = None

        system_result = handle_system(
            user_input,
            speak_proxy
        )

        if system_result:

            reply = str(
                system_result
            ).strip()

            speak_proxy(
                reply
            )

            print(
                "System Reply:",
                repr(reply)
            )

            return reply

        if captured_reply["text"]:

            reply = captured_reply["text"]

            print(
                "Captured System Reply:",
                repr(reply)
            )

            return reply

    except Exception as e:

        print(
            "System Router Error:",
            repr(e)
        )

    # ======================================================
    # 9. PROFILE
    # ======================================================

    try:

        captured_reply["text"] = None

        profile_reply = handle_profile(
            user_input,
            speak_proxy
        )

        if profile_reply:

            reply = str(
                profile_reply
            ).strip()

            speak_proxy(
                reply
            )

            print(
                "Profile Reply:",
                repr(reply)
            )

            return reply

        if captured_reply["text"]:

            return captured_reply["text"]

    except Exception as e:

        print(
            "Profile Router Error:",
            repr(e)
        )

    # ======================================================
    # 10. REMINDER
    # ======================================================

    try:

        captured_reply["text"] = None

        reminder_reply = handle_reminder(
            user_input,
            speak_proxy
        )

        if reminder_reply:

            reply = str(
                reminder_reply
            ).strip()

            speak_proxy(
                reply
            )

            print(
                "Reminder Reply:",
                repr(reply)
            )

            return reply

        if captured_reply["text"]:

            return captured_reply["text"]

    except Exception as e:

        print(
            "Reminder Router Error:",
            repr(e)
        )

    # ======================================================
    # 11. NOTES
    # ======================================================

    try:

        captured_reply["text"] = None

        notes_reply = handle_notes(
            user_input,
            speak_proxy
        )

        if notes_reply:

            reply = str(
                notes_reply
            ).strip()

            speak_proxy(
                reply
            )

            print(
                "Notes Reply:",
                repr(reply)
            )

            return reply

        if captured_reply["text"]:

            return captured_reply["text"]

    except Exception as e:

        print(
            "Notes Router Error:",
            repr(e)
        )

    # ======================================================
    # 12. BRAIN
    # ======================================================

    try:

        brain_reply = handle_brain(
            user_input
        )

        if brain_reply:

            reply = str(
                brain_reply
            ).strip()

            speak_proxy(
                reply
            )

            print(
                "Brain Reply:",
                repr(reply)
            )

            return reply

    except Exception as e:

        print(
            "Brain Router Error:",
            repr(e)
        )

    # ======================================================
    # 13. THINKING
    # ======================================================

    try:

        think()

    except Exception as e:

        print(
            "Thinking Error:",
            repr(e)
        )

    # ======================================================
    # 14. AI FALLBACK
    # ======================================================

    memory_context = f"""
Current Mood:
{mood_name}

Mood Confidence:
{mood_confidence}%

Mood Style:
{mood_style}

Matched Mood Words:
{matched_words}
"""

    try:

        reply = ask_ai(
            user_input,
            memory_context
        )

    except Exception as e:

        print(
            "AI Router Error:",
            repr(e)
        )

        reply = None

    # ======================================================
    # 15. GUARANTEED AI FALLBACK
    # ======================================================

    if reply:

        reply = str(
            reply
        ).strip()

    if not reply:

        reply = (
            "Sir, main yahan hoon 😎 "
            "Lekin AI service ne is waqt jawab nahi diya."
        )

    # ======================================================
    # 16. PERSISTENT MEMORY
    #
    # Har message par Gemini call nahi.
    # Sirf likely personal information.
    # ======================================================

    memory_words = [
        "mera naam",
        "my name",
        "meri age",
        "meri umar",
        "mujhe pasand",
        "mujhe acha lagta",
        "mujhe achha lagta",
        "mera favourite",
        "meri favourite",
        "mera favorite",
        "meri favorite",
        "mera shehar",
        "main rehta",
        "main rehti",
        "mera goal",
        "mera dream",
        "mera phone",
        "meri hobby",
        "mera favourite game",
        "mera favorite game"
    ]

    should_extract_memory = any(
        word in user_input.lower()
        for word in memory_words
    )

    if should_extract_memory:

        try:

            extracted_memory = extract_memory(
                user_input
            )

            if extracted_memory:

                saved = save_extracted_memory(
                    extracted_memory
                )

                if saved:

                    print(
                        "Memory Saved:",
                        extracted_memory
                    )

        except Exception as e:

            # Memory fail hone se Buddy ka main reply
            # kabhi block nahi hoga.

            print(
                "Memory Save Skipped:",
                repr(e)
            )

    # ======================================================
    # 17. CONVERSATION HISTORY
    # ======================================================

    try:

        add_history(
            user_input,
            reply
        )

    except Exception as e:

        print(
            "History Error:",
            repr(e)
        )

    # ======================================================
    # 18. FINAL REPLY
    # ======================================================

    print(
        "Buddy Final Reply:",
        repr(reply)
    )

    # ======================================================
    # IMPORTANT
    #
    # Voice sirf yahan se.
    # AI/Memory ke baad duplicate speak nahi.
    # ======================================================

    speak_proxy(
        reply
    )

    # ======================================================
    # GUI KO REPLY RETURN
    # ======================================================

    return reply


# ==========================================================
# Router Ready
# ==========================================================

print(
    "Buddy AI Router 3.0 Loaded"
)