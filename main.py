# myAI/main.py

import json
import signal
import sys
import threading
import keyboard
import time
from pathlib import Path
from chat_objects import User, Assistant, ChatManager
from voice_output import stop_speaking
from mood import detect_mood  # NEW
import llm_engine  # Ensure this is imported to initialize the LLM engine

# Load config
with open("config.json", "r") as f:
    CONFIG = json.load(f)

# Paths
USER_PROFILES_FILE = Path("prompts/user_profiles.json")
ASSISTANT_PROFILES_FILE = Path("prompts/assistant_profiles.json")

mood_timestamp = 0  # NEW

def load_profiles():
    with open(USER_PROFILES_FILE, "r") as f:
        user_profiles = json.load(f)
    with open(ASSISTANT_PROFILES_FILE, "r") as f:
        assistant_profiles = json.load(f)
    return user_profiles, assistant_profiles

def choose_user_and_assistant(user_profiles, assistant_profiles):
    default_user_key = CONFIG.get("default_user")
    default_assistant_key = CONFIG.get("default_assistant")

    if default_user_key in user_profiles:
        user = User(name=user_profiles[default_user_key]["name"], voice=user_profiles[default_user_key]["voice"])
        assistant_key = default_assistant_key
        assistant = Assistant(name=assistant_key, profile=assistant_profiles[assistant_key])
        print(f"✅ Using default user: {user.name} with assistant: {assistant.name}")
        return user, assistant

    print("👤 Who's chatting today?")
    for i, key in enumerate(user_profiles):
        print(f"{i+1}. {user_profiles[key]['name']}")
    while True:
        try:
            selected = list(user_profiles.keys())[int(input("Enter number: ")) - 1]
            break
        except:
            print("Invalid choice.")
    user_data = user_profiles[selected]
    user = User(name=user_data["name"], voice=user_data["voice"])
    assistant_key = user_data.get("voice", default_assistant_key)
    assistant = Assistant(name=assistant_key, profile=assistant_profiles[assistant_key])
    return user, assistant

# Async mood detection (NEW)
def update_mood_async(user_obj, user_text):
    def detect_and_store():
        global mood_timestamp
        if len(user_text.split()) < 4:
            return
        mood, score = detect_mood(user_text)
        if score > 0.6:
            user_obj.memory["mood"] = mood
            mood_timestamp = time.time()
    threading.Thread(target=detect_and_store).start()

def main():
    user_profiles, assistant_profiles = load_profiles()
    user, assistant = choose_user_and_assistant(user_profiles, assistant_profiles)

    signal.signal(signal.SIGINT, lambda s, f: (stop_speaking(), print("\n👋 Jai Shree Krishna!"), sys.exit(0)))
    keyboard.add_hotkey("ctrl+c", lambda: sys.exit(0))

    chat = ChatManager(user, assistant, CONFIG)

    # Inject mood into system message before each prompt (NEW)
    def custom_prompt_modifier(prompt):
        if CONFIG.get("enable_mood_tone"):
            if "mood" in user.memory and (time.time() - mood_timestamp) < 120:
                return f"User is in a {user.memory['mood']} mood. Respond appropriately.\n{prompt}"
        return prompt

    chat.set_prompt_modifier(custom_prompt_modifier)  # You need to support this in ChatManager

    chat.set_user_hook(update_mood_async)  # Hook to pass user input to mood updater
    chat.run()

if __name__ == "__main__":
    main()
