# ==========================================================
# Buddy AI - Smart Router 3.5
# Memory + Commands + Weather + Web Search + AI + Voice
# Gemini -> APInex -> OpenCode Zen
# ==========================================================

import threading

from commands import handle_command

from modules.brain import handle_brain
from modules.ai import extract_memory
from modules.ai_manager import get_ai_response
from modules.intent import detect_intent
from modules.profile import handle_profile
from modules.reminder import handle_reminder
from modules.thinking import think
from modules.notes import handle_notes
from modules.mood import analyze_mood
from modules.history import add_history

from modules.memory import (
    get_memory,
    search_memory,
    get_all_memory,
    save_extracted_memory
)

from modules.weather import ask_weather
from modules.buddy_mood_triggers import detect_buddy_mood_trigger
from modules.diagnostics import diagnose
from plugins.system import handle_system

try:
    from modules.web_search import (
        web_search,
        format_search_results
    )
    WEB_SEARCH_AVAILABLE = True
except Exception as e:
    print(
        "[Web Search] Module unavailable:",
        repr(e)
    )
    WEB_SEARCH_AVAILABLE = False


# ==========================================================
# MEMORY QUESTION DETECTOR
# ==========================================================

def is_memory_question(text):

    text = text.lower().strip()

    memory_words = [
        "favorite game",
        "favourite game",
        "favorite food",
        "favourite food",
        "favorite phone",
        "favourite phone",
        "favorite car",
        "favourite car",
        "favorite youtuber",
        "favourite youtuber",
        "favorite ai",
        "favourite ai",
        "hobby",
        "dream",
        "goal",
        "mera game kya",
        "meri game kya",
        "mera favorite",
        "mera favourite",
        "meri favorite",
        "meri favourite",
        "mujhe kya pasand",
        "mujhe kya acha lagta",
        "mujhe kya achha lagta",
        "mera phone kya",
        "meri hobby kya",
        "mera dream kya",
        "mera goal kya",
        "mera youtuber kaun",
        "mera favorite youtuber kaun",
        "mera favourite youtuber kaun"
    ]

    return any(
        word in text
        for word in memory_words
    )


# ==========================================================
# FORMAT MEMORY REPLY
# ==========================================================

def format_memory_reply(results):

    if not results:
        return None

    if "favorite_game" in results:
        return (
            f"Sir, aapka favorite game "
            f"{results['favorite_game']} hai. 🎮"
        )

    if "favorite_food" in results:
        return (
            f"Sir, aapka favorite food "
            f"{results['favorite_food']} hai. 🍛"
        )

    if "favorite_phone" in results:
        return (
            f"Sir, aapka favorite phone "
            f"{results['favorite_phone']} hai. 📱"
        )

    if "favorite_car" in results:
        return (
            f"Sir, aapki favorite car "
            f"{results['favorite_car']} hai. 🚙"
        )

    if "favorite_ai" in results:
        return (
            f"Sir, aapka favorite AI "
            f"{results['favorite_ai']} hai. 🤖"
        )

    if "favorite_youtuber" in results:
        return (
            f"Sir, aapke favorite YouTuber "
            f"{results['favorite_youtuber']} hain. ▶️"
        )

    if "hobby" in results:
        return (
            f"Sir, aapka hobby "
            f"{results['hobby']} hai. 😎"
        )

    if "dream" in results:
        return (
            f"Sir, aapka dream "
            f"{results['dream']} hai. ✨"
        )

    if "goal" in results:
        return (
            f"Sir, aapka goal "
            f"{results['goal']} hai. 🎯"
        )

    return None


# ==========================================================
# MEMORY CONTEXT BUILDER
# ==========================================================

def build_memory_context():

    try:

        memory = get_all_memory()

        if not memory:
            return ""

        lines = []

        for key, value in memory.items():

            if value is None:
                continue

            if isinstance(value, (dict, list)):
                continue

            lines.append(
                f"{key}: {value}"
            )

        if not lines:
            return ""

        return "\n".join(lines)

    except Exception as e:

        print(
            "Memory Context Error:",
            repr(e)
        )

        return ""


# ==========================================================
# AI ERROR CHECK
# ==========================================================

