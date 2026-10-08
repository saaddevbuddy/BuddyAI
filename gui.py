# ==========================================================
# Buddy AI - Modern Pro Dark GUI
# Voice + Sound Control + Avatar + Mood + Proactive Mode
# ==========================================================

import os
import threading
import datetime
import time
import tkinter as tk


# ==========================================================
# Buddy Modules
# ==========================================================

from modules.router import route
from voice import speak as real_speak
from voice import listen
from modules.buddy_mood import get_buddy_mood

from modules.proactive import (
    start_proactive,
    stop_proactive,
    set_proactive_callback
)


# ==========================================================
# Pillow
# ==========================================================

try:

    from PIL import Image, ImageTk

    PIL_AVAILABLE = True

except ImportError:

    PIL_AVAILABLE = False

    print("[Avatar] Pillow is not installed.")


# ==========================================================
# GLOBALS
# ==========================================================

root = None

chat_box = None
entry_box = None

avatar_label = None
sidebar_avatar_label = None

status_label = None
clock_label = None
uptime_label = None

sound_button = None

avatar_images = {}
sidebar_avatar_images = {}

current_avatar_state = "idle"

avatar_animation_job = None

avatar_bob_offset = 0
avatar_bob_direction = 1

start_time = time.time()

sound_enabled = True

speaking_active = False


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================================
# AVATAR FOLDER
# ==========================================================

AVATAR_FOLDER = os.path.join(
    BASE_DIR,
    "assets",
    "avatar"
)


# ==========================================================
# AVATAR FILES
# ==========================================================

AVATAR_FILES = {

    "idle": "buddy_idle.png.jpg",

    "listening": "buddy_listening.png.jpg",

    "thinking": "buddy_thinking.png.jpg",

    "speaking": "buddy_speaking.png.jpg",

    "happy": "buddy_happy.png.jpg",

    "concerned": "buddy_concerned.png.jpg"
}


# ==========================================================
# COLORS
# ==========================================================

BG_COLOR = "#08111F"

SIDEBAR_COLOR = "#0D1726"

CARD_COLOR = "#111E30"

CARD_LIGHT = "#16263B"

TEXT_COLOR = "#EAF4FF"

SECONDARY_TEXT = "#91A4BB"

BLUE = "#2196F3"

BLUE_LIGHT = "#42A5F5"

GREEN = "#35D07F"

YELLOW = "#FFD166"

RED = "#FF647C"


# ==========================================================
# SAFE TKINTER CALLBACK
# ==========================================================

def safe_after(delay, callback):

    try:

        if (
            root is not None
            and root.winfo_exists()
        ):

            return root.after(
                delay,
                callback
            )

    except Exception:

        pass

    return None


# ==========================================================
# SOUND CONTROL
# ==========================================================

def toggle_sound():

    global sound_enabled

    sound_enabled = not sound_enabled

    update_sound_button()

    if sound_enabled:

        print("[Sound] ON")

        if status_label is not None:

            status_label.configure(
                text="● Sound ON",
                fg=GREEN
            )

            safe_after(
                1200,
                update_status_online
            )

    else:

        print("[Sound] OFF")

        if status_label is not None:

            status_label.configure(
                text="● Sound OFF",
                fg=YELLOW
            )


# ==========================================================
# SOUND BUTTON
# ==========================================================

def update_sound_button():

    if sound_button is None:

        return

    try:

        if sound_enabled:

            sound_button.configure(
                text="🔊 Sound ON",
                fg=GREEN
            )

        else:

            sound_button.configure(
                text="🔇 Sound OFF",
                fg=YELLOW
            )

    except Exception:

        pass


# ==========================================================
# STOP SPEAKING
# ==========================================================

def stop_speaking():

    global speaking_active

    print("[Voice] Stop requested.")

    speaking_active = False

    try:

        import pygame

        if pygame.mixer.get_init():

            pygame.mixer.music.stop()

    except Exception as e:

        print(
            "[Voice] Stop Error:",
            repr(e)
        )

    set_avatar_state("idle")

    update_status_online()


# ==========================================================
# CLEAR CHAT
# ==========================================================

def clear_chat():

    if chat_box is None:

        return

    try:

        chat_box.configure(
            state="normal"
        )

        chat_box.delete(
            "1.0",
            tk.END
        )

        chat_box.configure(
            state="disabled"
        )

        add_chat_message(
            "Buddy",
            "Chat clear ho gayi Sir. Main ready hoon.",
            is_user=False
        )

        set_avatar_state(
            "idle"
        )

        update_status_online()

        print("[Chat] Chat cleared.")

    except Exception as e:

        print(
            "[Chat] Clear Error:",
            repr(e)
        )


