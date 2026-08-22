import os


NOTE_FILE = "notes.txt"


def load_notes():
    """Saare notes list ki form mein load karta hai."""

    if not os.path.exists(NOTE_FILE):
        return []

    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip()
        ]


def save_notes(notes):
    """Notes ko file mein dobara save karta hai."""

    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(note + "\n")


def handle_notes(command, speak):

    command = command.strip()

    # ==================================================
    # SAVE NOTE
    # ==================================================

    if (
    command.lower().startswith("note ")
    and "delete" not in command.lower()
    and "hata" not in command.lower()
    and "mita" not in command.lower()
    ):

        note = command[5:].strip()

        if not note:
            reply = "Sir, note mein kya save karna hai?"
            speak(reply)
            return reply

        with open(
            NOTE_FILE,
            "a",
            encoding="utf-8"
        ) as f:
            f.write(note + "\n")

        reply = "Sir, note save kar diya hai."
        speak(reply)

        return reply

    # ==================================================
    # SHOW NOTES
    # ==================================================

    if (
        command.lower() == "show notes"
        or command.lower() == "meri notes"
        or command.lower() == "notes dikhao"
        or command.lower() == "mere notes"
    ):

        notes = load_notes()

        if not notes:

            reply = "Sir, abhi koi note save nahi hai."
            speak(reply)

            return reply

        reply = "Sir, ye aapke notes hain:\n\n"

        for i, note in enumerate(notes, start=1):
            reply += f"{i}. {note}\n"

        speak(reply)

        return reply

    # ==================================================
    # DELETE NOTE
    # ==================================================

    if (
        "delete note" in command.lower()
        or "note delete" in command.lower()
        or "note hata" in command.lower()
        or "note mita" in command.lower()
    ):

        words = command.lower().split()

        note_number = None

        for word in words:

            if word.isdigit():
                note_number = int(word)
                break

        if note_number is None:

            reply = (
                "Sir, kaunsa note delete karna hai? "
                "Misal ke taur par: note 2 delete karo."
            )

            speak(reply)
            return reply

        notes = load_notes()

        if not notes:

            reply = "Sir, koi note saved nahi hai."
            speak(reply)

            return reply

        if note_number < 1 or note_number > len(notes):

            reply = (
                f"Sir, note number {note_number} "
                "maujood nahi hai."
            )

            speak(reply)
            return reply

        deleted_note = notes.pop(note_number - 1)

        save_notes(notes)

        reply = (
            f"Ji Sir, note {note_number} delete kar diya.\n"
            f"Note tha: {deleted_note}"
        )

        speak(reply)

        return reply

    # ==================================================
    # SEARCH NOTES
    # ==================================================

    if (
        "search notes" in command.lower()
        or "notes search" in command.lower()
        or "notes mein search" in command.lower()
    ):

        # Search keyword nikalna
        keyword = ""

        if "search notes" in command.lower():

            keyword = command.lower().split(
                "search notes",
                1
            )[1].strip()

        elif "notes search" in command.lower():

            keyword = command.lower().split(
                "notes search",
                1
            )[1].strip()

        elif "notes mein search" in command.lower():

            keyword = command.lower().split(
                "notes mein search",
                1
            )[1].strip()

        if not keyword:

            reply = (
                "Sir, kya search karna hai? "
                "Misal: notes mein search Physics."
            )

            speak(reply)
            return reply

        notes = load_notes()

        results = []

        for i, note in enumerate(notes, start=1):

            if keyword.lower() in note.lower():

                results.append(
                    f"{i}. {note}"
                )

        if not results:

            reply = (
                f"Sir, '{keyword}' se related "
                "koi note nahi mila."
            )

        else:

            reply = (
                f"Sir, '{keyword}' se related notes:\n\n"
                + "\n".join(results)
            )

        speak(reply)

        return reply

    # ==================================================
    # CLEAR ALL NOTES
    # ==================================================

    if (
        command.lower() == "clear notes"
        or command.lower() == "delete all notes"
        or command.lower() == "saare notes delete karo"
    ):

        notes = load_notes()

        if not notes:

            reply = "Sir, delete karne ke liye koi notes nahi hain."
            speak(reply)

            return reply

        # Safety confirmation ke liye signal
        reply = (
            "Sir, aapke saare notes delete ho jayenge. "
            "Agar confirm karna hai to 'confirm delete notes' boliye."
        )

        speak(reply)

        return reply

    # ==================================================
    # CONFIRM DELETE ALL
    # ==================================================

    if (
        command.lower() == "confirm delete notes"
        or command.lower() == "confirm notes delete"
    ):

        notes = load_notes()

        if not notes:

            reply = "Sir, koi notes saved nahi hain."
            speak(reply)

            return reply

        save_notes([])

        reply = "Ji Sir, saare notes delete kar diye hain."

        speak(reply)

        return reply

    # ==================================================
    # NOTHING MATCHED
    # ==================================================

    return None