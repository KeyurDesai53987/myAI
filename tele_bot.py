import json
import time
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from chat_objects import User, Assistant
from mood import detect_mood
from llm_engine import ask_assistant

# === Directories and Files ===
HISTORY_DIR = Path("telegram_history")
HISTORY_DIR.mkdir(exist_ok=True)

USER_REGISTRY_FILE = HISTORY_DIR / "user_names.json"
user_names = {}

# Load registered names
if USER_REGISTRY_FILE.exists():
    with open(USER_REGISTRY_FILE, "r") as f:
        user_names = json.load(f)

user_histories = {}  # chat_id -> message history
mood_timestamp = 0

# === Load config and profiles ===
with open("config.json", "r") as f:
    CONFIG = json.load(f)
with open("prompts/user_profiles.json", "r") as f:
    user_profiles = json.load(f)
with open("prompts/assistant_profiles.json", "r") as f:
    assistant_profiles = json.load(f)

# Default user/assistant
user_key = CONFIG["default_user"]
assistant_key = CONFIG["default_assistant"]
user = User(name=user_profiles[user_key]["name"], voice=user_profiles[user_key]["voice"])
assistant = Assistant(name=assistant_key, profile=assistant_profiles[assistant_key])

# === Mood detection ===
def update_mood(text):
    global mood_timestamp
    if len(text.split()) < 4:
        return
    mood, score = detect_mood(text)
    if score > 0.6:
        user.memory["mood"] = mood
        mood_timestamp = time.time()

# === Message handler ===
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    chat_id = str(update.effective_chat.id)
    history_file = HISTORY_DIR / f"{chat_id}.json"

    # Ask name if not known
    if chat_id not in user_names:
        if message.lower().startswith("my name is"):
            name = message[10:].strip().split()[0].capitalize()
            user_names[chat_id] = name
            with open(USER_REGISTRY_FILE, "w") as f:
                json.dump(user_names, f, indent=2)
            await update.message.reply_text(f"Nice to meet you, {name}! How can I help?")
        else:
            await update.message.reply_text("Hi! What's your name? Please type: *My name is YourName*")
        return

    # Load or init history
    if chat_id not in user_histories:
        if history_file.exists():
            with open(history_file, "r") as f:
                user_histories[chat_id] = json.load(f)
        else:
            user_histories[chat_id] = []

    # Mood detection
    update_mood(message)

    # Build user profile
    user_profile = {"name": user_names[chat_id]}
    if "mood" in user.memory:
        user_profile["mood"] = user.memory["mood"]

    # Save user message
    user_histories[chat_id].append({"role": "user", "message": message})

    # Get response
    result = ask_assistant(message, assistant.name, user_histories[chat_id], user_profile)
    reply = result["final"].strip()

    if reply:
        user_histories[chat_id].append({"role": "assistant", "message": reply})
        with open(history_file, "w") as f:
            json.dump(user_histories[chat_id][-20:], f, indent=2)
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("Okay, It's time to say goodbye. 👋")

# === Start bot ===
def start_bot():
    app = ApplicationBuilder().token(CONFIG["telegram_token"]).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("🤖 Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    start_bot()
