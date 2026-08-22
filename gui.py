# ==========================================================
# Buddy AI - Desktop Companion GUI
# Login + Living Companion Edition
# ==========================================================

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import datetime
import time

from modules.router import route
from voice import speak as real_speak
from voice import listen

from modules.buddy_mood import get_buddy_mood

from modules.proactive import (
    start_proactive,
    stop_proactive,
    register_activity,
    set_proactive_callback
)

from modules.login_system import (
    account_exists,
    create_account,
    verify_login,
    should_auto_login,
    logout,
    get_user_name
)


# ==========================================================
# ROOT
# ==========================================================

root = tk.Tk()

root.title("Buddy AI")

root.configure(
    bg="#EEF6FF"
)

root.attributes(
    "-topmost",
    True
)


# ==========================================================
# COLORS
# ==========================================================

BG = "#EEF6FF"
TOP = "#D7E9FA"

WHITE = "#FFFFFF"
CHAT = "#F8FBFF"

TEXT = "#243447"
MUTED = "#718096"

BLUE = "#4A90E2"
BLUE_HOVER = "#357ABD"

GREEN = "#22A06B"
GREEN_BG = "#E3F8EE"

PURPLE = "#7C5CFC"

PINK = "#E96B8A"
PINK_BG = "#FDEBF0"

BORDER = "#CFE0F0"

DARK_BLUE = "#245B8F"


# ==========================================================
# GLOBAL STATE
# ==========================================================

processing = False

voice_processing = False

proactive_enabled = True

is_maximized = False

normal_geometry = None

drag_x = 0
drag_y = 0

last_gui_reply = ""
last_gui_reply_time = 0

buddy_started_at = time.time()


# ==========================================================
# WINDOW SIZE
# ==========================================================

WIDTH = 470
HEIGHT = 850


# ==========================================================
# WINDOW MOVEMENT
# ==========================================================

def start_drag(event):

    global drag_x
    global drag_y

    if not is_maximized:

        drag_x = (
            event.x_root -
            root.winfo_x()
        )

        drag_y = (
            event.y_root -
            root.winfo_y()
        )


def drag_window(event):

    if not is_maximized:

        new_x = (
            event.x_root -
            drag_x
        )

        new_y = (
            event.y_root -
            drag_y
        )

        root.geometry(
            f"{root.winfo_width()}x"
            f"{root.winfo_height()}+"
            f"{new_x}+"
            f"{new_y}"
        )


# ==========================================================
# WINDOW CONTROLS
# ==========================================================

def minimize_buddy():

    root.iconify()


def toggle_maximize():

    global is_maximized
    global normal_geometry

    if not is_maximized:

        normal_geometry = root.geometry()

        root.geometry(
            f"{root.winfo_screenwidth()}x"
            f"{root.winfo_screenheight()}+0+0"
        )

        maximize_button.config(
            text="❐"
        )

        is_maximized = True

    else:

        if normal_geometry:

            root.geometry(
                normal_geometry
            )

        maximize_button.config(
            text="□"
        )

        is_maximized = False


# ==========================================================
# CLOSE
# ==========================================================

def close_buddy():

    try:

        stop_proactive()

    except Exception:
        pass

    root.destroy()


# ==========================================================
# LOGIN VARIABLES
# ==========================================================

login_frame = None

login_username = None
login_password = None

create_name = None
create_username = None
create_password = None
create_confirm = None


# ==========================================================
# LOGIN SCREEN
# ==========================================================

def clear_root():

    for widget in root.winfo_children():

        widget.destroy()


# ==========================================================
# LOGIN TITLE
# ==========================================================

