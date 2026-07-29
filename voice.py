import pyttsx3
import speech_recognition as sr


def speak(text):

    print("🤖 Buddy:", text)

    try:
        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)

        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print("Voice Error:", e)



def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("🎤 Sun raha hoon...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        audio = recognizer.listen(source)


    try:

        text = recognizer.recognize_google(audio)

        print("👤 Saad:", text)

        return text


    except sr.UnknownValueError:

        speak("Maaf kijiye Sir, mujhe samajh nahi aaya.")

        return ""


    except sr.RequestError:

        speak("Sir, speech service mein masla hai.")

        return ""