def is_ai_error_message(text):

    if not text:
        return False

    text = str(text).lower().strip()

    error_phrases = [
        "gemini api key ya authentication mein masla",
        "gemini se response lene mein filhaal masla",
        "gemini ki free-tier limit",
        "gemini abhi bohat busy hai",
        "ai brain mein filhaal masla",
        "ai service unavailable",
        "authentication error",
        "authentication mein masla",
        "temporarily unavailable",
        "service unavailable",
        "rate limit",
        "too many requests",
        "internal server error"
    ]

    return any(
        phrase in text
        for phrase in error_phrases
    )


# ==========================================================
# WEB SEARCH DETECTOR
# ==========================================================

def is_web_search_request(text):

    text = text.lower().strip()

    search_phrases = [

        # English
        "search",
        "search it",
        "search this",
        "search online",
        "search the web",
        "google it",
        "google this",
        "look it up",
        "look up",
        "find online",
        "find on internet",
        "check online",
        "check internet",
        "latest",
        "latest news",
        "breaking news",
        "today's news",
        "todays news",
        "current news",
        "current information",
        "recent news",
        "recent information",
        "what happened today",
        "what is happening",

        # Roman Urdu
        "internet se",
        "net se",
        "online se",
        "google par",
        "google pe",
        "web par",
        "web pe",
        "internet par",
        "internet pe",
        "net par",
        "net pe",
        "taza khabar",
        "taza khabrein",
        "aaj ki khabar",
        "aaj ki khabrein",
        "aaj ki news",
        "latest khabar",
        "latest khabrein",
        "haal ki khabar",
        "abhi ki khabar",
        "abhi kya hua",
        "aaj kya hua",
        "aaj kya ho raha",
        "latest kya hai",
        "latest kya chal raha",
        "nayi khabar",
        "nai khabar",
        "maloom karo",
        "pata karo",
        "dekh kar batao",
        "check karke batao",
        "search karke batao"
    ]

    return any(
        phrase in text
        for phrase in search_phrases
    )


# ==========================================================
# CLEAN WEB QUERY
# ==========================================================

def build_web_query(user_input):

    query = str(
        user_input
    ).strip()

    remove_phrases = [

        "buddy",
        "please",
        "sir",
        "search it",
        "search this",
        "search online",
        "search the web",
        "google it",
        "google this",
        "look it up",
        "look up",
        "find online",
        "find on internet",
        "check online",
        "check internet",
        "internet se",
        "net se",
        "online se",
        "google par",
        "google pe",
        "web par",
        "web pe",
        "internet par",
        "internet pe",
        "net par",
        "net pe",
        "search karke batao",
        "check karke batao",
        "dekh kar batao",
        "maloom karo",
        "pata karo"
    ]

    for phrase in remove_phrases:

        query = query.replace(
            phrase,
            " "
        )

    query = " ".join(
        query.split()
    ).strip()

    if not query:
        query = user_input

    return query


# ==========================================================
# BUILD WEB-AWARE AI PROMPT
# ==========================================================

def build_web_ai_prompt(
    user_input,
    search_results,
    memory_context
):

    formatted = format_search_results(
        search_results
    )

    return f"""
You are Buddy, a friendly personal AI companion.

User message:
{user_input}

Fresh internet search results:
{formatted}

Buddy Memory:
{memory_context}

Instructions:

1. Answer the user's actual question.
2. Use the fresh search results when relevant.
3. Do not invent facts that are not supported by the results.
4. If the search results are unclear or insufficient, say so naturally.
5. Answer in natural Roman Urdu.
6. English technical names, proper names and terms can remain in English.
7. Do not mention internal AI providers.
8. Do not say you are GPT or another model.
9. Address the user as Sir naturally.
10. Keep the answer conversational and useful.
"""


# ==========================================================
# MAIN ROUTER
# ==========================================================

