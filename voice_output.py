import pyttsx3
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

current_assistant = "Assistant"
speech_active = False
speech_lock = threading.Lock()

def set_voice_by_name(name):
    global current_assistant
    current_assistant = name

    voice_map = {
        "anaya": "Microsoft Zira Desktop",
        "ishita": "Microsoft Zira Desktop",
        "isha": "Microsoft Zira Desktop",
        "sakhi": "Microsoft Zira Desktop"
    }

    target = voice_map.get(name.lower())
    for voice in voices:
        if target and target.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

def speak(text):
    global speech_active
    with speech_lock:
        print(f"{current_assistant}: {text}")
        speech_active = True
        engine.say(text)
        engine.runAndWait()
        speech_active = False

def stop_speaking():
    if speech_active:
        engine.stop()
