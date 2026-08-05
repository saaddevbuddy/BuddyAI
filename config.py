from pathlib import Path

# ==========================
# Project Information
# ==========================

APP_NAME = "Buddy AI"
VERSION = "1.0.0"

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

GEMINI_API_KEY = "AQ.Ab8RN6ISXd2HIvqBiEdgcGWN0EoI0n1ifmV_O2F1GpAn1af1rg"
MODEL_NAME = "gemini-flash-latest"

# ==========================
# Voice
# ==========================

VOICE_RATE = 170
VOICE_VOLUME = 1.0

# ==========================
# Debug
# ==========================

DEBUG = True