import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def speak(text):
    print("🤖 Buddy:", text)
    engine.say(text)
    engine.runAndWait()