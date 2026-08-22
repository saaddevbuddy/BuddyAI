from modules.memory import load_memory, save_memory
PROFILE_FIELDS = {
    "name": "name",
    "favorite game": "favorite_game",
    "favorite colour": "favorite_colour",
    "favorite color": "favorite_colour",
    "favorite food": "favorite_food",
    "favorite phone": "favorite_phone",
    "favorite car": "favorite_car",
    "favorite youtuber": "favorite_youtuber",
    "favorite ai": "favorite_ai",
    "city": "city",
    "country": "country",
    "dream": "dream",
    "goal": "goal",
    "hobby": "hobby",
    "age": "age",
}


def _ensure_profile(memory):
    if "profile" not in memory:
        memory["profile"] = {}
    return memory["profile"]


def _save_field(memory, key, value):
    profile = _ensure_profile(memory)
    profile[key] = value
    save_memory(memory)


def _get_field(memory, key):
    profile = _ensure_profile(memory)
    return profile.get(key)


def handle_profile(command, speak):

    memory = load_memory()
    profile = _ensure_profile(memory)

    command = command.lower().strip()

    # ==========================
    # Save Name
    # ==========================

    if (
        "mera naam" in command
        and "kya hai" not in command
        and "hai" in command
    ):

        name = (
            command.replace("mera naam", "")
            .replace("hai", "")
            .strip()
            .title()
        )

        _save_field(memory, "name", name)

        reply = (
            f"Theek hai Sir, maine yaad rakh liya "
            f"ke aapka naam {name} hai."
        )

        speak(reply)
        return reply

    # ==========================
    # Ask Name
    # ==========================

    if (
        "mera naam kya hai" in command
        or "what is my name" in command
    ):

        name = _get_field(memory, "name")

        if name:
            reply = f"Sir, aapka naam {name} hai."
        else:
            reply = "Sir, mujhe abhi aapka naam yaad nahi."

        speak(reply)
        return reply

    # ==========================
    # Save Favourite Game
    # ==========================

    if (
        "mera favourite game" in command
        and "kya hai" not in command
        and "yaad hai" not in command
        and "hai" in command
    ):

        game = (
            command.replace("mera favourite game", "")
            .replace("hai", "")
            .strip()
            .upper()
        )

        _save_field(memory, "favorite_game", game)

        reply = (
            f"Theek hai Sir, maine yaad rakh liya "
            f"ke aapka favourite game {game} hai."
        )

        speak(reply)
        return reply

    # ==========================
    # Ask Favourite Game
    # ==========================

    if (
        "mera favourite game kya hai" in command
        or "favourite game kya hai" in command
        or "mera favourite game kon sa hai" in command
        or "mera favourite game kaun sa hai" in command
        or "mera favourite game yaad hai" in command
    ):

        game = _get_field(memory, "favorite_game")

        if game:
            reply = f"Sir, aapka favourite game {game} hai."
        else:
            reply = "Sir, mujhe abhi aapka favourite game yaad nahi."

        speak(reply)
        return reply

    # ======= PART 2 CONTINUE HOGA YAHAN SE =======
    # ==========================
    # Generic Save Profile Fields
    # ==========================

    for field_name, memory_key in PROFILE_FIELDS.items():

        if field_name == "name":
            continue

        if (
            f"mera {field_name}" in command
            and "kya hai" not in command
            and "kon sa" not in command
            and "kaun sa" not in command
            and "yaad hai" not in command
            and "hai" in command
        ):

            value = (
                command.replace(f"mera {field_name}", "")
                .replace("hai", "")
                .strip()
                .title()
            )

            _save_field(memory, memory_key, value)

            reply = (
                f"Theek hai Sir, maine yaad rakh liya "
                f"ke aapka {field_name} {value} hai."
            )

            speak(reply)
            return reply

    # ==========================
    # Generic Ask Profile Fields
    # ==========================

    for field_name, memory_key in PROFILE_FIELDS.items():

        if field_name == "name":
            continue

        if (
            f"mera {field_name} kya hai" in command
            or f"mera {field_name} kon sa hai" in command
            or f"mera {field_name} kaun sa hai" in command
            or f"mera {field_name} yaad hai" in command
        ):

            value = _get_field(memory, memory_key)

            if value:
                reply = (
                    f"Sir, aapka {field_name} "
                    f"{value} hai."
                )
            else:
                reply = (
                    f"Sir, mujhe abhi "
                    f"aapka {field_name} yaad nahi."
                )

            speak(reply)
            return reply

    # ==========================
    # Show Complete Profile
    # ==========================

    if (
        "meri profile" in command
        or "profile dikhao" in command
        or "my profile" in command
    ):

        reply = (
            "📋 Buddy Profile\n\n"
            f"👤 Name: {profile.get('name', 'Unknown')}\n"
            f"🎮 Favourite Game: {profile.get('favorite_game', 'Unknown')}\n"
            f"🎨 Favourite Colour: {profile.get('favorite_colour', 'Unknown')}\n"
            f"🍕 Favourite Food: {profile.get('favorite_food', 'Unknown')}\n"
            f"📱 Favourite Phone: {profile.get('favorite_phone', 'Unknown')}\n"
            f"🚗 Favourite Car: {profile.get('favorite_car', 'Unknown')}\n"
            f"▶ Favourite YouTuber: {profile.get('favorite_youtuber', 'Unknown')}\n"
            f"🤖 Favourite AI: {profile.get('favorite_ai', 'Unknown')}\n"
            f"🏙 City: {profile.get('city', 'Unknown')}\n"
            f"🌍 Country: {profile.get('country', 'Unknown')}\n"
            f"🎯 Dream: {profile.get('dream', 'Unknown')}\n"
            f"🏆 Goal: {profile.get('goal', 'Unknown')}\n"
            f"🎯 Hobby: {profile.get('hobby', 'Unknown')}\n"
            f"🎂 Age: {profile.get('age', 'Unknown')}"
        )

        speak(reply)
        return reply

    return None