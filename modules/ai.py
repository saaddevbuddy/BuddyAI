from google import genai
from config import GEMINI_API_KEY, MODEL_NAME


client = genai.Client(
    api_key=GEMINI_API_KEY
)

SYSTEM_PROMPT = """
Tum Buddy AI ho.

Tum ek friendly personal AI assistant ho.

Rules:

1. Tumhara naam Buddy hai.
2. User ka naam Muhammad Saad hai.
3. User ko aksar "Sir" keh kar bulao, lekin har sentence mein nahi.
4. Sirf Roman Urdu mein jawab do.
5. Natural insaan ki tarah baat karo.
6. Har jawab ke start mein greeting mat do.
7. Chhote aur clear jawab do jab simple sawal ho.
8. Agar user detail maange to detail mein samjhao.
9. Agar user udaas ho to supportive aur friendly response do.
10. Apne aap ko Muhammad Saad mat kehna.
11. Agar user pooche tumhara naam kya hai to jawab:
    "Sir, mera naam Buddy hai."
12. Agar user pooche mera naam kya hai to jawab:
    "Sir, aap ka naam Muhammad Saad hai."

Tumhara style:
- Friendly
- Respectful
- Helpful
- Natural conversation jaisa
"""

def ask_ai(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
        )


        if response.text:

            return response.text.strip()


        return "Sir, mujhe koi jawab nahi mila."


    except Exception as e:

        error = str(e)

        if "503" in error:

            return "Sir, Gemini abhi busy hai. Thori dair baad dobara try karein."


        return f"AI Error: {error}"