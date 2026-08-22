import asyncio
import edge_tts
import pygame
import speech_recognition as sr
import tempfile
import os
import time

# ------------------------------------
# Voice Settings
# ------------------------------------

VOICE = "en-GB-RyanNeural"   # Natural Female Voice
RATE = "+0%"
VOLUME = "+0%"

pygame.mixer.init()


# ------------------------------------
# Speak Function
# ------------------------------------

def speak(text):
    """
    Buddy AI Speak Function
    Uses Microsoft Edge TTS
    """

    print(f"\n🤖 Buddy: {text}")

    if not text:
        return

    try:
        asyncio.run(_edge_speak(text))

    except Exception as e:
        print("Voice Error:", e)


async def _edge_speak(text):

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    temp_file.close()

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
        volume=VOLUME
    )

    await communicate.save(temp_file.name)

    pygame.mixer.music.load(temp_file.name)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()

    try:
        os.remove(temp_file.name)
    except:
        pass


# ------------------------------------
# Listen Function
# ------------------------------------

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\n🎤 Sun raha hoon...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print(f"👤 Saad: {text}")

        return text

    except sr.UnknownValueError:

        speak("Maaf kijiye Sir, mujhe samajh nahi aaya.")
        return ""

    except sr.RequestError:

        speak("Sir, speech service mein masla hai.")
        return ""

    except Exception as e:

        print("Speech Error:", e)
        return ""