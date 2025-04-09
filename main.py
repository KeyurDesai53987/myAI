import os
import json
import signal
import sys
import threading
import datetime
from llm_engine import ask_assistant
from voice_output import speak, stop_speaking, set_voice_by_name

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# File paths
CHAT_LOG_FILE = "data/chat_log.json"
LAST_USED_FILE = "data/last_used.json"
USAGE_FILE = "data/assistant_usage.json"
PROFILE_FILE = "prompts/assistant_profiles.json"

# Load assistant profiles
with open(PROFILE_FILE, "r") as f:
    assistant_profiles = json.load(f)
ASSISTANT_NAMES = list(assistant_profiles.keys())

# Threaded speech
speech_thread = None

def threaded_speak(text):
    global speech_thread
    if speech_thread and speech_thread.is_alive():
        stop_speaking()
    speech_thread = threading.Thread(target=speak, args=(text,), daemon=True)
    speech_thread.start()

def choose_assistant():
    try:
        with open(LAST_USED_FILE, "r") as f:
            last_used = json.load(f).get("assistant")
            if last_used in ASSISTANT_NAMES:
                use_last = input(f"Would you like to continue with {last_used}? (y/n): ").strip().lower()
                if use_last == 'y':
                    return last_used
    except Exception as e:
        print(f"No previous assistant found. Error: {e}")

    print("Who would you like to talk to today?")
    for i, name in enumerate(ASSISTANT_NAMES):
        print(f"{i+1}. {name}")
    while True:
        try:
            choice = int(input("Enter the number: ")) - 1
            if 0 <= choice < len(ASSISTANT_NAMES):
                selected = ASSISTANT_NAMES[choice]
                with open(LAST_USED_FILE, "w") as f:
                    json.dump({"assistant": selected}, f)
                return selected
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

def update_usage_stats(assistant_name):
    try:
        with open(USAGE_FILE, "r") as f:
            usage_data = json.load(f)
    except FileNotFoundError:
        usage_data = {}

    if assistant_name not in usage_data:
        usage_data[assistant_name] = {"sessions": 0, "last_used": None}

    usage_data[assistant_name]["sessions"] += 1
    usage_data[assistant_name]["last_used"] = str(datetime.datetime.now())

    with open(USAGE_FILE, "w") as f:
        json.dump(usage_data, f, indent=2)

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

def load_chat_history():
    try:
        with open(CHAT_LOG_FILE, 'r') as f:
            content = f.read()
            chat_log = json.loads(content) if content.strip() else []
        return chat_log[-10:] if len(chat_log) > 10 else chat_log
    except FileNotFoundError:
        return []

def should_exit(user_input):
    exit_phrases = ["bye", "goodbye", "see you", "exit", "stop", "quit"]
    return any(phrase in user_input.lower() for phrase in exit_phrases)

def handle_exit(assistant_name):
    farewell = f"It was lovely chatting with you, Keyur! Take care 💛 – {assistant_name}"
    print(f"{assistant_name}: {farewell}")
    threaded_speak(farewell)
    log_interaction("assistant", farewell)
    sys.exit(0)

def chat_loop(assistant_name):
    print(f"👋 Hi Keyur! I'm {assistant_name}. Let's chat! (Ctrl+C or say 'bye' to exit)")

    while True:
        try:
            user_input = input("You: ").strip()
            log_interaction("user", user_input)

            if should_exit(user_input):
                handle_exit(assistant_name)

            recent_history = load_chat_history()
            response = ask_assistant(user_input, assistant_name, history=recent_history)

            # print(f"{assistant_name}: {response}")
            threaded_speak(response)
            log_interaction("assistant", response)

        except KeyboardInterrupt:
            stop_speaking()
            print("\n👋 See you next time, Keyur!")
            break

def main():
    assistant_name = choose_assistant()
    set_voice_by_name(assistant_name)
    update_usage_stats(assistant_name)
    chat_loop(assistant_name)

# Graceful Ctrl+C
signal.signal(signal.SIGINT, lambda s, f: (stop_speaking(), print("\n👋 Exiting. See you later, Keyur!"), sys.exit(0)))

if __name__ == "__main__":
    main()