def route(user_input, speak=None):

    if user_input is None:
        return None

    user_input = str(
        user_input
    ).strip()

    if not user_input:
        return None

    print(
        "\n========== GUI ROUTER =========="
    )

    print(
        "User:",
        user_input
    )

    # ======================================================
    # REPLY CAPTURE
    # ======================================================

    captured_reply = {
        "text": None
    }

    def speak_proxy(text):

        if text is None:
            return

        text = str(
            text
        ).strip()

        if not text:
            return

        captured_reply["text"] = text

        print(
            "Buddy Spoken Reply:",
            repr(text)
        )

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
    # BUDDY MOOD TRIGGER
    # ======================================================

    try:

        buddy_trigger = detect_buddy_mood_trigger(
            user_input
        )

        if buddy_trigger:

            print(
                "Buddy Mood Trigger:",
                buddy_trigger
            )

    except Exception as e:

        print(
            "Buddy Mood Trigger Error:",
            repr(e)
        )

    # ======================================================
    # INTENT
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
        "Detected Intent:",
        intent
    )

    # ======================================================
    # MOOD
    # ======================================================

    try:

        mood_data = analyze_mood(
            user_input
        )

        if not isinstance(
            mood_data,
            dict
        ):
            mood_data = {}

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

    # ======================================================
    # MEMORY QUESTION
    # ======================================================

    if is_memory_question(
        user_input
    ):

        try:

            print(
                "[Memory] Searching Buddy memory..."
            )

            memory_results = search_memory(
                user_input
            )

            print(
                "[Memory] Results:",
                memory_results
            )

            memory_reply = format_memory_reply(
                memory_results
            )

            if memory_reply:

                print(
                    "[Memory] Direct memory answer:",
                    repr(memory_reply)
                )

                speak_proxy(
                    memory_reply
                )

                try:

                    add_history(
                        user_input,
                        memory_reply
                    )

                except Exception as e:

                    print(
                        "History Error:",
                        repr(e)
                    )

                print(
                    "GUI ROUTER RETURN:",
                    repr(memory_reply)
                )

                return memory_reply

            print(
                "[Memory] No matching memory found."
            )

        except Exception as e:

            print(
                "[Memory] Search Error:",
                repr(e)
            )

    # ======================================================
    # DIAGNOSTICS
    # ======================================================

    diagnostic_words = [

        "system check",
        "system check karo",
        "apna system check karo",
        "buddy check",
        "buddy diagnostic",
        "diagnostic",
        "diagnostics",
        "buddy health check",
        "health check"
    ]

    if any(
        word in user_input.lower()
        for word in diagnostic_words
    ):

        try:

            print(
                "[Diagnostics] Running Buddy system check..."
            )

            diagnostic_reply = diagnose()

            if diagnostic_reply:

                diagnostic_reply = str(
                    diagnostic_reply
                ).strip()

                speak_proxy(
                    diagnostic_reply
                )

                print(
                    "Diagnostic Reply:",
                    repr(diagnostic_reply)
                )

                return diagnostic_reply

        except Exception as e:

            print(
                "Diagnostics Error:",
                repr(e)
            )

            diagnostic_reply = (
                "Sir, system diagnostic chalane mein "
                "problem aa gayi."
            )

            speak_proxy(
                diagnostic_reply
            )

            return diagnostic_reply

    # ======================================================
    # WEATHER
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
    # WEB SEARCH
    # ======================================================

    if is_web_search_request(
        user_input
    ):

        print(
            "\n[Web Search] Internet request detected."
        )

        if not WEB_SEARCH_AVAILABLE:

            print(
                "[Web Search] Module unavailable."
            )

            reply = (
                "Sir, meri web search service "
                "abhi available nahi hai."
            )

            speak_proxy(
                reply
            )

            return reply

        try:

            web_query = build_web_query(
                user_input
            )

            print(
                "[Web Search] Query:",
                web_query
            )

            search_results = web_search(
                web_query,
                max_results=5
            )

            if search_results:

                print(
                    "[Web Search] Search successful."
                )

                full_memory = build_memory_context()

                web_prompt = build_web_ai_prompt(
                    user_input,
                    search_results,
                    full_memory
                )

                print(
                    "[Web Search] Sending results to AI..."
                )

                reply = get_ai_response(
                    web_prompt,
                    ""
                )

                if reply:

                    reply = str(
                        reply
                    ).strip()

                if reply:

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

                    speak_proxy(
                        reply
                    )

                    print(
                        "Web AI Reply:",
                        repr(reply)
                    )

                    print(
                        "GUI ROUTER RETURN:",
                        repr(reply)
                    )

                    return reply

                print(
                    "[Web Search] AI could not summarize results."
                )

            else:

                print(
                    "[Web Search] No results."
                )

                reply = (
                    "Sir, mujhe is waqt internet par "
                    "relevant information nahi mili."
                )

                speak_proxy(
                    reply
                )

                return reply

        except Exception as e:

            print(
                "[Web Search] Router Error:",
                repr(e)
            )

            reply = (
                "Sir, internet se information "
                "lene mein filhaal problem aa gayi."
            )

            speak_proxy(
                reply
            )

            return reply

    # ======================================================
    # COMMANDS
    # ======================================================

    try:

        captured_reply["text"] = None

        command_result = handle_command(
            user_input,
            speak_proxy
        )

        if command_result:

            reply = str(
                command_result
            ).strip()

            if is_ai_error_message(
                reply
            ):

                print(
                    "Command returned AI error."
                )

                captured_reply["text"] = None

            else:

                if captured_reply["text"] != reply:

                    speak_proxy(
                        reply
                    )

                print(
                    "Command Reply:",
                    repr(reply)
                )

                return reply

        if captured_reply["text"]:

            reply = captured_reply["text"]

            if not is_ai_error_message(
                reply
            ):

                print(
                    "Module Captured Reply:",
                    repr(reply)
                )

                return reply

            captured_reply["text"] = None

    except Exception as e:

        print(
            "Command Router Error:",
            repr(e)
        )

    # ======================================================
    # SYSTEM
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

            if captured_reply["text"] != reply:

                speak_proxy(
                    reply
                )

            print(
                "System Reply:",
                repr(reply)
            )

            return reply

        if captured_reply["text"]:

            return captured_reply["text"]

    except Exception as e:

        print(
            "System Router Error:",
            repr(e)
        )

    # ======================================================
    # PROFILE
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

            if captured_reply["text"] != reply:

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
    # REMINDER
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

            if captured_reply["text"] != reply:

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
    # NOTES
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

            if captured_reply["text"] != reply:

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
    # BRAIN
    # ======================================================

    try:

        brain_reply = handle_brain(
            user_input
        )

        if brain_reply:

            reply = str(
                brain_reply
            ).strip()

            if not is_ai_error_message(
                reply
            ):

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
    # THINKING
    # ======================================================

    try:

        think()

    except Exception as e:

        print(
            "Thinking Error:",
            repr(e)
        )

    # ======================================================
    # MEMORY CONTEXT
    # ======================================================

    full_memory = build_memory_context()

    memory_context = f"""
Buddy Memory:

{full_memory}

Current Mood:
{mood_name}

Mood Confidence:
{mood_confidence}%

Mood Style:
{mood_style}

Matched Mood Words:
{matched_words}

Important:
Agar user apni saved information ke bare mein pooche
to Buddy Memory ko use karo.
"""

    # ======================================================
    # AI MANAGER
    # ======================================================

    try:

        print(
            "\n=========================================="
        )

        print(
            "Buddy AI Manager Started"
        )

        print(
            "Primary: Gemini"
        )

        print(
            "Fallback Chain: APInex -> OpenCode Zen"
        )

        print(
            "Memory Context: ENABLED"
        )

        print(
            "=========================================="
        )

        reply = get_ai_response(
            user_input,
            memory_context
        )

    except Exception as e:

        print(
            "AI Manager Router Error:",
            repr(e)
        )

        reply = None

    # ======================================================
    # FINAL AI FALLBACK
    # ======================================================

    if reply:

        reply = str(
            reply
        ).strip()

    if not reply:

        reply = (
            "Sir, is waqt meri AI services se "
            "response nahi aa raha."
        )

    # ======================================================
    # SAVE PERSONAL MEMORY
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

            print(
                "Memory Save Skipped:",
                repr(e)
            )

    # ======================================================
    # HISTORY
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
    # FINAL VOICE
    # ======================================================

    speak_proxy(
        reply
    )

    # ======================================================
    # FINAL GUI REPLY
    # ======================================================

    print(
        "Buddy Final Reply:",
        repr(reply)
    )

    print(
        "GUI ROUTER RETURN:",
        repr(reply)
    )

    return reply


# ==========================================================
# ROUTER READY
# ==========================================================

print(
    "Buddy AI Router 3.5 Loaded"
)

print(
    "AI Chain: Memory -> Web Search -> Gemini -> APInex -> OpenCode Zen"
)

print(
    "Persistent Memory: ENABLED"
)

print(
    "Web Search:",
    "ENABLED" if WEB_SEARCH_AVAILABLE else "DISABLED"
)