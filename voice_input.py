import speech_recognition as sr

recognizer = sr.Recognizer()

def listen(prompt=None):
    if prompt:
        print(prompt)

    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)

        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"⚠️ Could not request results; {e}")
            return ""
