import pyttsx3
import speech_recognition as sr
import time


def speak(text):
    time.sleep(0.7)

    engine = pyttsx3.init()
    print("Buddy:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Sun raha hoon...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Saad:", text)
        return text

    except sr.UnknownValueError:
        speak("Maaf kijiye, mujhe samajh nahi aaya.")
        return ""

    except sr.RequestError:
        speak("Internet ya Speech Service ka masla hai.")
        return ""