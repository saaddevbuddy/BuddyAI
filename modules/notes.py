import os


def handle_notes(command, speak):

    note_file = "notes.txt"

    # ------------------- Save Note -------------------

    if command.startswith("note "):

        note = command.replace("note", "", 1).strip()

        with open(note_file, "a", encoding="utf-8") as f:
            f.write(note + "\n")

        reply = "Sir, note save kar diya hai."
        speak(reply)
        return reply

    # ------------------- Show Notes -------------------

    if (
        "show notes" in command
        or "meri notes" in command
        or "notes dikhao" in command
    ):

        if not os.path.exists(note_file):
            reply = "Sir, abhi koi note save nahi hai."
            speak(reply)
            return reply

        with open(note_file, "r", encoding="utf-8") as f:
            notes = f.read().strip()

        if not notes:
            reply = "Sir, notes file khali hai."
        else:
            reply = "Sir, ye aapke notes hain.\n" + notes

        speak(reply)
        return reply

    return None