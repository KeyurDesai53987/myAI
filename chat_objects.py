# myAI/chat_objects.py

import json
import datetime
from pathlib import Path
from voice_output import set_voice_by_name, speak, stop_speaking
from memory import remember, recall, extract_memorable_facts
from llm_engine import ask_assistant
from mood import detect_mood

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

class User:
    def __init__(self, name, voice):
        self.name = name
        self.voice = voice
        self.memory = {}
        self.log_file = DATA_DIR / f"chat_log_{self.name.lower()}.json"
        set_voice_by_name(voice)

    def log(self, role, message, raw=None):
        try:
            with open(self.log_file, 'r') as f:
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

        with open(self.log_file, 'w') as f:
            json.dump(chat, f, indent=2)

    def history(self):
        try:
            with open(self.log_file, 'r') as f:
                chat = json.loads(f.read().strip() or "[]")
                return chat[-10:] if len(chat) > 10 else chat
        except FileNotFoundError:
            return []

class Assistant:
    def __init__(self, name, profile):
        self.name = name
        self.profile = profile

    def speak(self, text):
        speak(text)

    def prompt(self, user_name):
        return self.profile["system_prompt"].replace("{user_name}", user_name)

class ChatManager:
    def __init__(self, user, assistant, config):
        self.user = user
        self.assistant = assistant
        self.config = config
        self.prompt_modifier = None  # NEW
        self.user_input_hook = None  # NEW

    def set_prompt_modifier(self, modifier_func):
        self.prompt_modifier = modifier_func

    def set_user_hook(self, hook_func):
        self.user_input_hook = hook_func


    def run(self):
        print(f"👋 Hi {self.user.name}! I'm {self.assistant.name}. Let's chat. (Press Ctrl+C to quit)")
        while True:
            try:
                user_input = input("You: ").strip()
                self.user.log("user", user_input)

                if user_input.lower().startswith("!remember"):
                    fact = user_input[9:].strip()
                    if fact:
                        remember(fact, self.user.name)
                        reply = "Got it! I’ll keep that in mind."
                    else:
                        reply = "You need to say what to remember."
                    print(f"{self.assistant.name}: {reply}")
                    self.user.log("assistant", reply)
                    continue

                if user_input.lower().startswith("!recall"):
                    memory = recall(self.user.name)
                    if "Nothing remembered" in memory:
                        reply = "I don’t have anything stored yet. Want to tell me something?"
                    else:
                        reply = f"I remember this about you:\n{memory}"
                    print(f"{self.assistant.name}: {reply}")
                    self.user.log("assistant", reply)
                    continue

                if self.config.get("use_memory", True):
                    for fact in extract_memorable_facts(user_input):
                        remember(fact, self.user.name)

                if any(phrase in user_input.lower() for phrase in ["bye", "goodbye"]):
                    farewell = f"Bye {self.user.name} 👋"
                    print(f"{self.assistant.name}: {farewell}")
                    self.user.log("assistant", farewell)
                    break

                # ASYNC mood detection update (non-blocking)
                if hasattr(self, "user_input_hook") and self.user_input_hook:
                    self.user_input_hook(self.user, user_input)

                history = self.user.history()
                mood = self.user.memory.get("mood")  # Read cached mood
                user_profile = {"name": self.user.name}
                if mood:
                    user_profile["mood"] = mood

                result = ask_assistant(
                    user_input,
                    self.assistant.name,
                    history,
                    user_profile=user_profile
                )

                print(f"{self.assistant.name}: {result['final']}")
                if self.config.get("enable_voice", True):
                    self.assistant.speak(result["final"])

                self.user.log("assistant", result["final"], raw=result["raw"])

            except KeyboardInterrupt:
                stop_speaking()
                print(f"\n👋 See you later, {self.user.name}!")
                break
        