def create_login_screen():

    global login_frame
    global login_username
    global login_password

    clear_root()

    root.geometry(
        "430x620"
    )

    root.resizable(
        False,
        False
    )

    root.attributes(
        "-topmost",
        True
    )

    login_frame = tk.Frame(
        root,
        bg=BG
    )

    login_frame.pack(
        fill="both",
        expand=True
    )

    # ------------------------------------------------------
    # Avatar
    # ------------------------------------------------------

    tk.Label(
        login_frame,
        text="🤖",
        font=(
            "Segoe UI Emoji",
            70
        ),
        bg=BG
    ).pack(
        pady=(35, 5)
    )

    tk.Label(
        login_frame,
        text="Buddy AI",
        font=(
            "Segoe UI",
            24,
            "bold"
        ),
        bg=BG,
        fg=TEXT
    ).pack()

    tk.Label(
        login_frame,
        text="Welcome back, Sir ❤️",
        font=(
            "Segoe UI",
            11
        ),
        bg=BG,
        fg=MUTED
    ).pack(
        pady=(3, 25)
    )

    # ------------------------------------------------------
    # Username
    # ------------------------------------------------------

    tk.Label(
        login_frame,
        text="👤 Username",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=45
    )

    login_username = tk.Entry(
        login_frame,
        font=(
            "Segoe UI",
            11
        ),
        bg=WHITE,
        fg=TEXT,
        bd=0,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE
    )

    login_username.pack(
        fill="x",
        padx=45,
        ipady=10,
        pady=(4, 15)
    )

    # ------------------------------------------------------
    # Password
    # ------------------------------------------------------

    tk.Label(
        login_frame,
        text="🔑 Password",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=45
    )

    login_password = tk.Entry(
        login_frame,
        font=(
            "Segoe UI",
            11
        ),
        bg=WHITE,
        fg=TEXT,
        bd=0,
        relief="flat",
        show="●",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE
    )

    login_password.pack(
        fill="x",
        padx=45,
        ipady=10,
        pady=(4, 22)
    )

    # ------------------------------------------------------
    # Login Button
    # ------------------------------------------------------

    tk.Button(
        login_frame,
        text="🔐  LOGIN",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_HOVER,
        activeforeground="white",
        bd=0,
        padx=30,
        pady=11,
        cursor="hand2",
        command=perform_login
    ).pack(
        fill="x",
        padx=45
    )

    # ------------------------------------------------------
    # Create Account
    # ------------------------------------------------------

    tk.Button(
        login_frame,
        text="✨ Create New Buddy Account",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=BG,
        fg=PURPLE,
        activebackground=BG,
        activeforeground=BLUE,
        bd=0,
        cursor="hand2",
        command=create_account_screen
    ).pack(
        pady=20
    )

    tk.Label(
        login_frame,
        text="🔒 Your Buddy account stays on this PC.",
        font=(
            "Segoe UI",
            8
        ),
        bg=BG,
        fg=MUTED
    ).pack(
        pady=5
    )

    login_username.focus_set()

    login_password.bind(
        "<Return>",
        lambda event: perform_login()
    )


# ==========================================================
# CREATE ACCOUNT SCREEN
# ==========================================================

def create_account_screen():

    global create_name
    global create_username
    global create_password
    global create_confirm

    clear_root()

    root.geometry(
        "430x720"
    )

    root.resizable(
        False,
        False
    )

    frame = tk.Frame(
        root,
        bg=BG
    )

    frame.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        frame,
        text="🤖",
        font=(
            "Segoe UI Emoji",
            55
        ),
        bg=BG
    ).pack(
        pady=(20, 0)
    )

    tk.Label(
        frame,
        text="Create Buddy Account",
        font=(
            "Segoe UI",
            21,
            "bold"
        ),
        bg=BG,
        fg=TEXT
    ).pack()

    tk.Label(
        frame,
        text="Sir, pehli dafa Buddy setup karte hain ❤️",
        font=(
            "Segoe UI",
            10
        ),
        bg=BG,
        fg=MUTED
    ).pack(
        pady=(3, 20)
    )

    # ------------------------------------------------------
    # FIELD HELPER
    # ------------------------------------------------------

    def field(
        title,
        show=None
    ):

        tk.Label(
            frame,
            text=title,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=BG,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=45
        )

        entry = tk.Entry(
            frame,
            font=(
                "Segoe UI",
                10
            ),
            bg=WHITE,
            fg=TEXT,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE,
            show=show if show else ""
        )

        entry.pack(
            fill="x",
            padx=45,
            ipady=9,
            pady=(4, 12)
        )

        return entry

    # ------------------------------------------------------
    # Fields
    # ------------------------------------------------------

    create_name = field(
        "👤 Your Name"
    )

    create_username = field(
        "🪪 Username"
    )

    create_password = field(
        "🔑 Password",
        "●"
    )

    create_confirm = field(
        "🔐 Confirm Password",
        "●"
    )

    # ------------------------------------------------------
    # Create Button
    # ------------------------------------------------------

    tk.Button(
        frame,
        text="✨  CREATE ACCOUNT",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_HOVER,
        activeforeground="white",
        bd=0,
        padx=25,
        pady=11,
        cursor="hand2",
        command=perform_create_account
    ).pack(
        fill="x",
        padx=45,
        pady=(8, 10)
    )

    # ------------------------------------------------------
    # Back
    # ------------------------------------------------------

    tk.Button(
        frame,
        text="← Back to Login",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=BG,
        fg=MUTED,
        activebackground=BG,
        activeforeground=TEXT,
        bd=0,
        cursor="hand2",
        command=create_login_screen
    ).pack()

    create_name.focus_set()


