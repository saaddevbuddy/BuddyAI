import speech_recognition as sr
import datetime
import random
import time
import os
from commands import handle_command
from voice import speak, listen
from modules.brain import handle_brain
from modules.router import route
from modules.scheduler import start_scheduler
def save_name(name):
    file = open("name.txt", "w")
    file.write(name)
    file.close()
 
def load_name():
    try:
        file = open("name.txt", "r")
        name = file.read()
        file.close()
        return name
    except:
        return ""

def greet(name):
    
   

    hour = datetime.datetime.now().hour
   
    if hour >= 5 and hour < 12:
        speak("Assalam o Alaikum " + name + ". Subah bakhair.")

    elif hour >= 12 and hour < 17:
        speak("Assalam o Alaikum " + name + ". Umeed hai aap ka din achha ja raha hoga.")

    elif hour >= 17 and hour < 20:
        speak("Assalam o Alaikum " + name + ". Shaam mubarak.")

    else:
        speak("Assalam o Alaikum " + name + ". Umeed hai aap khairiyat se hain.")


def chat():

    name = load_name()

    if name == "":
        speak("Assalam o Alaikum")
        speak("Ap ka nam kia hai?")

        name = listen()

        if name != "":
            save_name(name)
            speak("Aapse mil kar khushi hui " + name)

    else:
        greet(name)

    speak("Aaj aap kaise hain?")

    while True:

        mood = listen()

        if mood == "":
            continue

        mood = mood.lower()

        # Exit Conversation
        if "bye" in mood or "allah hafiz" in mood or "exit" in mood:
            speak("Allah Hafiz Sir.")
            break
        reply = route(mood, speak)

        if reply:
            speak(f"{name}, {reply}")


def start_buddy():

    print("Buddy AI Starting...")

    # Reminder Scheduler Start
    start_scheduler(speak)

    while True:

        print("\n==========================")
        print("       🤖 BUDDY AI")
        print("==========================")
        print("1. Start Conversation")
        print("2. Exit")
        print("==========================")

        choice = input("Enter Choice: ")

        if choice == "1":
            chat()

        elif choice == "2":
            speak("Allah Hafiz")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    start_buddy()