# Buddy AI 🤖

Buddy AI is a personal desktop AI companion designed to feel more natural, friendly, and personal than a basic chatbot.

## Features

* Personal AI companion
* Natural Roman Urdu conversation
* Voice input
* AI voice output
* Sound ON/OFF control
* Stop Speaking control
* Clear Chat control
* 2D Buddy avatar
* Mood-aware responses
* Persistent memory
* Notes and reminders
* Web search support
* Multiple AI providers with fallback
* Modern dark GUI
* Windows desktop application

## AI System

Buddy AI uses a fallback-based AI architecture:

```text
Memory
   ↓
Gemini
   ↓
APInex
   ↓
OpenCode Zen
```

If one AI service becomes unavailable, Buddy can try the next available service.

## Voice

Buddy supports voice input and AI voice output.

The voice system is designed for Roman Urdu conversations while keeping the displayed chat text unchanged.

## Requirements

* Windows 10 or later
* Python 3.12+
* Internet connection
* Required Python packages listed in `requirements.txt`

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd BuddyAI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your required API keys as environment variables.

Do not put API keys directly inside the source code.

Then start Buddy:

```bash
python gui.py
```

## Project Structure

```text
BuddyAI/
│
├── assets/
├── data/
├── modules/
├── gui.py
├── voice.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## Privacy

Buddy AI is designed to keep personal information local.

Personal memory, conversation history, profile information, API keys, and temporary generated files should not be uploaded publicly.

Never publish API keys or other private credentials in the repository.

## Status

### v1.0.0

First public release of Buddy AI.

This version focuses on the core Buddy experience:

* AI conversation
* Roman Urdu interaction
* Voice input and output
* 2D avatar
* Mood system
* Persistent memory
* Reminders
* Web search
* Modern dark desktop GUI
* AI fallback system

## Future Plans

Future versions may include:

* More advanced animated avatar
* Real-time lip synchronization
* Improved Roman Urdu voice
* Better web search
* More natural emotional expressions
* Android companion
* Additional AI providers
* More advanced memory
* Better proactive companion features

## Author

Built as a personal AI companion project.

Made with Python ❤️
