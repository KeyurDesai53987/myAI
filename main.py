# myAI/main.py

import os
import json
import signal
import sys
import threading
import datetime
from pathlib import Path
from llm_engine import ask_assistant
from voice_output import speak, stop_speaking, set_voice_by_name
from memory import remember, recall, extract_memorable_facts
from rewrite import rewrite_for_tone

# Load config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

try:
    import keyboard
except ImportError:
    print("Missing 'keyboard' module. Install with: pip install keyboard")
    sys.exit(1)

# Paths
USER_PROFILES_FILE = Path("prompts/user_profiles.json")
ASSISTANT_PROFILES_FILE = Path("prompts/assistant_profiles.json")
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Globals
user_profiles = {}
assistant_profiles = {}
active_user = {}
assistant_name = ""
assistant_profile = {}
speech_thread = None


def load_profiles():
    global user_profiles, assistant_profiles
    with open(USER_PROFILES_FILE, "r") as f:
        user_profiles = json.load(f)
    with open(ASSISTANT_PROFILES_FILE, "r") as f:
        assistant_profiles = json.load(f)


def choose_user():
    global active_user, assistant_name, assistant_profile
    default_user = CONFIG.get("default_user")
    default_assistant = CONFIG.get("default_assistant")

    if default_user in user_profiles:
        active_user = user_profiles[default_user]
        assistant_name = active_user.get("voice", default_assistant)
        assistant_profile = assistant_profiles.get(assistant_name, {})
        set_voice_by_name(assistant_name)
        print(f"✅ Using default user: {active_user['name']} with assistant: {assistant_name}")
        return

    print("👤 Who's chatting today?")
    for i, u in enumerate(user_profiles):
        print(f"{i+1}. {user_profiles[u]['name']}")
    while True:
        try:
            user_key = list(user_profiles.keys())[int(input("Enter number: ")) - 1]
            break
        except Exception:
            print("Invalid choice.")
    active_user = user_profiles[user_key]
    assistant_name = active_user["voice"]
    assistant_profile = assistant_profiles.get(assistant_name, {})
    set_voice_by_name(assistant_name)


def switch_user():
    choose_user()
    print(f"✅ Switched to {active_user['name']} with assistant {assistant_name}")


def switch_assistant():
    global assistant_name, assistant_profile
    print("🔄 Switching assistant...")
    for i, a in enumerate(assistant_profiles):
        print(f"{i+1}. {a}")
    try:
        choice = int(input("Enter number: ")) - 1
        assistant_name = list(assistant_profiles.keys())[choice]
        assistant_profile = assistant_profiles[assistant_name]
        set_voice_by_name(assistant_name)
        print(f"✅ Switched to {assistant_name}")
    except Exception:
        print("❌ Invalid selection.")


def log(role, message, raw=None):
    user_name = active_user["name"]
    log_file = DATA_DIR / f"chat_log_{user_name.lower()}.json"
    try:
        with open(log_file, 'r') as f:
            chat = json.loads(f.read().strip() or "[]")
    except FileNotFoundError:
        chat = []
    entry = {
        "role": role,
        "message": message,
        "timestamp": str(datetime.datetime.now())
    }
    if raw and role == "assistant":
        entry["raw_response"] = raw
    chat.append(entry)
    with open(log_file, 'w') as f:
        json.dump(chat, f, indent=2)


def load_history():
    user_name = active_user["name"]
    log_file = DATA_DIR / f"chat_log_{user_name.lower()}.json"
    try:
        with open(log_file, 'r') as f:
            chat = json.loads(f.read().strip() or "[]")
            return chat[-5:] if len(chat) > 5 else chat
    except:
        return []


def threaded_speak(text):
    global speech_thread
    if speech_thread and speech_thread.is_alive():
        stop_speaking()
    speech_thread = threading.Thread(target=speak, args=(text,), daemon=True)
    speech_thread.start()


def should_exit(user_input):
    return any(phrase in user_input.lower() for phrase in ["bye", "exit", "quit", "goodbye", "see you"])


def chat():
    print(f"👋 Hi {active_user['name']}! I'm {assistant_name}. Let's chat.")

    keyboard.add_hotkey("ctrl+u", switch_user)
    keyboard.add_hotkey("ctrl+a", switch_assistant)

    while True:
        try:
            user_input = input("You: ").strip()
            log("user", user_input)

            if CONFIG.get("use_memory", True):
                for fact in extract_memorable_facts(user_input):
                    remember(fact, active_user["name"])

            if should_exit(user_input):
                print(f"{assistant_name}: Bye {active_user['name']} 👋")
                log("assistant", f"Bye {active_user['name']} 👋")
                break

            history = load_history()
            result = ask_assistant(user_input, assistant_name, history, user_profile=active_user)

            print(f"{assistant_name}: {result['final']}")
            if CONFIG.get("enable_voice", True):
                threaded_speak(result["final"])

            log("assistant", result["final"], raw=result["raw"])

        except KeyboardInterrupt:
            stop_speaking()
            print(f"\n👋 See you later, {active_user['name']}!")
            break


def main():
    load_profiles()
    choose_user()
    signal.signal(signal.SIGINT, lambda s, f: (stop_speaking(), print(f"\n👋I won't talk Bye!"), sys.exit(0)))
    chat()


if __name__ == "__main__":
    main()
