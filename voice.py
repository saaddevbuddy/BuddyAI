# ==========================================================
# Buddy AI - Stable Natural Voice System
# Roman Urdu + English
# Full Text Speech
# Single TTS Request
# Clean Audio Playback
# Voice Sync Friendly
# ==========================================================

import asyncio
import edge_tts
import pygame
import speech_recognition as sr
import tempfile
import os
import threading
import re


# ==========================================================
# VOICE SETTINGS
# ==========================================================

# Andrew is currently the most reliable voice for complete
# Roman Urdu text without randomly dropping words.

ROMAN_URDU_VOICE = "en-US-AndrewNeural"
ENGLISH_VOICE = "en-US-AndrewNeural"


# ==========================================================
# AUDIO SETTINGS
# ==========================================================

_audio_lock = threading.Lock()

pygame.mixer.init()


# ==========================================================
# TEXT CLEANING
# ==========================================================

def clean_for_voice(text):
    """
    Sirf unnecessary symbols/formatting clean karta hai.
    Text ka actual content change nahi karta.
    """

    if text is None:
        return ""

    text = str(text).strip()

    if not text:
        return ""

    # Remove markdown formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # Remove code formatting
    text = text.replace("```", "")
    text = text.replace("`", "")

    # Remove unnecessary decorative symbols
    text = re.sub(r"[#~]+", " ", text)

    # Keep normal punctuation
    text = re.sub(r"[ \t]+", " ", text)

    # Too many dots -> normal pause
    text = re.sub(r"\.{4,}", "...", text)

    # Too many exclamation marks
    text = re.sub(r"!{3,}", "!!", text)

    # Too many question marks
    text = re.sub(r"\?{3,}", "??", text)

    return text.strip()


# ==========================================================
# VOICE TEXT PREPARATION
# ==========================================================

def prepare_voice_text(text):
    """
    Voice ke liye final text.
    Important:
    Original Roman Urdu ko convert nahi karta.
    """

    text = clean_for_voice(text)

    if not text:
        return ""

    return text


# ==========================================================
# ROMAN URDU DETECTION
# ==========================================================

def is_roman_urdu(text):
    """
    Simple detection.
    Roman Urdu ko English se alag karne ke liye common words.
    """

    if not text:
        return False

    text_lower = text.lower()

    roman_urdu_words = [
        "aap",
        "aapka",
        "aapki",
        "aapko",
        "mera",
        "meri",
        "mere",
        "mujhe",
        "mujh",
        "tum",
        "tumhara",
        "tumhari",
        "ham",
        "hum",
        "humein",
        "hai",
        "hain",
        "ho",
        "tha",
        "thi",
        "the",
        "kar",
        "karo",
        "kya",
        "kyun",
        "kaise",
        "kaisa",
        "acha",
        "achha",
        "abhi",
        "aaj",
        "kal",
        "sir",
        "bhai",
        "chahiye",
        "raha",
        "rahi",
        "rhe",
        "batao",
        "bata",
        "sakta",
        "sakti",
        "hoga",
        "hogi",
        "nahi",
        "nahin",
        "bohat",
        "zyada",
        "kam",
        "wala",
        "wali",
        "liye",
        "liye",
        "se",
        "ko",
        "mein",
        "me",
    ]

    words = re.findall(r"[a-zA-Z']+", text_lower)

    if not words:
        return False

    matches = sum(1 for word in words if word in roman_urdu_words)

    return matches >= 1


# ==========================================================
# VOICE SELECTION
# ==========================================================

def choose_voice(text):
    """
    Currently Andrew is used for both Roman Urdu and English.

    Reason:
    Andrew complete Roman Urdu text ko zyada reliably bol raha hai.
    """

    if is_roman_urdu(text):
        return ROMAN_URDU_VOICE

    return ENGLISH_VOICE


# ==========================================================
# TTS GENERATION
# ==========================================================

async def generate_audio(text, voice, output_file):
    """
    Complete text ko ek hi Edge TTS request mein convert karta hai.
    """

    communicate = edge_tts.Communicate(
        text,
        voice
    )

    await communicate.save(output_file)


# ==========================================================
# PLAY AUDIO
# ==========================================================

def play_audio(audio_file):
    """
    Audio ko blocking mode mein play karta hai.
    Jab tak audio complete na ho, function return nahi hota.
    """

    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(20)

    pygame.mixer.music.stop()


# ==========================================================
# MAIN SPEAK FUNCTION
# ==========================================================

def speak(text):
    """
    Buddy ka main voice function.

    Important:
    - Complete text
    - Single TTS request
    - Single audio file
    - Blocking playback
    - No word splitting
    """

    if text is None:
        return

    text = str(text).strip()

    if not text:
        return

    voice_text = prepare_voice_text(text)

    if not voice_text:
        return

    voice = choose_voice(voice_text)

    temp_file = None

    with _audio_lock:

        try:

            print()
            print("[Buddy Voice] Preparing speech...")
            print("[TTS Voice]", voice)
            print("[TTS Text]", voice_text)

            with tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            ) as temp:

                temp_file = temp.name

            asyncio.run(
                generate_audio(
                    voice_text,
                    voice,
                    temp_file
                )
            )

            if not os.path.exists(temp_file):
                print("[Buddy Voice] ERROR: Audio file was not created.")
                return

            if os.path.getsize(temp_file) == 0:
                print("[Buddy Voice] ERROR: Empty audio file.")
                return

            print("[Buddy Voice] Playing...")

            play_audio(temp_file)

            print("[Buddy Voice] COMPLETE")

        except Exception as e:

            print(
                "[Buddy Voice] ERROR:",
                repr(e)
            )

        finally:

            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

            if temp_file and os.path.exists(temp_file):

                try:
                    os.remove(temp_file)

                except Exception:
                    pass


# ==========================================================
# LISTEN
# ==========================================================

def listen():
    """
    Microphone se user ki voice sunta hai.
    """

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print("[Voice Input] Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=12
            )

        print("[Voice Input] Processing...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        text = str(text).strip()

        print("[Voice Input] You said:", text)

        return text

    except sr.WaitTimeoutError:

        print("[Voice Input] Timeout.")
        return ""

    except sr.UnknownValueError:

        print("[Voice Input] Could not understand.")
        return ""

    except sr.RequestError as e:

        print(
            "[Voice Input] Recognition service error:",
            repr(e)
        )

        return ""

    except Exception as e:

        print(
            "[Voice Input] ERROR:",
            repr(e)
        )

        return ""


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print(" Buddy AI Voice Test")
    print("==========================================")

    test_text = (
        "Assalam o Alaikum Sir. "
        "Mera naam Buddy hai. "
        "Aaj hum Buddy AI ko mazeed behtareen banayenge. "
        "Main aapki baat poori tarah sununga aur poora jawab dunga."
    )

    print()
    print("Test Text:")
    print(test_text)
    print()

    speak(test_text)

    print()
    print("Voice test finished.")