# ==========================================================
# CREATE ACCOUNT
# ==========================================================

def perform_create_account():

    name = create_name.get().strip()
    username = create_username.get().strip()
    password = create_password.get()
    confirm = create_confirm.get()

    if not name:

        messagebox.showwarning(
            "Buddy AI",
            "Sir, apna naam enter karein."
        )

        create_name.focus_set()

        return

    if not username:

        messagebox.showwarning(
            "Buddy AI",
            "Username enter karein."
        )

        create_username.focus_set()

        return

    if not password:

        messagebox.showwarning(
            "Buddy AI",
            "Password enter karein."
        )

        create_password.focus_set()

        return

    if password != confirm:

        messagebox.showerror(
            "Buddy AI",
            "Dono passwords same nahi hain."
        )

        create_confirm.focus_set()

        return

    success, message = create_account(
        name,
        username,
        password
    )

    if success:

        messagebox.showinfo(
            "Buddy AI",
            "Account create ho gaya! 🎉\n\n"
            "Welcome to Buddy AI, "
            + name
            + " ❤️"
        )

        open_buddy_gui()

    else:

        messagebox.showerror(
            "Buddy AI",
            message
        )


# ==========================================================
# LOGIN
# ==========================================================

def perform_login():

    username = login_username.get().strip()
    password = login_password.get()

    if not username:

        messagebox.showwarning(
            "Buddy AI",
            "Username enter karein."
        )

        return

    if not password:

        messagebox.showwarning(
            "Buddy AI",
            "Password enter karein."
        )

        return

    success, message = verify_login(
        username,
        password
    )

    if success:

        open_buddy_gui()

    else:

        messagebox.showerror(
            "Login Failed",
            message
        )

        login_password.delete(
            0,
            tk.END
        )

        login_password.focus_set()


# ==========================================================
# LOGOUT
# ==========================================================

def perform_logout():

    global proactive_enabled

    answer = messagebox.askyesno(
        "Logout",
        "Sir, kya aap Buddy se logout karna chahte hain?"
    )

    if not answer:

        return

    proactive_enabled = False

    try:

        stop_proactive()

    except Exception:
        pass

    logout()

    create_login_screen()


# ==========================================================
# GUI HELPERS
# ==========================================================

def update_status(
    text,
    emoji="🟢"
):

    root.after(
        0,
        lambda: status_label.config(
            text=f"{emoji} {text}"
        )
    )


def set_mood(text):

    root.after(
        0,
        lambda: mood_label.config(
            text=text
        )
    )


# ==========================================================
# CLOCK
# ==========================================================

def update_clock():

    current_time = datetime.datetime.now().strftime(
        "%I:%M:%S %p"
    )

    clock_label.config(
        text=f"🕐 {current_time}"
    )

    root.after(
        1000,
        update_clock
    )


# ==========================================================
# UPTIME
# ==========================================================

def update_uptime():

    elapsed = int(
        time.time()
        -
        buddy_started_at
    )

    hours = elapsed // 3600

    minutes = (
        elapsed % 3600
    ) // 60

    seconds = (
        elapsed % 60
    )

    uptime_label.config(
        text=(
            f"⚡ Online "
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )
    )

    root.after(
        1000,
        update_uptime
    )


# ==========================================================
# BIRTHDAY
# ==========================================================

def update_birthday():

    now = datetime.datetime.now()

    birthday = datetime.datetime(
        now.year,
        8,
        24,
        0,
        0,
        0
    )

    if now >= birthday:

        birthday = datetime.datetime(
            now.year + 1,
            8,
            24,
            0,
            0,
            0
        )

    remaining = birthday - now

    days = remaining.days

    hours = (
        remaining.seconds // 3600
    )

    minutes = (
        remaining.seconds % 3600
    ) // 60

    if days == 0:

        birthday_label.config(
            text="🎂 HAPPY BIRTHDAY SIR! 🎉"
        )

    elif days <= 7:

        birthday_label.config(
            text=(
                f"🔥 Birthday incoming! "
                f"{days}d {hours}h {minutes}m"
            )
        )

    else:

        birthday_label.config(
            text=(
                f"🎁 Birthday Countdown: "
                f"{days}d {hours}h {minutes}m"
            )
        )

    root.after(
        30000,
        update_birthday
    )


