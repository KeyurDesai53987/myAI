import os
from pathlib import Path

# Base project structure
folders = [
    "./data",
    "./assets",
    "./prompts"
]

files = {
    "./requirements.txt": "openai==1.14.3\npyttsx3==2.90\npython-dotenv==1.0.1\n",
    "./.env": "OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx\n",
    "./assets/motivational_quotes.txt": "You are stronger than you think.\nThis too shall pass.\nTake a deep breath, you're doing great.\n",
    "./prompts/general_prompt.txt": "Respond warmly and wisely as if you're a close friend.\n",
    "./prompts/mood_check_prompt.txt": "Keyur is feeling {mood}. Say something comforting or motivating.\n",
    "./prompts/assistant_profiles.json": '{\n  "Anaya": {"tone": "calm"},\n  "Ishita": {"tone": "motivating"},\n  "Isha": {"tone": "gentle"},\n  "Sakhi": {"tone": "cheerful"}\n}\n',
    "./data/moods.json": "{}\n",
    "./data/tasks.json": "{}\n"
}

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("✅ Project folders and files created successfully!")