# ==========================================================
# LOAD AVATAR IMAGES
# ==========================================================

def load_avatar_images():

    global avatar_images
    global sidebar_avatar_images

    avatar_images = {}
    sidebar_avatar_images = {}

    if not PIL_AVAILABLE:

        print("[Avatar] Pillow missing.")

        return

    if not os.path.isdir(
        AVATAR_FOLDER
    ):

        print(
            "[Avatar] Folder missing:",
            AVATAR_FOLDER
        )

        return

    for state, filename in AVATAR_FILES.items():

        path = os.path.join(
            AVATAR_FOLDER,
            filename
        )

        if not os.path.exists(path):

            print(
                "[Avatar] Missing:",
                path
            )

            continue

        try:

            image = Image.open(
                path
            )

            image = image.convert(
                "RGB"
            )

            image.thumbnail(
                (
                    220,
                    220
                ),
                Image.Resampling.LANCZOS
            )

            avatar_images[state] = (
                ImageTk.PhotoImage(
                    image
                )
            )

            sidebar_image = Image.open(
                path
            )

            sidebar_image = sidebar_image.convert(
                "RGB"
            )

            sidebar_image.thumbnail(
                (
                    125,
                    125
                ),
                Image.Resampling.LANCZOS
            )

            sidebar_avatar_images[state] = (
                ImageTk.PhotoImage(
                    sidebar_image
                )
            )

            print(
                "[Avatar] Loaded:",
                state,
                filename
            )

        except Exception as e:

            print(
                "[Avatar] Load Error:",
                filename,
                repr(e)
            )


# ==========================================================
# SET AVATAR STATE
# ==========================================================

def set_avatar_state(state):

    global current_avatar_state

    if state not in AVATAR_FILES:

        state = "idle"

    current_avatar_state = state

    try:

        if (
            avatar_label is not None
            and state in avatar_images
        ):

            avatar_label.configure(
                image=avatar_images[state]
            )

        if (
            sidebar_avatar_label is not None
            and state in sidebar_avatar_images
        ):

            sidebar_avatar_label.configure(
                image=sidebar_avatar_images[state]
            )

    except Exception as e:

        print(
            "[Avatar] State Error:",
            repr(e)
        )


# ==========================================================
# AVATAR ANIMATION
# ==========================================================

def avatar_breathing_animation():

    global avatar_animation_job
    global avatar_bob_offset
    global avatar_bob_direction

    try:

        if (
            root is None
            or not root.winfo_exists()
            or avatar_label is None
        ):

            return

        if current_avatar_state == "speaking":

            speed = 1.0
            min_offset = -4
            max_offset = 5
            next_delay = 55

        elif current_avatar_state == "listening":

            speed = 0.65
            min_offset = -3
            max_offset = 3
            next_delay = 75

        elif current_avatar_state == "thinking":

            speed = 0.45
            min_offset = -2
            max_offset = 2
            next_delay = 90

        else:

            speed = 0.30
            min_offset = -2
            max_offset = 3
            next_delay = 100

        avatar_bob_offset += (
            speed
            * avatar_bob_direction
        )

        if avatar_bob_offset >= max_offset:

            avatar_bob_direction = -1

        elif avatar_bob_offset <= min_offset:

            avatar_bob_direction = 1

        avatar_label.place_configure(
            y=int(
                avatar_bob_offset
            )
        )

        avatar_animation_job = root.after(
            next_delay,
            avatar_breathing_animation
        )

    except Exception as e:

        print(
            "[Avatar Animation Error]:",
            repr(e)
        )

        avatar_animation_job = None


# ==========================================================
# CHAT MESSAGE
# ==========================================================

def add_chat_message(
    sender,
    message,
    is_user=False
):

    if chat_box is None:

        return

    try:

        chat_box.configure(
            state="normal"
        )

        if is_user:

            chat_box.insert(
                tk.END,
                "\nYou\n",
                "user_name"
            )

            chat_box.insert(
                tk.END,
                f"{message}\n",
                "user_message"
            )

        else:

            chat_box.insert(
                tk.END,
                "\nBuddy\n",
                "buddy_name"
            )

            chat_box.insert(
                tk.END,
                f"{message}\n",
                "buddy_message"
            )

        chat_box.configure(
            state="disabled"
        )

        chat_box.see(
            tk.END
        )

    except Exception as e:

        print(
            "[Chat] Error:",
            repr(e)
        )


