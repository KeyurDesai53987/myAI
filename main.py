# myAI/main.py

import random
import datetime
import json
from llm_engine import ask_assistant
from voice_output import speak, set_voice_by_name
from mood_tracker import track_mood
from task_manager import add_task, list_tasks

# Load assistant profiles
with open("prompts/assistant_profiles.json", "r") as f:
    assistant_profiles = json.load(f)

# Available assistant personalities
ASSISTANT_NAMES = list(assistant_profiles.keys())
assistant_name = random.choice(ASSISTANT_NAMES)
profile = assistant_profiles[assistant_name]
assistant_tone = profile.get("tone", "friendly")
assistant_style = profile.get("style", "speaks supportively")
assistant_quotes = profile.get("motivational_quotes", [])

# Set voice for selected assistant
set_voice_by_name(assistant_name)

# Log chat interactions
CHAT_LOG_FILE = "data/chat_log.json"
def log_interaction(role, message):
    try:
        with open(CHAT_LOG_FILE, 'r') as f:
            chat_log = json.load(f)
    except FileNotFoundError:
        chat_log = []
    chat_log.append({"role": role, "message": message, "timestamp": str(datetime.datetime.now())})
    with open(CHAT_LOG_FILE, 'w') as f:
        json.dump(chat_log, f, indent=2)

# Main routine
def main():
    user_name = "Keyur"
    greeting = f"Hi {user_name}, I'm {assistant_name}, your {assistant_tone} personal buddy. I usually {assistant_style}"
    speak(greeting)
    log_interaction("assistant", greeting)

    speak("Let's make today a little better together.")
    log_interaction("assistant", "Let's make today a little better together.")

    mood = track_mood(user_name, assistant_name)
    log_interaction("user", f"Mood: {mood}")

    response = ask_assistant(f"User {user_name} is feeling {mood}. What should I say to make them feel supported?", assistant_name)
    speak(response)
    log_interaction("assistant", response)

    # Say a motivational quote if available
    if assistant_quotes:
        quote = random.choice(assistant_quotes)
        speak(f"Also, here's a little something to lift your spirit: {quote}")
        log_interaction("assistant", f"Motivational Quote: {quote}")

    speak("Would you like to add a task for today? (yes/no)")
    choice = input("Add task? ").strip().lower()
    log_interaction("user", f"Task Add Choice: {choice}")

    if choice == "yes":
        speak("Tell me the task you want to add.")
        task = input("Your task: ")
        log_interaction("user", f"Task Added: {task}")
        result = add_task(task)
        speak(result)
        log_interaction("assistant", result)

    speak("Here are your tasks for today:")
    tasks = list_tasks()
    if tasks:
        for t in tasks:
            speak(f"- {t}")
            log_interaction("assistant", f"Task: {t}")
    else:
        speak("You have no tasks for today.")
        log_interaction("assistant", "You have no tasks for today.")

    # Daily summary
    speak("Here's a quick summary of today, Keyur:")
    log_interaction("assistant", "Summary Start")

    # Mood summary
    speak(f"You mentioned feeling {mood} earlier today.")
    log_interaction("assistant", f"Mood Summary: {mood}")

    # Task summary
    if tasks:
        speak("You planned the following tasks:")
        for t in tasks:
            speak(f"- {t}")
    else:
        speak("No tasks were listed today.")
    log_interaction("assistant", "Summary End")


if __name__ == "__main__":
    main()
