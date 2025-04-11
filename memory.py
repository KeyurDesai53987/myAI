# myAI/memory.py

import json
from pathlib import Path

MEMORY_FILE = Path("data/memory.json")
MEMORY_FILE.parent.mkdir(exist_ok=True)

def remember(fact, user_name):
    memory = load_memory()
    memory.setdefault(user_name, {"facts": []})
    if fact not in memory[user_name]["facts"]:
        memory[user_name]["facts"].append(fact)
    save_memory(memory)

def recall(user_name):
    memory = load_memory()
    facts = memory.get(user_name, {}).get("facts", [])
    if not facts:
        return "Nothing remembered yet."
    return "\n".join(facts)

def extract_memorable_facts(text):
    keywords = ["want", "need", "like", "wish", "plan", "important", "goal", "remember"]
    return [text.strip()] if any(k in text.lower() for k in keywords) else []

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
