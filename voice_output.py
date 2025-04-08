# myAI/voice_output.py

import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Assign voice by name or fallback
def set_voice_by_name(name):
    name = name.lower()
    matched = {
        "anaya": "female",
        "ishita": "female",
        "isha": "female",
        "sakhi": "female"
    }
    for voice in voices:
        if matched.get(name, "") in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

# Speak a message aloud and print to console
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