# ==========================================================
# BUDDY SPEAK
# ==========================================================

def buddy_speak(text):

    global speaking_active

    if not text:

        return

    text = str(
        text
    ).strip()

    if not text:

        return

    # ------------------------------------------------------
    # SOUND OFF
    # ------------------------------------------------------

    if not sound_enabled:

        print(
            "[Voice] Sound OFF - skipping speech."
        )

        set_avatar_state(
            "idle"
        )

        update_status_online()

        return

    # ------------------------------------------------------
    # SPEAKING START
    # ------------------------------------------------------

    speaking_active = True

    set_avatar_state(
        "speaking"
    )

    if status_label is not None:

        try:

            status_label.configure(
                text="● Speaking...",
                fg=BLUE_LIGHT
            )

        except Exception:

            pass

    print(
        "[Avatar] Speaking animation START"
    )

    # ------------------------------------------------------
    # SPEAK THREAD
    # ------------------------------------------------------

    def speak_worker():

        global speaking_active

        try:

            if sound_enabled:

                real_speak(
                    text
                )

        except Exception as e:

            print(
                "[Voice Error]:",
                repr(e)
            )

        finally:

            speaking_active = False

            print(
                "[Avatar] Voice COMPLETE"
            )

            safe_after(
                0,
                finish_speaking
            )

    threading.Thread(
        target=speak_worker,
        daemon=True
    ).start()


# ==========================================================
# FINISH SPEAKING
# ==========================================================

def finish_speaking():

    set_avatar_state(
        "idle"
    )

    update_status_online()

    print(
        "[Avatar] Speaking animation STOP"
    )


# ==========================================================
# VOICE COMMAND
# ==========================================================

def voice_command():

    set_avatar_state(
        "listening"
    )

    if status_label is not None:

        status_label.configure(
            text="● Listening...",
            fg=BLUE_LIGHT
        )

    def voice_worker():

        try:

            result = listen()

            if result:

                safe_after(
                    0,
                    lambda r=result:
                    process_message(r)
                )

            else:

                safe_after(
                    0,
                    lambda:
                    set_avatar_state(
                        "idle"
                    )
                )

        except Exception as e:

            print(
                "[Voice] Error:",
                repr(e)
            )

            safe_after(
                0,
                lambda:
                set_avatar_state(
                    "idle"
                )
            )

        finally:

            # Do not force Online if a recognized
            # message has already started processing.
            pass

    threading.Thread(
        target=voice_worker,
        daemon=True
    ).start()


# ==========================================================
# ONLINE STATUS
# ==========================================================

def update_status_online():

    if status_label is None:

        return

    try:

        if sound_enabled:

            status_label.configure(
                text="● Online",
                fg=GREEN
            )

        else:

            status_label.configure(
                text="● Online • Muted",
                fg=YELLOW
            )

    except Exception:

        pass


# ==========================================================
# PROCESS MESSAGE
# ==========================================================

