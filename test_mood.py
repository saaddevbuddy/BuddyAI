from modules.mood import (
    detect_mood,
    analyze_mood
)


# ==========================================
# Buddy AI - Mood Engine Test
# ==========================================

tests = [
    "aaj bohat khushi ho rahi hai",
    "yar main bohat udaas hoon",
    "ye error baar baar aa raha hai",
    "kal exam ki tension hai",
    "mujhe samajh nahi aa raha",
    "bohat thak gaya hoon",
    "Chrome kholo"
]


print("\n================================")
print("🤖 Buddy AI Mood Engine Test")
print("================================\n")


for text in tests:

    result = analyze_mood(text)

    print(f"👤 Saad: {text}")

    print(
        f"🤖 Mood: {result['emoji']} "
        f"{result['name']}"
    )

    print(
        f"📊 Confidence: "
        f"{result['confidence']}%"
    )

    print(
        f"🔎 Matched: "
        f"{result['matched_words']}"
    )

    print(
        f"🧠 Style: "
        f"{result['style']}"
    )

    print("--------------------------------")


print("\n✅ Mood Engine Test Complete!")