from pathlib import Path
import os

# ==========================
# Buddy AI Configuration
# ==========================

APP_NAME = "Buddy AI"
VERSION = "2.0.0"

# ==========================
# Base Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

MEMORY_FILE = DATA_DIR / "memory.json"
PROFILE_FILE = DATA_DIR / "profile.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
HISTORY_FILE = DATA_DIR / "history.json"

# ==========================
# Gemini AI
# ==========================

# Put your API key in Windows environment variable:
# GEMINI_API_KEY

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Current stable Gemini model
MODEL_NAME = "gemini-3.6-flash"

# Lightweight fallback model
FALLBACK_MODEL_NAME = "gemini-2.5-flash-lite"

# ==========================
# AI Settings
# ==========================

AI_ENABLED = True
AI_TIMEOUT = 30

# ==========================
# Voice
# ==========================

VOICE_RATE = 170
VOICE_VOLUME = 1.0

# ==========================
# Debug
# ==========================

DEBUG = True