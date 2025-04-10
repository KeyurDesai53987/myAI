# smart_features.py
# This module contains functions to detect the mood of a user based on their input.

def detect_mood_with_llm(user_input: str, llm) -> str:
    prompt = (
        "Based on the message below, identify the user's emotional tone in one or two words. "
        "Be honest and avoid guessing. If unclear, respond 'neutral'.\n\n"
        f"Message: \"{user_input}\"\n\nMood:"
    )

    result = llm(
        prompt=prompt,
        temperature=0.3,
        max_tokens=10,
        stop=["\n", "</s>"],
        stream=False
    )

    mood = result['choices'][0]['text'].strip().lower()
    return mood if mood else 'neutral'
