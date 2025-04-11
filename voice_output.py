import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty("rate", 180)

_speak_lock = threading.Lock()
_current_thread = None

def speak(text):
    global _current_thread
    stop_speaking()  # stop previous speech
    def _speak():
        with _speak_lock:
            engine.say(text)
            engine.runAndWait()
    _current_thread = threading.Thread(target=_speak, daemon=True)
    _current_thread.start()

def stop_speaking():
    engine.stop()
    if _current_thread and _current_thread.is_alive():
        try:
            _current_thread.join(timeout=0.1)
        except:
            pass

def set_voice_by_name(name):
    voices = engine.getProperty("voices")
    for voice in voices:
        if name.lower() in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