def process_message(
    message=None
):

    if message is None:

        try:

            message = (
                entry_box
                .get()
                .strip()
            )

        except Exception:

            return

    if not message:

        return

    try:

        entry_box.delete(
            0,
            tk.END
        )

    except Exception:

        pass

    add_chat_message(
        "You",
        message,
        is_user=True
    )

    set_avatar_state(
        "thinking"
    )

    if status_label is not None:

        status_label.configure(
            text="● Thinking...",
            fg=YELLOW
        )

    def ai_worker():

        try:

            print(
                "\n========== GUI ROUTER =========="
            )

            print(
                "User:",
                message
            )

            try:

                mood_result = get_buddy_mood()

                print(
                    "Buddy Mood:",
                    mood_result
                )

            except Exception as e:

                print(
                    "Mood Error:",
                    repr(e)
                )

            try:

                reply = route(
                    message
                )

            except TypeError:

                reply = route(
                    message,
                    ""
                )

            if reply is None:

                reply = (
                    "Sir, mujhe is waqt jawab dene mein "
                    "thora masla aa raha hai."
                )

            reply = str(
                reply
            ).strip()

            print(
                "Buddy Reply:",
                repr(reply)
            )

            lower_reply = reply.lower()

            if any(
                word in lower_reply
                for word in [
                    "sorry",
                    "fikr",
                    "pareshan",
                    "masla",
                    "concern"
                ]
            ):

                next_state = "concerned"

            elif any(
                word in lower_reply
                for word in [
                    "haha",
                    "hehe",
                    "khushi",
                    "great",
                    "zabardast",
                    "nice",
                    "lol"
                ]
            ):

                next_state = "happy"

            else:

                next_state = "speaking"

            safe_after(
                0,
                lambda r=reply:
                add_chat_message(
                    "Buddy",
                    r,
                    is_user=False
                )
            )

            safe_after(
                100,
                lambda r=reply:
                buddy_speak(r)
            )

        except Exception as e:

            print(
                "[GUI Router] Error:",
                repr(e)
            )

            error_reply = (
                "Sir, abhi Buddy ko jawab dene mein "
                "thora technical masla aa gaya."
            )

            safe_after(
                0,
                lambda:
                add_chat_message(
                    "Buddy",
                    error_reply,
                    is_user=False
                )
            )

            safe_after(
                0,
                lambda:
                set_avatar_state(
                    "concerned"
                )
            )

            safe_after(
                100,
                lambda:
                buddy_speak(
                    error_reply
                )
            )

    threading.Thread(
        target=ai_worker,
        daemon=True
    ).start()


# ==========================================================
# ENTER
# ==========================================================

def on_enter(event=None):

    process_message()

    return "break"


# ==========================================================
# CLOCK
# ==========================================================

def update_clock():

    if root is None:

        return

    try:

        now = datetime.datetime.now()

        if clock_label is not None:

            clock_label.configure(
                text=now.strftime(
                    "%I:%M %p"
                )
            )

        elapsed = int(
            time.time()
            - start_time
        )

        hours = (
            elapsed
            // 3600
        )

        minutes = (
            elapsed % 3600
        ) // 60

        seconds = (
            elapsed % 60
        )

        if uptime_label is not None:

            uptime_label.configure(
                text=(
                    f"Uptime "
                    f"{hours:02d}:"
                    f"{minutes:02d}:"
                    f"{seconds:02d}"
                )
            )

        root.after(
            1000,
            update_clock
        )

    except Exception:

        pass


# ==========================================================
# SIDEBAR BUTTON HELPER
# ==========================================================

def create_sidebar_button(
    parent,
    text,
    command,
    color=TEXT_COLOR
):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=CARD_COLOR,
        fg=color,
        activebackground=CARD_LIGHT,
        activeforeground=TEXT_COLOR,
        relief="flat",
        bd=0,
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        anchor="w",
        padx=14,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        padx=18,
        pady=3
    )

    return button


# ==========================================================
# SIDEBAR
# ==========================================================

