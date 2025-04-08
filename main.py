# myAI/main.py

import random
import datetime
import json
import signal
import sys
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
            content = f.read()
            chat_log = json.loads(content) if content.strip() else []
    except FileNotFoundError:
        chat_log = []
    chat_log.append({"role": role, "message": message, "timestamp": str(datetime.datetime.now())})
    with open(CHAT_LOG_FILE, 'w') as f:
        json.dump(chat_log, f, indent=2)

# Graceful interrupt handler
def handle_interrupt(signal_received, frame):
    speak("Oh! Looks like you're leaving, Keyur. Take care and talk to you soon 💛")
    log_interaction("assistant", "Session interrupted by user.")
    sys.exit(0)

# Main routine
def main():
    signal.signal(signal.SIGINT, handle_interrupt)
    user_name = "Keyur"

    # GPT-based greeting
    greeting_prompt = f"You are {assistant_name}, a {assistant_tone} voice assistant who talks like a best friend. Greet Keyur in a friendly and emotional way."
    greeting = ask_assistant(greeting_prompt, assistant_name)
    speak(greeting)
    log_interaction("assistant", greeting)

    # Mood check
    mood = track_mood(user_name, assistant_name)
    log_interaction("user", f"Mood: {mood}")

    mood_prompt = f"Keyur is feeling {mood}. Respond supportively as {assistant_name}, and casually ask if he wants to add a task today."
    mood_response = ask_assistant(mood_prompt, assistant_name)
    speak(mood_response)
    log_interaction("assistant", mood_response)

    # User response to task suggestion
    choice = input("Add task? (yes/no): ").strip().lower()
    log_interaction("user", f"Task Add Choice: {choice}")

    if choice == "yes":
        ask_task_prompt = f"As {assistant_name}, ask Keyur to tell you the task he wants to remember in a fun or friendly way."
        speak(ask_assistant(ask_task_prompt, assistant_name))

        task = input("Your task: ")
        log_interaction("user", f"Task Added: {task}")
        result = add_task(task)
        speak(result)
        log_interaction("assistant", result)

    # Task recap
    task_summary_prompt = f"As {assistant_name}, list Keyur's tasks for today in a cheerful and supportive tone."
    tasks = list_tasks()
    if tasks:
        speak(ask_assistant(task_summary_prompt, assistant_name))
        for t in tasks:
            speak(f"- {t}")
            log_interaction("assistant", f"Task: {t}")
    else:
        no_task_prompt = f"As {assistant_name}, say something fun or casual to let Keyur know he has no tasks today."
        speak(ask_assistant(no_task_prompt, assistant_name))
        log_interaction("assistant", "You have no tasks for today.")

    # Daily summary
    summary_prompt = f"Summarize today's interaction warmly, considering that Keyur felt {mood} and talked to you, {assistant_name}."
    speak(ask_assistant(summary_prompt, assistant_name))
    log_interaction("assistant", "Summary delivered.")

if __name__ == "__main__":
    main()
    # Graceful exit
    speak("Goodbye, Keyur! Remember, I'm always here for you. Take care!")
    log_interaction("assistant", "Goodbye message delivered.")  