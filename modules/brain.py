import random

brain = {
    "khush": [
        "MashaAllah! Allah aap ko hamesha khush rakhe.",
        "Ye sun kar khushi hui.",
        "Allah aap ki khushiyan barqarar rakhe.",
        "Alhamdulillah! Bohot achhi baat hai."
    ],

    "udaas": [
        "Allah behtari kare. Agar baat karni ho to main sun raha hoon.",
        "Har mushkil ke baad aasani hai.",
        "Allah aap ke liye aasani paida farmaye."
    ],

    "gussa": [
        "Gussa kabhi kabhi aa jata hai.",
        "Allah aap ko sukoon ata farmaye.",
        "Thoda sukoon se sochiye."
    ],

    "thak": [
        "Lagta hai aaj ka din lamba tha.",
        "Thoda aaram kar lijiye.",
        "Aap ne kaafi mehnat ki lagti hai."
    ],

    "bhook": [
        "Pehle kuch kha lijiye.",
        "Khali pait kaam karna mushkil hota hai."
    ],

    "tension": [
        "Allah par bharosa rakhiye.",
        "In Sha Allah sab behtar hoga."
    ],

    "thank you": [
        "Aap ka hamesha khair maqdam hai.",
        "Khushi hui madad karke."
    ],

    "shukriya": [
        "Aap ka hamesha khair maqdam hai.",
        "Khushi hui madad karke."
    ],

    "allah hafiz": [
        "Allah Hafiz. Allah aap ki hifazat farmaye."
    ],

    "bye": [
        "Allah Hafiz. Phir mulaqat hogi."
    ],

    "tum kaise ho": [
        "Alhamdulillah! Main theek hoon. Aap sunaiye?"
    ],

    "tumhara naam kya hai": [
        "Mera naam Buddy hai."
    ],

    "mera naam kya hai": [
        "Aap ka naam Muhammad Saad hai."
    ],

    "main kon hoon": [
        "Aap Muhammad Saad hain."
    ],

    "kaun ho tum": [
        "Main Buddy hoon, aap ka AI Assistant."
    ],

    "kis ne banaya": [
        "Mujhe Muhammad Saad aur mere Sir develop kar rahe hain."
    ],

    "tum kya kar sakte ho": [
        "Main apps khol sakta hoon, waqt aur tareekh bata sakta hoon aur bohot se commands perform kar sakta hoon."
    ],

    "what can you do": [
        "Main apps khol sakta hoon, waqt aur tareekh bata sakta hoon aur bohot se commands perform kar sakta hoon."
    ],
    "assalam o alaikum": [
    "Walaikum Assalam Sir! Kaise hain aap?"
],

    "assalamualaikum": [
        "Walaikum Assalam Sir! Kaise hain aap?"
    ],

    "salam": [
        "Wa Alaikum Assalam Sir!"
    ],

    "hello": [
        "Hello Sir! Kaise hain aap?"
    ],

    "hi": [
        "Hi Sir! Kaise hain aap?"
    ],

    "good morning": [
        "Good Morning Sir! Allah aap ka din behtareen kare."
    ],

    "good night": [
        "Good Night Sir! Allah Hafiz, achhi neend aaye."
    ],

    "good evening": [
        "Good Evening Sir!"
    ],

    "good afternoon": [
        "Good Afternoon Sir!"
    ],

    "kon ho tum": [
        "Main Buddy hoon Sir, aap ka AI Assistant."
    ],

    "who are you": [
        "Main Buddy hoon Sir."
    ],

    "mera dost banoge": [
        "Main pehle se hi aap ka dost hoon Sir."
    ],

    "i love you": [
        "Shukriya Sir. Main hamesha aap ki madad ke liye hoon."
    ],

    "allah": [
        "SubhanAllah."
    ],

    "alhamdulillah": [
        "Alhamdulillah! Allah ka shukar hai."
    ],

    "mashaallah": [
        "MashaAllah! Allah aur barkat ata farmaye."
    ],
    "acha": [
    "Theek hai Sir."
],

    "theek hai": [
        "Ji Sir."
    ],

    "ok": [
        "Ji Sir."
    ],

    "okay": [
        "Theek hai Sir."
    ],

    "haan": [
        "Ji Sir."
    ],

    "yes": [
        "Ji Sir."
    ],

    "wah": [
        "Shukriya Sir."
    ],

    "good": [
        "Khushi hui ke aap ko pasand aaya."
    ],

    "bohot acha": [
        "Shukriya Sir, main aur behtar banne ki koshish karunga."
    ],
    "tum kis ne banaya": [
        "Sir, mujhe Muhammad Saad aur mere Sir mil kar bana rahe hain."
    ],

    "tumhara developer kon hai": [
        "Sir, mera developer Muhammad Saad hai."
    ],

    "good night": [
        "Good Night Sir. Allah aap ko sukoon bhari neend ata farmaye."
    ],

    "good morning": [
        "Good Morning Sir. Umeed hai aaj ka din bohot achha guzrega."
    ],

    "good evening": [
        "Good Evening Sir."
    ]
}


def get_reply(message):
    message = message.lower()

    for key, replies in brain.items():
        if key in message:
            return random.choice(replies)

    return None


def handle_brain(message, speak=None):
    """
    Brain se reply do.
    Agar reply mil jaye to bol bhi de aur return bhi kare.
    """

    reply = get_reply(message)

    if reply:

        if speak:
            speak(reply)

        return reply

    return None