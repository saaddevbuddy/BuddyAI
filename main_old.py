import pyttsx3
import speech_recognition as sr
import time


engine = pyttsx3.init()

def speak(text):
    print("Buddy:", text)
    engine.say(text)
    engine.runAndWait()
print("Assalam o Alaikum Saad!")
print("Main Buddy hoon")
speak("ASsalam o alaikum Saad")

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
        print("Maaf kijiye, samajh nahi aaya.")
        return ""

    except sr.RequestError:
        print("Internet ya Speech Service ka masla hai.")
        return ""

def start_conversation():
    speak("Assalam o Alaikum Saad")
    time.sleep(2)

    speak("Aap ka naam kya hai?")
    name = listen()

    if name == "":
        speak("Main aap ki baat samajh nahi saka.")
        return

    speak("Aapse mil kar khushi hui " + name)

    speak("Aap kis city se hain?")
    city = listen()

    if city != "":
        speak("Ma Sha Allah. Aap " + city + " se hain.")





print("Aaj se hamara safar shuru hua")
print("In Sha Allah main har din behter hoonga")
speak("Aapka naam kya hai?")
time.sleep(2)
name = listen()
speak("Aapse mil kar khushi hui " + name)
city = input("Aap kis city se hain")
print("Ma Sha Allah ap" , city , "se hain")

print("-----------")
print("Chalo Addition kartay hain")
num1 = int(input("Pehla number likho:"))
num2 = int(input("Doosra Number likho:"))
result = num1 + num2
print("Jawab hay:", result)
num3 = input("1st num")
num4 = input("2nd num")
result = num3 + num4
print("ans yah hay:", result)
print("-----------")
print("Buddy Decision System")
age = int(input("Apni age likho:"))
if age >= 18:
    print("Ma Sha Allah! Aap vote de sakty hain")
else:
    print("nhi de sakty 😥")
marks = int(input("Marks likho apnay"))
if marks < 33:
        print("Maazrat App dobara Koshish krein")
else:
        print("Mubarak hoo!😍🎊✨ App pass hogaye")
print("====== Buddy Security=====")
password = input("password:")
age = int(input(" Age likho"))
if password == "Buddy123" and age >= 18:
    print("Access Granted")
else:
  print("Access Denied")

print("-----------")
print("Day 5")
password = input("Password")

if password == "Buddy123":
    print("Password correct")

    age = int(input("Age Likho:"))

    if age >= 18:
        print("Welcome to BuddyAi")
    else:
        print("Age Not Allowed")

else:
    print("Wronge Password")

print("Day 5 own")

password = input("Password")
if password == "Buddy123":
    print("password sahi hay")

    age = int(input("your Age"))

    if age >= 18:
        print("Age Allowed person")
    else:
        print("Not Allowed age person")
else:
    print("password Ghalat hay")


print("----------Day 6------------")
username = input("username")
print("Username:")
if username == "Saad"or username == "Admin":
    print("Welcom to buddy")
else:
    print("unknown user")

print("BUDDY ATM")
username = input("Input username")
password = input("input password")
balance = 5000
if username == "Saad" and password == "Buddy123":
  print("Your balance is 5000")
withdrawamount = int(input("withdraw amount"))
if withdrawamount > balance:
  print("unsufficient balance")
else:
    print("transaction success")
    remaining = balance - withdrawamount
    print("Remaining balance",remaining)

print("-----DAY 7--------")
num = 1
while num <= 10:
    print("I love PYTHON")
    num = num + 1

num = 1
while num <= 10:
    print(num, "I love PYTHON")
    num = num + 1

num = 2
while num <= 20:
    print(num, "I love PYTHON")
    num = num + 2

num = 1
while num <= 15:
    print(num, "I love PYTHON")
    num = num + 2

print("1.Login")
print("2.ATM")
print("3.Exit")
choice = int(input("Choice"))
if choice == 1:
    print("Login open")
elif choice == 2:
    print("ATM open")
elif choice == 3:
    print("Allah Hafiz")
else:
    print("invalid Choice")

print("DAy 8")
number = 1
for number in range(1,11):
  print(number)

