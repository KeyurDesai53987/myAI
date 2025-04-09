# myAI/llm_engine.py

from llama_cpp import Llama
import json

MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=1024)

# Load assistant profiles
with open("prompts/assistant_profiles.json", "r") as f:
    assistant_profiles = json.load(f)

def ask_assistant(user_input, assistant_name="Anaya", history=None):
    system_prompt = assistant_profiles[assistant_name]["system_prompt"]

    history_text = ""
    if history:
        for entry in history:
            speaker = "You" if entry["role"] == "user" else assistant_name
            history_text += f"{speaker}: {entry['message']}\n"

    full_prompt = f"{system_prompt}\n\n{history_text}You: {user_input}\n{assistant_name}:"

    print(f"{assistant_name}: ", end="", flush=True)
    output = ""
    for chunk in llm(
        prompt=full_prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.95,
        stop=["\n", "</s>"],
        stream=True
    ):
        token = chunk["choices"][0]["text"]
        print(token, end="", flush=True)
        output += token

    print()
    return output.strip()