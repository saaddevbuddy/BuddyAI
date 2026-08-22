# ==========================================
# Buddy AI - AI Status
# ==========================================

from google import genai
from config import GEMINI_API_KEY, MODEL_NAME


def check_ai_status():

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents="Reply with only: OK"
        )

        if response.text:
            return True

        return False

    except Exception as e:

        print("AI Status Error:", e)

        return False