def build_sidebar(parent):

    global sidebar_avatar_label
    global status_label
    global clock_label
    global uptime_label
    global sound_button

    sidebar = tk.Frame(
        parent,
        bg=SIDEBAR_COLOR,
        width=230
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(
        False
    )

    logo = tk.Label(
        sidebar,
        text="BUDDY AI",
        font=(
            "Segoe UI",
            20,
            "bold"
        ),
        fg=TEXT_COLOR,
        bg=SIDEBAR_COLOR
    )

    logo.pack(
        pady=(25, 4)
    )

    subtitle = tk.Label(
        sidebar,
        text="Your Living AI Companion",
        font=(
            "Segoe UI",
            9
        ),
        fg=SECONDARY_TEXT,
        bg=SIDEBAR_COLOR
    )

    subtitle.pack(
        pady=(0, 20)
    )

    avatar_card = tk.Frame(
        sidebar,
        bg=CARD_COLOR,
        width=190,
        height=180
    )

    avatar_card.pack(
        padx=18,
        pady=5
    )

    avatar_card.pack_propagate(
        False
    )

    sidebar_avatar_label = tk.Label(
        avatar_card,
        bg=CARD_COLOR
    )

    sidebar_avatar_label.pack(
        expand=True
    )

    status_title = tk.Label(
        sidebar,
        text="STATUS",
        font=(
            "Segoe UI",
            8,
            "bold"
        ),
        fg=SECONDARY_TEXT,
        bg=SIDEBAR_COLOR
    )

    status_title.pack(
        pady=(16, 2)
    )

    status_label = tk.Label(
        sidebar,
        text="● Online",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        fg=GREEN,
        bg=SIDEBAR_COLOR
    )

    status_label.pack()

    clock_label = tk.Label(
        sidebar,
        text="--:--",
        font=(
            "Segoe UI",
            20,
            "bold"
        ),
        fg=TEXT_COLOR,
        bg=SIDEBAR_COLOR
    )

    clock_label.pack(
        pady=(15, 0)
    )

    uptime_label = tk.Label(
        sidebar,
        text="Uptime 00:00:00",
        font=(
            "Segoe UI",
            8
        ),
        fg=SECONDARY_TEXT,
        bg=SIDEBAR_COLOR
    )

    uptime_label.pack(
        pady=(2, 12)
    )

    # ======================================================
    # CONTROLS
    # ======================================================

    controls_title = tk.Label(
        sidebar,
        text="CONTROLS",
        font=(
            "Segoe UI",
            8,
            "bold"
        ),
        fg=SECONDARY_TEXT,
        bg=SIDEBAR_COLOR
    )

    controls_title.pack(
        pady=(2, 6)
    )

    sound_button = create_sidebar_button(
        sidebar,
        "🔊 Sound ON",
        toggle_sound,
        GREEN
    )

    create_sidebar_button(
        sidebar,
        "⏹ Stop Speaking",
        stop_speaking,
        RED
    )

    create_sidebar_button(
        sidebar,
        "🧹 Clear Chat",
        clear_chat,
        TEXT_COLOR
    )

    # ======================================================
    # BOTTOM INFO
    # ======================================================

    info = tk.Label(
        sidebar,
        text=(
            "Buddy is here.\n"
            "Always ready to help."
        ),
        font=(
            "Segoe UI",
            9
        ),
        fg=SECONDARY_TEXT,
        bg=SIDEBAR_COLOR,
        justify="center"
    )

    info.pack(
        side="bottom",
        pady=20
    )

    return sidebar


# ==========================================================
# CHAT AREA
# ==========================================================

def build_chat_area(parent):

    global chat_box
    global entry_box
    global avatar_label

    content = tk.Frame(
        parent,
        bg=BG_COLOR
    )

    content.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ======================================================
    # TOP BAR
    # ======================================================

    top_bar = tk.Frame(
        content,
        bg=BG_COLOR,
        height=60
    )

    top_bar.pack(
        fill="x"
    )

    top_bar.pack_propagate(
        False
    )

    title = tk.Label(
        top_bar,
        text="Buddy",
        font=(
            "Segoe UI",
            17,
            "bold"
        ),
        fg=TEXT_COLOR,
        bg=BG_COLOR
    )

    title.pack(
        side="left",
        padx=20,
        pady=15
    )

    sub = tk.Label(
        top_bar,
        text="Living Companion",
        font=(
            "Segoe UI",
            9
        ),
        fg=SECONDARY_TEXT,
        bg=BG_COLOR
    )

    sub.pack(
        side="left",
        pady=18
    )

    # ======================================================
    # MAIN AVATAR
    # ======================================================

    avatar_frame = tk.Frame(
        content,
        bg=BG_COLOR,
        height=175
    )

    avatar_frame.pack(
        fill="x"
    )

    avatar_frame.pack_propagate(
        False
    )

    avatar_label = tk.Label(
        avatar_frame,
        bg=BG_COLOR
    )

    avatar_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # ======================================================
    # CHAT CONTAINER
    # ======================================================

    chat_container = tk.Frame(
        content,
        bg=BG_COLOR
    )

    chat_container.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=(0, 10)
    )

    chat_box = tk.Text(
        chat_container,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        font=(
            "Segoe UI",
            11
        ),
        relief="flat",
        bd=0,
        wrap="word",
        padx=18,
        pady=12,
        insertbackground=TEXT_COLOR
    )

    chat_box.pack(
        fill="both",
        expand=True
    )

    chat_box.tag_configure(
        "user_name",
        foreground=BLUE_LIGHT,
        font=(
            "Segoe UI",
            10,
            "bold"
        )
    )

    chat_box.tag_configure(
        "buddy_name",
        foreground=GREEN,
        font=(
            "Segoe UI",
            10,
            "bold"
        )
    )

    chat_box.tag_configure(
        "user_message",
        foreground=TEXT_COLOR,
        spacing3=8
    )

    chat_box.tag_configure(
        "buddy_message",
        foreground=TEXT_COLOR,
        spacing3=8
    )

    chat_box.configure(
        state="disabled"
    )

    # ======================================================
    # INPUT AREA
    # ======================================================

    input_frame = tk.Frame(
        content,
        bg=BG_COLOR,
        height=70
    )

    input_frame.pack(
        fill="x",
        padx=18,
        pady=(0, 18)
    )

    input_frame.pack_propagate(
        False
    )

    entry_box = tk.Entry(
        input_frame,
        bg=CARD_LIGHT,
        fg=TEXT_COLOR,
        font=(
            "Segoe UI",
            11
        ),
        relief="flat",
        bd=0,
        insertbackground=TEXT_COLOR
    )

    entry_box.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 8)
    )

    entry_box.bind(
        "<Return>",
        on_enter
    )

    # ======================================================
    # MIC BUTTON
    # ======================================================

    voice_button = tk.Button(
        input_frame,
        text="🎙",
        command=voice_command,
        bg=CARD_LIGHT,
        fg=TEXT_COLOR,
        activebackground=BLUE,
        activeforeground="white",
        relief="flat",
        bd=0,
        font=(
            "Segoe UI Emoji",
            14
        ),
        width=4,
        cursor="hand2"
    )

    voice_button.pack(
        side="left",
        padx=(0, 8)
    )

    # ======================================================
    # SEND BUTTON
    # ======================================================

    send_button = tk.Button(
        input_frame,
        text="Send",
        command=process_message,
        bg=BLUE,
        fg="white",
        activebackground=BLUE_LIGHT,
        activeforeground="white",
        relief="flat",
        bd=0,
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        padx=18,
        cursor="hand2"
    )

    send_button.pack(
        side="right"
    )

    return content


