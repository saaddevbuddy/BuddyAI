from commands import handle_command
from voice import speak, listen
import tkinter as tk
from tkinter import scrolledtext
import threading
def voice_command():
    status.config(text="Status: Listening...")
    message = listen()

    if message:
        chat_box.config(state="normal")
        chat_box.insert(tk.END, f"\n👤 Saad: {message}\n")
        status.config(text="Status: Thinking...")

        reply = handle_command(message, speak)

        if reply:
            chat_box.insert(tk.END, f"🤖 Buddy: {reply}\n")
            status.config(text="Status: Ready")

        chat_box.config(state="disabled")
        chat_box.see(tk.END)
def send_message():

    message = input_box.get()

    if not message:
        return

    input_box.delete(0, tk.END)

    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"\n👤 Saad: {message}\n")
    chat_box.config(state="disabled")

    status.config(text="Status: Thinking...")


    def process():

        reply = handle_command(message, speak)

        def update():

            chat_box.config(state="normal")
            chat_box.insert(
                tk.END,
                f"🤖 Buddy: {reply}\n"
            )
            chat_box.config(state="disabled")

            chat_box.see(tk.END)

            status.config(
                text="Status: Ready"
            )


        root.after(0, update)


    threading.Thread(
        target=process,
        daemon=True
    ).start()
root = tk.Tk()
root.title("🤖 Buddy AI")
root.geometry("900x700")
root.configure(bg="#1E1E1E")
root.resizable(False, False)
title = tk.Label(
    root,
    text="🤖 Buddy AI",
    font=("Segoe UI", 22, "bold"),
    bg="#1E1E1E",
    fg="white"
)
title.pack(pady=20)
status = tk.Label(
    root,
    text="🟢 Status: Ready",
    font=("Segoe UI", 11),
    bg="#1E1E1E",
    fg="#00FF99"
)
status.pack()
chat_box = scrolledtext.ScrolledText(
    root,
    width=80,
    height=20,
    bg="#252526",
    fg="white",
    insertbackground="white",
    font=("Segoe UI", 11),
    bd=0
)
chat_box.pack(pady=10)
chat_box.insert(tk.END, "🤖 Buddy: Assalam-o-Alaikum Muhammad Saad!\n")
chat_box.insert(tk.END, "🤖 Buddy: Welcome to Buddy AI.\n")
chat_box.config(state="disabled")
mic_button = tk.Button(
    root,
    text="🎤 Voice",
    font=("Segoe UI", 11, "bold"),
    bg="#16A085",
    fg="white",
    activebackground="#13856D",
    activeforeground="white",
    bd=0,
    padx=12,
    pady=8,
    cursor="hand2",
    command=voice_command
)
mic_button.pack(pady=10)
input_box = tk.Entry(
    root,
    font=("Segoe UI", 12),
    width=60,
    bg="#2D2D30",
    fg="white",
    insertbackground="white",
    bd=0
)
input_box.pack(pady=5)
send_button = tk.Button(
    root,
    text="📤 Send",
    font=("Segoe UI", 11, "bold"),
    bg="#007ACC",
    fg="white",
    activebackground="#0060A8",
    activeforeground="white",
    bd=0,
    padx=12,
    pady=8,
    cursor="hand2",
    command=send_message
)
send_button.pack(pady=5)

root.mainloop()