# ==========================================================
# CHAT
# ==========================================================

def add_chat(
    sender,
    message
):

    if message is None:
        return

    message = str(
        message
    ).strip()

    if not message:
        return

    def write():

        try:

            chat_box.config(
                state="normal"
            )

            chat_box.insert(
                tk.END,
                f"{sender}: {message}\n\n"
            )

            chat_box.config(
                state="disabled"
            )

            chat_box.see(
                tk.END
            )

        except Exception as e:

            print(
                "Chat Write Error:",
                repr(e)
            )

    root.after(
        0,
        write
    )


# ==========================================================
# SPEAK
# ==========================================================

def speak_async(text):

    if not text:
        return

    try:

        threading.Thread(
            target=real_speak,
            args=(text,),
            daemon=True
        ).start()

    except Exception as e:

        print(
            "Speech Error:",
            repr(e)
        )


# ==========================================================
# BUDDY SPEAK
# ==========================================================

def buddy_speak(text):

    global last_gui_reply
    global last_gui_reply_time

    if text is None:
        return

    text = str(
        text
    ).strip()

    if not text:
        return

    last_gui_reply = text

    last_gui_reply_time = time.time()

    add_chat(
        "🤖 Buddy",
        text
    )

    speak_async(
        text
    )


# ==========================================================
# PROACTIVE
# ==========================================================

def proactive_message(text):

    global processing

    if not proactive_enabled:
        return

    if processing:
        return

    if voice_processing:
        return

    if not text:
        return

    text = str(
        text
    ).strip()

    if not text:
        return

    add_chat(
        "💭 Buddy",
        text
    )

    speak_async(
        text
    )


# ==========================================================
# BUDDY MOOD
# ==========================================================

def update_buddy_mood():

    try:

        mood_data = get_buddy_mood()

        mood = mood_data.get(
            "mood",
            "normal"
        )

        intensity = mood_data.get(
            "intensity",
            0
        )

        mood_map = {

            "normal": (
                "🤖",
                "Normal"
            ),

            "happy": (
                "😊",
                "Happy"
            ),

            "excited": (
                "🤩",
                "Excited"
            ),

            "annoyed": (
                "😒",
                "Annoyed"
            ),

            "angry": (
                "😠",
                "Angry"
            ),

            "sad": (
                "😔",
                "Sad"
            ),

            "tired": (
                "😴",
                "Tired"
            )
        }

        emoji, mood_name = mood_map.get(
            mood,
            (
                "🤖",
                "Normal"
            )
        )

        avatar.config(
            text=emoji
        )

        mood_label.config(
            text=(
                f"{mood_name} • "
                f"Intensity {intensity}%"
            )
        )

    except Exception as e:

        print(
            "Mood GUI Error:",
            repr(e)
        )

        avatar.config(
            text="🤖"
        )

        mood_label.config(
            text="Normal • Ready to chat"
        )

    root.after(
        1500,
        update_buddy_mood
    )


# ==========================================================
# IDLE AVATAR
# ==========================================================

def buddy_idle_animation():

    if not processing:

        pulse = [
            "🤖",
            "🤖",
            "👀",
            "🤖"
        ]

        index = int(
            time.time() * 2
        ) % len(pulse)

        avatar.config(
            text=pulse[index]
        )

    root.after(
        700,
        buddy_idle_animation
    )


# ==========================================================
# GUI STATES
# ==========================================================

def show_thinking():

    update_status(
        "Thinking...",
        "🤔"
    )

    set_mood(
        "🧠 Thinking • Processing..."
    )


def show_listening():

    update_status(
        "Listening...",
        "🎙️"
    )

    set_mood(
        "🎙️ Listening • Sun raha hoon..."
    )


def show_ready():

    update_status(
        "Ready",
        "🟢"
    )


# ==========================================================
# PROCESS MESSAGE
# ==========================================================

