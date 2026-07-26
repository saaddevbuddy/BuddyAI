import tkinter as tk
from tkinter import scrolledtext
from commands import handle_command
from main import speak
from voice import speak
from voice import speak, listen
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

    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"\n👤 Saad: {message}\n")
    
    reply = handle_command(message, speak)
    chat_box.insert(tk.END, f"🤖 Buddy: {reply}\n")
    status.config(text="Status: Ready")
    chat_box.see(tk.END)
    chat_box.config(state="disabled")

    input_box.delete(0, tk.END)
root = tk.Tk()
root.title("Buddy AI")
root.geometry("700x650")
title = tk.Label(root, text="🤖 Buddy AI", font=("Arial", 22, "bold"))
title.pack(pady=20)
status = tk.Label(root, text="Status: Ready", font=("Arial", 12))
status.pack()
chat_box = scrolledtext.ScrolledText(root, width=70, height=18)
chat_box.pack(pady=10)
chat_box.insert(tk.END, "🤖 Buddy: Assalam-o-Alaikum Muhammad Saad!\n")
chat_box.insert(tk.END, "🤖 Buddy: Welcome to Buddy AI.\n")
chat_box.config(state="disabled")
mic_button = tk.Button(
    root,
    text="🎤 Speak",
    font=("Arial", 12),
    command=voice_command
)
mic_button.pack(pady=10)
input_box = tk.Entry(root, font=("Arial", 12), width=50)
input_box.pack(pady=5)
send_button = tk.Button(
    root,
    text="Send",
    font=("Arial", 12),
    command=send_message
)
send_button.pack(pady=5)

root.mainloop()