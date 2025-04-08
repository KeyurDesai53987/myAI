import random
import datetime
import json
import pyttsx3

# Available assistant personalities
ASSISTANT_NAMES = ["Anaya", "Ishita", "Isha", "Sakhi"]

# Current assistant name (you can change this for testing)
assistant_name = random.choice(ASSISTANT_NAMES)

# Initialize text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    print(f"{assistant_name}: {text}")
    engine.say(text)
    engine.runAndWait()

# Mood tracker
MOOD_FILE = "data/moods.json"
def track_mood(user_name):
    speak(f"Hey {user_name}, how are you feeling today?")
    mood = input("Your mood: ").strip()
    today = str(datetime.date.today())

    try:
        with open(MOOD_FILE, 'r') as f:
            mood_data = json.load(f)
    except FileNotFoundError:
        mood_data = {}

    mood_data[today] = mood
    with open(MOOD_FILE, 'w') as f:
        json.dump(mood_data, f, indent=2)

    if mood.lower() in ['sad', 'low', 'tired']:
        speak("I'm really sorry you're feeling that way. Want a motivational quote, or should I play your favorite music?")
    elif mood.lower() in ['happy', 'good', 'great']:
        speak("That's amazing! Let's keep the positive vibes going!")
    else:
        speak("Got it. I'm always here for you, no matter how you're feeling.")

# Main routine
def main():
    user_name = "Keyur"
    speak(f"Hi {user_name}, I'm {assistant_name}, your personal buddy. Let's make today a little better together.")
    track_mood(user_name)

if __name__ == "__main__":
    main()