def process_message(message):

    global processing
    global last_gui_reply
    global last_gui_reply_time

    try:

        print(
            "\n========== GUI ROUTER =========="
        )

        print(
            "User:",
            message
        )

        reply = route(
            message,
            buddy_speak
        )

        print(
            "GUI ROUTER RETURN:",
            repr(reply)
        )

        if reply is not None:

            reply_text = str(
                reply
            ).strip()

            if reply_text:

                current_time = time.time()

                duplicate = (
                    reply_text ==
                    last_gui_reply
                    and
                    current_time -
                    last_gui_reply_time < 2
                )

                if not duplicate:

                    add_chat(
                        "🤖 Buddy",
                        reply_text
                    )

                    last_gui_reply = reply_text

                    last_gui_reply_time = current_time

                    speak_async(
                        reply_text
                    )

    except Exception as e:

        print(
            "Buddy GUI Error:",
            repr(e)
        )

        add_chat(
            "🤖 Buddy",
            "Sir, process karte waqt masla aa gaya."
        )

    finally:

        processing = False

        show_ready()


# ==========================================================
# SEND
# ==========================================================

def send_message():

    global processing

    if processing:
        return

    message = input_box.get().strip()

    if not message:
        return

    register_activity()

    input_box.delete(
        0,
        tk.END
    )

    add_chat(
        "👤 Saad",
        message
    )

    processing = True

    show_thinking()

    threading.Thread(
        target=process_message,
        args=(message,),
        daemon=True
    ).start()


# ==========================================================
# PROCESS VOICE
# ==========================================================

def process_voice():

    global processing
    global voice_processing
    global last_gui_reply
    global last_gui_reply_time

    try:

        voice_processing = True

        message = listen()

        if not message:

            return

        register_activity()

        add_chat(
            "👤 Saad",
            message
        )

        show_thinking()

        reply = route(
            message,
            buddy_speak
        )

        print(
            "GUI VOICE RETURN:",
            repr(reply)
        )

        if reply:

            reply_text = str(
                reply
            ).strip()

            current_time = time.time()

            duplicate = (
                reply_text ==
                last_gui_reply
                and
                current_time -
                last_gui_reply_time < 2
            )

            if not duplicate:

                add_chat(
                    "🤖 Buddy",
                    reply_text
                )

                last_gui_reply = reply_text

                last_gui_reply_time = current_time

                speak_async(
                    reply_text
                )

    except Exception as e:

        print(
            "Voice Error:",
            repr(e)
        )

        add_chat(
            "🤖 Buddy",
            "Sir, voice process mein masla aa gaya."
        )

    finally:

        voice_processing = False

        processing = False

        show_ready()

        root.after(
            0,
            lambda: mic_button.config(
                state="normal"
            )
        )


# ==========================================================
# VOICE COMMAND
# ==========================================================

def voice_command():

    global processing

    if processing:
        return

    processing = True

    mic_button.config(
        state="disabled"
    )

    show_listening()

    threading.Thread(
        target=process_voice,
        daemon=True
    ).start()


# ==========================================================
# CLEAR CHAT
# ==========================================================

def clear_chat():

    chat_box.config(
        state="normal"
    )

    chat_box.delete(
        "1.0",
        tk.END
    )

    chat_box.insert(
        tk.END,
        "🤖 Buddy: Chat clear kar di Sir.\n\n"
    )

    chat_box.insert(
        tk.END,
        "🤖 Buddy: Ab fresh start karte hain. 😎\n"
    )

    chat_box.config(
        state="disabled"
    )


# ==========================================================
# BUDDY GUI
# ==========================================================