# ==========================================================
# PROACTIVE MESSAGE
# ==========================================================

def proactive_message(message):

    if not message:

        return

    text = str(
        message
    ).strip()

    blocked_phrases = [

        "standby par hoon",
        "standby par h",
        "buddy standby",
        "ready and waiting",
        "ready to help",
        "i am waiting",
        "main wait kar raha",
        "main yahin hoon",
        "main yahan hoon",
        "waiting for you"

    ]

    lower_text = text.lower()

    if any(
        phrase in lower_text
        for phrase in blocked_phrases
    ):

        print(
            "[Proactive] Blocked filler:",
            text
        )

        return

    safe_after(
        0,
        lambda m=text:
        add_chat_message(
            "Buddy",
            m,
            is_user=False
        )
    )

    safe_after(
        0,
        lambda:
        set_avatar_state(
            "happy"
        )
    )

    safe_after(
        100,
        lambda m=text:
        buddy_speak(
            m
        )
    )


# ==========================================================
# DELAYED PROACTIVE START
# ==========================================================

def delayed_proactive_start():

    try:

        set_proactive_callback(
            proactive_message
        )

        start_proactive()

        print(
            "Buddy Proactive Presence Started"
        )

    except Exception as e:

        print(
            "[Proactive] Error:",
            repr(e)
        )


# ==========================================================
# WINDOW CLOSE
# ==========================================================

def on_close():

    try:

        stop_proactive()

    except Exception as e:

        print(
            "[Proactive] Stop Error:",
            repr(e)
        )

    try:

        stop_speaking()

    except Exception:

        pass

    try:

        if root is not None:

            root.destroy()

    except Exception:

        pass


# ==========================================================
# MAIN GUI
# ==========================================================

def open_buddy_gui():

    global root

    root = tk.Tk()

    root.title(
        "Buddy AI"
    )

    root.geometry(
        "1050x720"
    )

    root.minsize(
        850,
        600
    )

    root.configure(
        bg=BG_COLOR
    )

    root.protocol(
        "WM_DELETE_WINDOW",
        on_close
    )

    load_avatar_images()

    main = tk.Frame(
        root,
        bg=BG_COLOR
    )

    main.pack(
        fill="both",
        expand=True
    )

    build_sidebar(
        main
    )

    build_chat_area(
        main
    )

    set_avatar_state(
        "idle"
    )

    add_chat_message(
        "Buddy",
        "Main yahin hoon Sir. Jab zarurat ho bula lena.",
        is_user=False
    )

    avatar_breathing_animation()

    update_clock()

    safe_after(
        60000,
        delayed_proactive_start
    )

    if entry_box is not None:

        entry_box.focus_set()

    update_sound_button()

    root.mainloop()


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    open_buddy_gui()