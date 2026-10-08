# ==========================================
# Buddy AI - OpenCode Zen
# Memory Aware AI
# ==========================================

import os
import requests


# ==========================================
# OpenCode Zen Settings
# ==========================================
ZEN_API_KEY = os.getenv("ZEN_API_KEY", "")

ZEN_URL = "https://opencode.ai/zen/v1/chat/completions"

ZEN_MODEL = "mimo-v2.5-free"


# ==========================================
# Ask OpenCode Zen
# ==========================================

def ask_zen_ai(user_message, memory_context=""):

    try:

        if not ZEN_API_KEY:

            print(
                "[Zen] API key missing."
            )

            return None

        # ==================================
        # Buddy Personality + Memory
        # ==================================

        prompt = f"""
Tum Buddy AI ho.

Tum Saad ke personal AI assistant ho.

Rules:

- Hamesha natural Roman Urdu mein jawab do.
- Friendly aur respectful raho.
- Zarurat par "Sir" keh sakte ho.
- User ki baat ko context ke sath samjho.
- Agar memory mein user ki koi relevant information ho,
  usay naturally use karo.
- User ki memory ko dobara unnecessarily mat pucho.
- Bohat lamba jawab mat do jab tak user detail na maange.
- Aisa mat kehna ke tumhein memory nahi hai agar neeche
  memory context diya gaya ho.

==========================================
USER MEMORY
==========================================

{memory_context}

==========================================
CURRENT USER MESSAGE
==========================================

{user_message}

==========================================
RESPONSE
==========================================

Roman Urdu mein natural jawab do.
"""

        headers = {
            "Authorization": f"Bearer {ZEN_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": ZEN_MODEL,

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "temperature": 0.7,
            "max_tokens": 1000
        }

        print(
            "[Zen] Sending request..."
        )

        response = requests.post(
            ZEN_URL,
            headers=headers,
            json=data,
            timeout=30
        )

        print(
            "[Zen] Status:",
            response.status_code
        )

        # ==================================
        # ERROR
        # ==================================

        if response.status_code != 200:

            print(
                "[Zen] Error:",
                response.text
            )

            return None

        # ==================================
        # JSON
        # ==================================

        result = response.json()

        choices = result.get(
            "choices",
            []
        )

        if not choices:

            print(
                "[Zen] No choices returned."
            )

            return None

        message = choices[0].get(
            "message",
            {}
        )

        content = message.get(
            "content"
        )

        if not content:

            print(
                "[Zen] Empty response."
            )

            return None

        return str(
            content
        ).strip()

    except requests.exceptions.Timeout:

        print(
            "[Zen] Request timed out."
        )

        return None

    except requests.exceptions.RequestException as e:

        print(
            "[Zen] Network error:",
            repr(e)
        )

        return None

    except Exception as e:

        print(
            "[Zen] Unexpected error:",
            repr(e)
        )

        return None