# myAI/llm_engine.py

from llama_cpp import Llama
import json

from memory import recall

ENABLE_MEMORY = False  # Change to True when you want memory back

MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_gpu_layers=60,
    verbose=False  # 👈 this disables internal print/log output
)

# Load assistant profiles
with open("prompts/assistant_profiles.json", "r") as f:
    assistant_profiles = json.load(f)

def ask_assistant(user_input, assistant_name="Anaya", history=None):
    profile = assistant_profiles.get(assistant_name, {})
    system_prompt = profile.get("system_prompt")
    
    if ENABLE_MEMORY:
        memory = recall()
        if memory and "Nothing remembered" not in memory:
            memory_text = f"\nHere's what you remember about Keyur:\n{memory}\n"
    else:
        memory_text = ""

    history_text = ""
    if history:
        for entry in history:
            speaker = "You" if entry["role"] == "user" else assistant_name
            history_text += f"{speaker}: {entry['message']}\n"

    full_prompt = f"{system_prompt}{memory_text}\n{history_text}You: {user_input}\n{assistant_name}:"

    print(f"{assistant_name}: ", end="", flush=True)
    output = ""
    for chunk in llm(
        prompt=full_prompt,
        max_tokens=300,
        temperature=0.75,
        top_p=0.9,
        stop=["\n", "</s>"],
        stream=True
    ):
        token = chunk["choices"][0]["text"]
        print(token, end="", flush=True)
        output += token

    print()
    return output.strip()