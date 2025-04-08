# myAI/voice_output.py

import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

def list_available_voices():
    for idx, voice in enumerate(voices):
        print(f"{idx}: {voice.name} - {voice.id}")

# Assign voice by name or fallback
def set_voice_by_name(name):
    voice_map = {
        "anaya": "Microsoft Hazel Desktop",   # Example female voice on Windows
        "ishita": "Microsoft Zira Desktop",
        "isha": "Microsoft Hazel Desktop",
        "sakhi": "Microsoft Zira Desktop"
    }
    target = voice_map.get(name.lower())
    for voice in voices:
        if target.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break


# Speak a message aloud and print to console
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
