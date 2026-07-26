from memory import load_memory, save_memory

def handle_brain(command, speak):
    

    command = command.lower()
    memory = load_memory()

    # Conversation Context
    if "context" not in memory:
        memory["context"] = {}
        save_memory(memory)

    # Greetings

    if any(word in command for word in ["hello", "hi", "assalam", "slam"]):

        reply = "Assalam-o-Alaikum Sir! Kaise hain aap?"

        speak(reply)
        return reply

    # How are you

    if "how are you" in command or "kaise ho" in command:

        reply = "Alhamdulillah Sir, main theek hoon. Aap sunaiye."

        speak(reply)
        return reply

    # Thank you

    if "thank" in command or "shukriya" in command:

        reply = "Hamesha Sir."

        speak(reply)
        return reply
    # ------------------- Sad Mood -------------------

    sad_words = [
        "sad",
        "udaas",
        "dukhi",
        "depressed",
        "tension",
        "pareshan"
    ]

    if any(word in command for word in sad_words):

        reply = (
            "Sir, mujhe afsos hai ke aap udaas hain. "
            "Allah sab aasaan kare. Agar baat karna chahein to main sun raha hoon."
        )

        speak(reply)
        return reply


    # ------------------- Happy Mood -------------------

    happy_words = [
        "happy",
        "khush",
        "bohot khushi",
        "excited"
    ]

    if any(word in command for word in happy_words):

        reply = (
            "MashAllah Sir! Allah aapko hamesha khush rakhe."
        )

        speak(reply)
        return reply
    # ------------------- Search Intent -------------------

    if (
        "video" in command
        or "tutorial" in command
        or "seekhna" in command
    ) and "python" in command:

        reply = "Sir, Python ki videos dhoond raha hoon."
        speak(reply)

        import webbrowser
        webbrowser.open(
            "https://www.youtube.com/results?search_query=Python+course"
        )

        return reply


    # ------------------- Open App Intent -------------------

    if "calculator" in command and (
        "open" in command
        or "khol" in command
        or "khol do" in command
    ):

        reply = "Sir, calculator khol raha hoon."
        speak(reply)

        import os
        os.system("calc")

        return reply
     # ------------------- Ask Name -------------------

    if "mera naam kya hai" in command or "naam kya hai" in command:

        if "name" in memory:
            reply = f"Sir, aapka naam {memory['name']} hai."
            memory["context"]["last_topic"] = "name"
            save_memory(memory)
        else:
            reply = "Sir, mujhe abhi aapka naam yaad nahi hai."

        speak(reply)
        return reply


    # ------------------- Name Save -------------------

    if "mera naam" in command and "hai" in command and "kya" not in command:

        name = command.replace("mera naam", "")
        name = name.replace("hai", "")
        name = name.strip()

        memory["name"] = name
        save_memory(memory)

        reply = f"Theek hai Sir, maine yaad rakh liya ke aapka naam {name} hai."

        speak(reply)
        return reply
    # ------------------- Favourite Game Save -------------------

    if "favourite game" in command and "kya" not in command:

        game = command.replace("mera favourite game", "")
        game = game.replace("hai", "")
        game = game.strip()

        memory["favorite_game"] = game

        save_memory(memory)

        reply = f"Theek hai Sir, maine yaad rakh liya ke aapka favourite game {game} hai."
        memory["context"]["last_topic"] = "favorite_game"
        save_memory(memory)

        speak(reply)
        return reply


    # ------------------- Favourite Game Ask -------------------

    if "favourite game kya hai" in command:

        if "favorite_game" in memory:

            reply = f"Sir, aapka favourite game {memory['favorite_game']} hai."
            memory["context"]["last_topic"] = "favorite_game"
            save_memory(memory)

        else:

            reply = "Sir, mujhe abhi aapka favourite game yaad nahi hai."

        speak(reply)
        return reply
    # ------------------- Favourite Colour Save -------------------

    if "favourite colour" in command and "kya" not in command:

        colour = command.replace("mera favourite colour", "")
        colour = colour.replace("hai", "")
        colour = colour.strip()

        memory["favorite_colour"] = colour

        save_memory(memory)

        reply = f"Theek hai Sir, maine yaad rakh liya ke aapka favourite colour {colour} hai."

        speak(reply)
        return reply


    # ------------------- Favourite Colour Ask -------------------

    if "favourite colour kya hai" in command:

        if "favorite_colour" in memory:

            reply = f"Sir, aapka favourite colour {memory['favorite_colour']} hai."

        else:

            reply = "Sir, mujhe abhi aapka favourite colour yaad nahi hai."

        speak(reply)
        return reply
    # ------------------- Favourite Food Save -------------------

    if "favourite food" in command and "kya" not in command:

        food = command.replace("mera favourite food", "")
        food = food.replace("hai", "")
        food = food.strip()

        memory["favorite_food"] = food

        save_memory(memory)

        reply = f"Theek hai Sir, maine yaad rakh liya ke aapka favourite food {food} hai."

        speak(reply)
        return reply


    # ------------------- Favourite Food Ask -------------------

    if "favourite food kya hai" in command:

        if "favorite_food" in memory:

            reply = f"Sir, aapka favourite food {memory['favorite_food']} hai."

        else:

            reply = "Sir, mujhe abhi aapka favourite food yaad nahi hai."

        speak(reply)
        return reply
    # ------------------- Hobby Save -------------------

    if "meri hobby" in command and "kya" not in command:

        hobby = command.replace("meri hobby", "")
        hobby = hobby.replace("hai", "")
        hobby = hobby.strip()

        memory["hobby"] = hobby

        save_memory(memory)

        reply = f"Theek hai Sir, maine yaad rakh liya ke aapki hobby {hobby} hai."

        speak(reply)
        return reply


    # ------------------- Hobby Ask -------------------

    if "meri hobby kya hai" in command or "hobby kya hai" in command:

        if "hobby" in memory:

            reply = f"Sir, aapki hobby {memory['hobby']} hai."

        else:

            reply = "Sir, mujhe abhi aapki hobby yaad nahi hai."

        speak(reply)
        return reply
    # ------------------- Profile Show -------------------

    if (
        "meri profile dikhao" in command
        or "my profile" in command
        or "profile dikhao" in command
    ):

        reply = "Sir, aapki profile ye hai. "

        if "name" in memory:
            reply += f"Aapka naam {memory['name']} hai. "

        if "favorite_game" in memory:
            reply += f"Aapka favourite game {memory['favorite_game']} hai. "

        if "favorite_colour" in memory:
            reply += f"Aapka favourite colour {memory['favorite_colour']} hai. "

        if "favorite_food" in memory:
            reply += f"Aapka favourite food {memory['favorite_food']} hai. "

        if "hobby" in memory:
            reply += f"Aapki hobby {memory['hobby']} hai."

        speak(reply)
        return reply
    return None