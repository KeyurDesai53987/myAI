import os
import json
import signal
import sys
import threading
import datetime
from llm_engine import ask_assistant
from voice_output import speak, stop_speaking, set_voice_by_name
from memory import remember, recall, extract_memorable_facts

# File paths
USER_PROFILES_FILE = "prompts/user_profiles.json"
ASSISTANT_PROFILES_FILE = "prompts/assistant_profiles.json"

# Load profiles
with open(USER_PROFILES_FILE, "r") as f:
    user_profiles = json.load(f)

with open(ASSISTANT_PROFILES_FILE, "r") as f:
    assistant_profiles = json.load(f)

# Select active user
print("👤 Who's chatting today?")
for i, user in enumerate(user_profiles.keys()):
    print(f"{i+1}. {user_profiles[user]['name']}")

while True:
    try:
        choice = int(input("Enter number: ")) - 1
        user_key = list(user_profiles.keys())[choice]
        break
    except (ValueError, IndexError):
        print("Invalid choice. Try again.")

active_user = user_profiles[user_key]
user_name = active_user["name"]
preferred_voice = active_user["voice"]
set_voice_by_name(preferred_voice)

# Assistant to use
assistant_name = preferred_voice
assistant_profile = assistant_profiles.get(assistant_name, {})

# Graceful Ctrl+C
signal.signal(signal.SIGINT, lambda s, f: (stop_speaking(), print(f"\n👋 See you later, {user_name}!"), sys.exit(0)))

# Threaded speech
speech_thread = None
def threaded_speak(text):
    global speech_thread
    if speech_thread and speech_thread.is_alive():
        stop_speaking()
    speech_thread = threading.Thread(target=speak, args=(text,), daemon=True)
    speech_thread.start()

# Logging
def log_interaction(role, message, user_name, raw=None):
    log_file = f"data/chat_log_{user_name.lower()}.json"
    try:
        with open(log_file, 'r') as f:
            chat_log = json.loads(f.read().strip() or "[]")
    except FileNotFoundError:
        chat_log = []

    entry = {
        "role": role,
        "message": message,
        "timestamp": str(datetime.datetime.now())
    }

    if raw and role == "assistant":
        entry["raw_response"] = raw

    chat_log.append(entry)

    with open(log_file, 'w') as f:
        json.dump(chat_log, f, indent=2)

def load_chat_history():
    log_file = f"data/chat_log_{user_name.lower()}.json"
    try:
        with open(log_file, 'r') as f:
            chat_log = json.loads(f.read().strip() or "[]")
            return chat_log[-10:] if len(chat_log) > 10 else chat_log
    except FileNotFoundError:
        return []

def should_exit(user_input):
    return any(phrase in user_input.lower() for phrase in ["bye", "goodbye", "exit", "see you", "quit", "stop"])

def handle_exit():
    farewell = f"It was lovely chatting with you, {user_name}! Take care 💛 {assistant_name}"
    print(f"{assistant_name}: {farewell}")
    threaded_speak(farewell)
    log_interaction("assistant", farewell, user_name)
    sys.exit(0)

def chat_loop():
    print(f"👋 Hi {user_name}! I'm {assistant_name}. Let's chat! (Ctrl+C or say 'bye' to exit)")

    while True:
        try:
            user_input = input("You: ").strip()
            log_interaction("user", user_input, user_name)

            if "what" in user_input.lower() and "remember" in user_input.lower():
                memory = recall(user_name)
                if "Nothing remembered" in memory:
                    response = f"Hmm, I don't really have anything remembered yet, {user_name}. Want to tell me something to keep?"
                else:
                    response = f"I remember this about you:\n{memory}"
                print(f"{assistant_name}: {response}")
                threaded_speak(response)
                log_interaction("assistant", response, user_name)
                continue

            facts = extract_memorable_facts(user_input)
            for fact in facts:
                remember(fact, user_name)

            if should_exit(user_input):
                handle_exit()

            history = load_chat_history()
            result = ask_assistant(user_input, assistant_name, history=history, user_profile=active_user)

            print(f"{assistant_name}: {result['final']}")
            threaded_speak(result["final"])
            log_interaction("assistant", result["final"], user_name, raw=result["raw"])

        except KeyboardInterrupt:
            stop_speaking()
            print(f"\n👋 See you later, {user_name}!")
            break

if __name__ == "__main__":
    chat_loop()
