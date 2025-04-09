import os
import json
from llama_cpp import Llama

# Load LLM once for memory extraction
MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
memory_llm = Llama(model_path=MODEL_PATH, n_ctx=1024, verbose=False)

MEMORY_FILE = "data/memory.json"
os.makedirs("data", exist_ok=True)

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"facts": []}, f)

def remember(fact: str):
    fact = fact.strip()

    # 💡 Reject vague or suspicious facts
    if (
        not fact or
        len(fact.split()) < 4 or  # too short
        len(fact) > 250 or        # too long (likely hallucinated)
        "mentioned" in fact.lower() or
        "remember" in fact.lower() or
        "remind" in fact.lower() or
        "wants to be reminded" in fact.lower()
    ):
        return

    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)

    if fact not in memory["facts"]:
        memory["facts"].append(fact)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def recall():
    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
        return "\n".join(memory["facts"]) if memory["facts"] else "Nothing remembered yet."
    except:
        return "Memory not found."

def extract_memorable_facts(text: str):
    # 🚨 STRICT prompt to prevent hallucination
    prompt = (
        "Extract ONLY factual information that Keyur directly states in the message below. "
        "Do NOT guess or assume anything. Do NOT say 'Keyur mentioned...' — just extract clear facts. "
        "Respond with NOTHING if no personal info is shared.\n\n"
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

    # 🧹 Filter: ignore vague/meta outputs
    garbage = {
        "none", "no", "nothing", "n/a", "null", "nothing memorable", "nothing to remember",
    }

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
