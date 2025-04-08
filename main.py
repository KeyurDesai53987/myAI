# my_friend_assistant/main.py

import random
import datetime
from llm_engine import ask_assistant
from voice_output import speak
from mood_tracker import track_mood

# Available assistant personalities
ASSISTANT_NAMES = ["Anaya", "Ishita", "Isha", "Sakhi"]
assistant_name = random.choice(ASSISTANT_NAMES)

# Main routine
def main():
    user_name = "Keyur"
    speak(f"Hi {user_name}, I'm {assistant_name}, your personal buddy. Let's make today a little better together.")
    mood = track_mood(user_name, assistant_name)
    response = ask_assistant(f"User {user_name} is feeling {mood}. What should I say to make them feel supported?", assistant_name)
    speak(response)

if __name__ == "__main__":
    main()
