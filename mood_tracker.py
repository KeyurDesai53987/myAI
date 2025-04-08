import json
import datetime

MOOD_FILE = "data/moods.json"

def track_mood(user_name, assistant_name):
    mood = input(f"{assistant_name}: How are you feeling today, {user_name}?\nYour mood: ").strip()
    today = str(datetime.date.today())
    
    try:
        with open(MOOD_FILE, 'r') as f:
            mood_data = json.load(f)
    except FileNotFoundError:
        mood_data = {}

    mood_data[today] = mood
    with open(MOOD_FILE, 'w') as f:
        json.dump(mood_data, f, indent=2)
    
    return mood
