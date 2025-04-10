import os
import json
from llama_cpp import Llama

MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
memory_llm = Llama(model_path=MODEL_PATH, n_ctx=1024, verbose=False)

MEMORY_DIR = "data"
os.makedirs(MEMORY_DIR, exist_ok=True)

def get_memory_file(user_name):
    return os.path.join(MEMORY_DIR, f"memory_{user_name.lower()}.json")

def ensure_memory_file(user_name):
    path = get_memory_file(user_name)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({"facts": []}, f)
    return path

def remember(fact: str, user_name: str):
    fact = fact.strip()
    if (
        not fact or
        len(fact.split()) < 4 or
        len(fact) > 250 or
        "mentioned" in fact.lower() or
        "remember" in fact.lower() or
        "remind" in fact.lower()
    ):
        return

    path = ensure_memory_file(user_name)
    with open(path, "r") as f:
        memory = json.load(f)

    if fact not in memory["facts"]:
        memory["facts"].append(fact)

    with open(path, "w") as f:
        json.dump(memory, f, indent=2)

def recall(user_name: str):
    try:
        path = ensure_memory_file(user_name)
        with open(path, "r") as f:
            memory = json.load(f)
        return "\n".join(memory["facts"]) if memory["facts"] else "Nothing remembered yet."
    except:
        return "Memory not found."

def extract_memorable_facts(text: str):
    prompt = (
        "Extract only direct, personal facts about the user that were explicitly stated in the message. "
        "Do NOT invent or guess. Skip vague or general statements. Return NOTHING if there's nothing worth remembering.\n\n"
        f"Message: \"{text}\"\n\nFacts:"
    )

    result = memory_llm(
        prompt=prompt,
        temperature=0.3,
        top_p=0.9,
        max_tokens=150,
        stop=["\n\n", "</s>"],
        stream=False
    )

    response = result["choices"][0]["text"].strip()

    garbage = {"none", "no", "nothing", "n/a", "null", "nothing memorable"}
    facts = [
        line.strip("-•* ").capitalize()
        for line in response.split("\n")
        if line.strip()
        and line.strip().lower() not in garbage
        and "remember" not in line.lower()
        and "mention" not in line.lower()
        and "remind" not in line.lower()
    ]

    return facts
