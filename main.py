import pyttsx3
import speech_recognition as sr
import datetime
import random
import time
import os
from commands import handle_command
from voice import speak, listen


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

brain = {
    "khush": "MashaAllah! Allah aap ko hamesha khush rakhe.",
    "udaas": "Allah behtari kare. Agar baat karni ho to main sun raha hoon.",
    "gussa": "Gussa kabhi kabhi aa jata hai. Umeed hai sab theek ho jayega.",
    "thak": "Lagta hai aaj ka din lamba tha. Thoda aaram kar lijiye.",
    "bhook": "Pehle kuch kha lijiye. Khali pait kaam karna mushkil hota hai.",
    "bhook lagi": "Pehle kuch kha lijiye. Phir aaram se baat karte hain.",
    "pareshan": "Har mushkil ke saath aasani hai. Allah par bharosa rakhiye.",
    "tension": "Zyada tension mat lijiye. In Sha Allah sab behtar hoga.",
    "dar": "Allah aap ke saath hai. Himmat rakhiye.",
    "alhamdulillah": "Alhamdulillah! Allah ka shukar hamesha ada karna chahiye.",
    "shukr": "Alhamdulillah. Allah aur barkat ata farmaye.",
    "theek": "Ye sun kar khushi hui.",
    "thank you": "Aap ka hamesha khair maqdam hai.",
    "shukriya": "Khushi hui madad karke.",
    "allah hafiz": "Allah Hafiz. Allah aap ki hifazat farmaye.",
    "bye": "Allah Hafiz. Phir mulaqat hogi.",
    "tum kaise ho": "Alhamdulillah! Main theek hoon. Aap sunaiye?",

"tumhara naam kya hai": "Mera naam Buddy hai.",

"mera naam kya hai": "Aap ka naam Muhammad Saad hai.",

"kaun ho tum": "Main Buddy hoon, aap ka AI Assistant.",
"kon banaya tumhe": "Mujhe Muhammad Saad aur mere Sir mil kar bana rahe hain.",

"kis ne banaya": "Mujhe Muhammad Saad aur mere Sir ne develop kiya hai.",

"tum kya kar sakte ho": "Main apps khol sakta hoon, waqt aur tareekh bata sakta hoon aur roz roz aur smart hota ja raha hoon.",
"kya kar sakte ho": "Main apps khol sakta hoon, waqt aur tareekh bata sakta hoon aur roz roz aur smart hota ja raha hoon.",

"tum kya kar sakte ho": "Main apps khol sakta hoon, waqt aur tareekh bata sakta hoon aur roz roz aur smart hota ja raha hoon.",

"what can you do": "Main apps khol sakta hoon, waqt aur tareekh bata sakta hoon aur roz roz aur smart hota ja raha hoon.",
}
replies = {
    "khush": [
        "MashaAllah! Allah aap ko hamesha khush rakhe.",
        "Ye sun kar khushi hui.",
        "Allah aap ki khushiyan barqarar rakhe.",
        "Alhamdulillah! Bohot achhi baat hai."
    ],

    "udaas": [
        "Allah behtari kare. Agar baat karni ho to main sun raha hoon.",
        "Umeed hai Allah aap ke liye aasani paida farmayega.",
        "Har mushkil ke baad aasani hai."
    ],

    "gussa": [
        "Gussa kabhi kabhi aa jata hai. Umeed hai sab theek ho jayega.",
        "Thoda sukoon se sochiye, In Sha Allah behtari hogi.",
        "Allah aap ko sukoon ata farmaye."
    ],

    "thak": [
        "Lagta hai aaj ka din lamba tha.",
        "Thoda aaram kar lijiye.",
        "Aaj kaafi mehnat ki lagti hai."
    ]

}
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

    mood = listen()
    if handle_command(mood, speak):
        return

    if mood != "":
        mood = mood.lower()
        if "notepad" in mood:
            speak("Notepad khol raha hoon.")
            os.system("notepad")
            return

        if "calculator" in mood:
            speak("Calculator khol raha hoon.")
            os.system("calc")
            return

        if "time" in mood:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak("Abhi waqt hai " + current_time)
                return

        if "date" in mood:
                current_date = datetime.datetime.now().strftime("%d %B %Y")
                speak("Aaj ki tareekh hai " + current_date)
                return
                
        found = False

        for word in brain:

            if word in mood:

                if word in replies:
                    speak(name + ", " + random.choice(replies[word]))
                else:
                    speak(name + ", " + brain[word])

                found = True
                break

        if found == False:
            speak(name + ", Samajh gaya.")
def start_buddy():
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