def open_buddy_gui():

    global proactive_enabled
    global top_bar
    global maximize_button

    proactive_enabled = True

    clear_root()

    root.resizable(
        True,
        True
    )

    screen_width = root.winfo_screenwidth()

    screen_height = root.winfo_screenheight()

    x = screen_width - WIDTH - 25

    y = screen_height - HEIGHT - 55

    root.geometry(
        f"{WIDTH}x{HEIGHT}+{x}+{y}"
    )

    # ======================================================
    # TOP BAR
    # ======================================================

    top_bar = tk.Frame(
        root,
        bg=TOP,
        height=50
    )

    top_bar.pack(
        fill="x"
    )

    top_bar.pack_propagate(
        False
    )

    top_bar.bind(
        "<Button-1>",
        start_drag
    )

    top_bar.bind(
        "<B1-Motion>",
        drag_window
    )

    title = tk.Label(
        top_bar,
        text="🤖  Buddy AI",
        font=(
            "Segoe UI",
            14,
            "bold"
        ),
        bg=TOP,
        fg=TEXT
    )

    title.pack(
        side="left",
        padx=14
    )

    title.bind(
        "<Button-1>",
        start_drag
    )

    title.bind(
        "<B1-Motion>",
        drag_window
    )

    # ======================================================
    # WINDOW BUTTONS
    # ======================================================

    window_buttons = tk.Frame(
        top_bar,
        bg=TOP
    )

    window_buttons.pack(
        side="right",
        padx=5
    )

    tk.Button(
        window_buttons,
        text="—",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=TOP,
        fg=MUTED,
        activebackground=TOP,
        activeforeground=TEXT,
        bd=0,
        width=3,
        command=minimize_buddy,
        cursor="hand2"
    ).pack(
        side="left"
    )

    maximize_button = tk.Button(
        window_buttons,
        text="□",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=TOP,
        fg=MUTED,
        activebackground=TOP,
        activeforeground=TEXT,
        bd=0,
        width=3,
        command=toggle_maximize,
        cursor="hand2"
    )

    maximize_button.pack(
        side="left"
    )

    tk.Button(
        window_buttons,
        text="✕",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=TOP,
        fg=PINK,
        activebackground=TOP,
        activeforeground=PINK,
        bd=0,
        width=3,
        command=close_buddy,
        cursor="hand2"
    ).pack(
        side="left"
    )

    # ======================================================
    # AVATAR CARD
    # ======================================================

    avatar_card = tk.Frame(
        root,
        bg=WHITE,
        height=205,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    avatar_card.pack(
        fill="x",
        padx=10,
        pady=10
    )

    avatar_card.pack_propagate(
        False
    )

    global avatar
    global mood_label
    global birthday_label
    global uptime_label

    avatar = tk.Label(
        avatar_card,
        text="🤖",
        font=(
            "Segoe UI Emoji",
            70
        ),
        bg=WHITE,
        fg=TEXT
    )

    avatar.pack(
        pady=(5, 0)
    )

    mood_label = tk.Label(
        avatar_card,
        text="Normal • Ready to chat",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=WHITE,
        fg=PURPLE
    )

    mood_label.pack()

    birthday_label = tk.Label(
        avatar_card,
        text="🎁 Birthday Countdown...",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=WHITE,
        fg=PINK
    )

    birthday_label.pack(
        pady=(7, 0)
    )

    uptime_label = tk.Label(
        avatar_card,
        text="⚡ Online 00:00:00",
        font=(
            "Segoe UI",
            8
        ),
        bg=WHITE,
        fg=MUTED
    )

    uptime_label.pack(
        pady=(4, 0)
    )

    # ======================================================
    # STATUS ROW
    # ======================================================

    status_row = tk.Frame(
        root,
        bg=BG
    )

    status_row.pack(
        fill="x",
        padx=16,
        pady=(0, 7)
    )

    global status_label
    global clock_label

    status_label = tk.Label(
        status_row,
        text="🟢 Ready",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=BG,
        fg=GREEN
    )

    status_label.pack(
        side="left"
    )

    clock_label = tk.Label(
        status_row,
        text="🕐 --:--:--",
        font=(
            "Segoe UI",
            9
        ),
        bg=BG,
        fg=MUTED
    )

    clock_label.pack(
        side="right"
    )

    # ======================================================
    # CHAT CARD
    # ======================================================

    chat_card = tk.Frame(
        root,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    chat_card.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0, 8)
    )

    global chat_box

    chat_box = scrolledtext.ScrolledText(
        chat_card,
        bg=CHAT,
        fg=TEXT,
        insertbackground=TEXT,
        selectbackground="#CFE5FA",
        selectforeground=TEXT,
        font=(
            "Segoe UI",
            10
        ),
        bd=0,
        relief="flat",
        wrap="word",
        padx=12,
        pady=10
    )

    chat_box.pack(
        fill="both",
        expand=True,
        padx=2,
        pady=2
    )

    # ======================================================
    # WELCOME
    # ======================================================

    username = get_user_name()

    if not username:
        username = "Sir"

    chat_box.insert(
        tk.END,
        f"🤖 Buddy: Assalam-o-Alaikum {username}! ❤️\n\n"
    )

    chat_box.insert(
        tk.END,
        "🤖 Buddy: Main ready hoon. 😎\n\n"
    )

    chat_box.insert(
        tk.END,
        "🎁 Buddy: Birthday countdown active hai! 🎉\n\n"
    )

    chat_box.insert(
        tk.END,
        "⚡ Buddy: Living Companion Mode ON.\n\n"
    )

    chat_box.insert(
        tk.END,
        "💡 Buddy: Neeche message likhein ya Voice dabayein.\n\n"
    )

    chat_box.insert(
        tk.END,
        "🟢 Buddy: Main aapke sawal ka jawab dete waqt random proactive messages nahi bhejunga. 😎\n"
    )

    chat_box.config(
        state="disabled"
    )

    # ======================================================
    # INPUT TITLE
    # ======================================================

    tk.Label(
        root,
        text="💬  Message Buddy",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=12,
        pady=(0, 4)
    )

    # ======================================================
    # INPUT ROW
    # ======================================================

    input_row = tk.Frame(
        root,
        bg=BG
    )

    input_row.pack(
        fill="x",
        padx=10,
        pady=(0, 7)
    )

    global input_box

    input_box = tk.Entry(
        input_row,
        font=(
            "Segoe UI",
            10
        ),
        bg=WHITE,
        fg=TEXT,
        insertbackground=TEXT,
        bd=0,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE
    )

    input_box.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=11,
        padx=(0, 7)
    )

    tk.Button(
        input_row,
        text="➤ SEND",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_HOVER,
        activeforeground="white",
        bd=0,
        padx=12,
        pady=9,
        command=send_message,
        cursor="hand2"
    ).pack(
        side="right"
    )

    # ======================================================
    # ACTION BAR
    # ======================================================

    action_bar = tk.Frame(
        root,
        bg=BG
    )

    action_bar.pack(
        fill="x",
        padx=10,
        pady=(0, 8)
    )

    global mic_button

    mic_button = tk.Button(
        action_bar,
        text="🎤  VOICE",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=GREEN_BG,
        fg="#16845A",
        activebackground="#C9F0DE",
        activeforeground="#126B49",
        bd=0,
        padx=28,
        pady=9,
        command=voice_command,
        cursor="hand2"
    )

    mic_button.pack(
        side="left"
    )

    tk.Button(
        action_bar,
        text="🗑  CLEAR CHAT",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=PINK_BG,
        fg="#C44E66",
        activebackground="#F8DCE3",
        activeforeground="#A83E55",
        bd=0,
        padx=20,
        pady=9,
        command=clear_chat,
        cursor="hand2"
    ).pack(
        side="left",
        padx=(7, 0)
    )

    # ======================================================
    # LOGOUT
    # ======================================================

    tk.Button(
        action_bar,
        text="🚪 LOGOUT",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg="#F1F3F5",
        fg=MUTED,
        activebackground="#E2E6EA",
        activeforeground=TEXT,
        bd=0,
        padx=13,
        pady=9,
        command=perform_logout,
        cursor="hand2"
    ).pack(
        side="right"
    )

    # ======================================================
    # BOTTOM
    # ======================================================

    tk.Label(
        root,
        text=(
            "🎤 Voice  •  ➤ Send  •  "
            "🤖 Buddy is listening"
        ),
        font=(
            "Segoe UI",
            8
        ),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=12,
        pady=(0, 8)
    )

    # ======================================================
    # ENTER KEY
    # ======================================================

    input_box.bind(
        "<Return>",
        lambda event: send_message()
    )

    # ======================================================
    # START SYSTEMS
    # ======================================================

    update_clock()

    update_uptime()

    update_birthday()

    update_status(
        "Ready",
        "🟢"
    )

    update_buddy_mood()

    buddy_idle_animation()

    # ======================================================
    # PROACTIVE
    # ======================================================

    set_proactive_callback(
        proactive_message
    )

    start_proactive()

    # ======================================================
    # FOCUS
    # ======================================================

    input_box.focus_set()


# ==========================================================
# SAFE SHUTDOWN
# ==========================================================

def on_closing():

    try:

        stop_proactive()

    except Exception:
        pass

    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    on_closing
)


# ==========================================================
# STARTUP
# ==========================================================

if not account_exists():

    create_account_screen()

elif should_auto_login():

    open_buddy_gui()

else:

    create_login_screen()


# ==========================================================
# MAIN LOOP
# ==========================================================

root.mainloop()