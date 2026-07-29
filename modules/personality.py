import random

INTRO = [
    "Main Buddy hoon Sir. Hamesha aap ki madad ke liye tayyar.",
    "Sir, main Buddy hoon. Batayein aaj kya madad kar sakta hoon?",
    "Buddy reporting Sir! Aaj kis cheez mein help chahiye?"
]

PRAISE = [
    "Shukriya Sir.",
    "Aap ke alfaaz sun kar khushi hui Sir.",
    "Aap ka bohot shukriya Sir."
]

JOKES = [
    "Sir, main chai nahi peeta... lekin agar peeta to coding aur tez ho jati.",
    "Mera favourite bug woh hota hai jo pehli baar mein hi fix ho jaye.",
    "Sir, AI bhi kabhi kabhi sochta hai... phir compile karta hai."
]

def random_intro():
    return random.choice(INTRO)

def random_praise():
    return random.choice(PRAISE)

def random_joke():
    return random.choice(JOKES)

MOTIVATION = [
    "Sir, har din kuch naya seekhna hi progress hai.",
    "In Sha Allah aap apne goals zaroor hasil karenge.",
    "Main aap ke saath hoon Sir, himmat mat harna.",
    "Allah par bharosa rakhein, mehnat kabhi zaya nahi hoti."
]

def random_motivation():
    return random.choice(MOTIVATION)