renum = 1
for renum in range(10,0,-1):
    print(renum)

number2 = 2
for number2 in range(2,21,2):
  print(number2)

print("DAY_________9")

def welcome():
    print("Assalam O Alaikum!")
    print("Welcome to Buddy AI")

welcome()
def myname():
    print("created byMuhammad Saad")

myname()
def login():
      print("Login Open")
def atm():
     print("ATM Open")
def calculator():
  print("Calculator Open")


print("=====Buddy AI======")
print("1.Login")
print("2.ATM")
print("3.Calculator")
choice = int(input("Enter Choice:"))
if choice == 1:
    login()

elif choice == 2:
    atm()

elif choice == 3:
    calculator()

else:
    print("Invalid choice")

import random
import string
def password_generator():
    print("\n===== Password Generator =====")

    length = int(input("Password ki length likhein: "))

    characters = string.ascii_letters + string.digits + string.punctuation

    password = ""

    for i in range(length):
        password += random.choice(characters)

    print("Generated Password:", password)

def calculator():
    while True:
        print("\n===== Calculator =====")

        num1 = float(input("Pehla number enter karein: "))
        num2 = float(input("Doosra number enter karein: "))

        print("\nOperation select karein:")
        print("+ Addition")
        print("- Subtraction")
        print("* Multiplication")
        print("/ Division")

        operation = input("Operation likhein (+, -, *, /): ")

        if operation == "+":
            print("Result:", num1 + num2)

        elif operation == "-":
            print("Result:", num1 - num2)

        elif operation == "*":
            print("Result:", num1 * num2)

        elif operation == "/":
            if num2 != 0:
                print("Result:", num1 / num2)
            else:
                print("ERROR! 0 se division mumkin nahi.")

        else:
            print("Invalid Operation!")

        choice = input("\nDobara calculation karni hai? (Y/N): ")

        if choice.lower() == "n":
            print("Calculator band ho raha hai...")
            break


def about():
    print("\n===== About Buddy AI =====")
    print("Project Name : Buddy AI")
    print("Developer    : Muhammad Saad")
    print("Language     : Python")
    print("Version      : 1.1")
    print("Description  : A personal AI assistant made in Python.")
    print("Thank you for using Buddy AI!")

def age_calculator():
    print("\n===== Age Calculator =====")

    birth_year = int(input("Apna Birth Year likhein: "))
    current_year = int(input("Current Year likhein: "))

    age = current_year - birth_year

    print("Aap ki age hai:", age, "saal")

def notes():
    print("\n===== Buddy Notes =====")

    print("1. Note Save Karein")
    print("2. Notes Dekhein")

    choice = input("Apni choice likhein: ")

    if choice == "1":
        note = input("Kya yaad rakhna hai?: ")

        with open("notes.txt", "a") as file:
            file.write(note + "\n")

        print("Buddy ne yaad rakh liya!")

    elif choice == "2":
        try:
            with open("notes.txt", "r") as file:
                notes_data = file.read()

            print("\n===== Saved Notes =====")
            print(notes_data)

        except FileNotFoundError:
            print("Abhi koi note save nahi hai.")

    else:
        print("Invalid Choice!")

while True:
    print("\n===== Buddy AI =====")
    print("1. Calculator")
    print("2. About")
    print("3. Age Calculator")
    print("4. Password Generator")
    print("5. Notes")
    print("6. Start Conversation")
    print("7. Exit")

    choice = input("Apni choice likhein: ")
while True:
    print("\n===== Buddy AI =====")
    print("1. Calculator")
    print("2. About")
    print("3. Age Calculator")
    print("4. Password Generator")
    print("5. Notes")
    print("6. Start Conversation")
    print("7. Exit")

    choice = input("Apni choice likhein: ")

    if choice == "1":
        calculator()

    elif choice == "2":
        about()

    elif choice == "3":
        age_calculator()

    elif choice == "4":
        password_generator()

    elif choice == "5":
        notes()

    elif choice == "6":
        start_conversation()

    elif choice == "7":
        print("Allah Hafiz! Buddy AI band ho raha hai.")
        break

    else:
        print("Invalid Choice!")
   
