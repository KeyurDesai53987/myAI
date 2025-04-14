# myAI/llm_engine.py

import json
from llama_cpp import Llama
from rewrite import rewrite_for_tone
from model_logic import get_model_format

# Load config directly
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

MODEL_PATH = CONFIG["model_path"]
N_CTX = CONFIG.get("n_ctx", 1024)
N_GPU_LAYERS = CONFIG.get("n_gpu_layers", 40)
N_THREADS = CONFIG.get("n_threads", 8)
VERBOSE_MODE = CONFIG.get("llm_verbose", False)

# Load assistant profiles
with open("prompts/assistant_profiles.json", "r") as f:
    assistant_profiles = json.load(f)

# Model-specific settings
model_settings = get_model_format(MODEL_PATH)
STOP_TOKENS = model_settings["stop"]
FORMAT_TYPE = model_settings.get("chat_format")

# Initialize LLM
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_gpu_layers=N_GPU_LAYERS,
    n_threads=N_THREADS,
    verbose=VERBOSE_MODE
)

def ask_assistant(user_input, assistant_name, history=None, user_profile=None):
    profile = assistant_profiles[assistant_name]
    user_name = user_profile["name"]
    system_prompt = profile["system_prompt"].replace("{user_name}", user_name)

    if FORMAT_TYPE == "chatml":  # TinyLlama
        messages = [f"<|system|>{system_prompt}</s>"]
        if history:
            for entry in history:
                if entry["role"] == "user":
                    messages.append(f"<|user|>{entry['message']}</s>")
                else:
                    messages.append(f"<|assistant|>{entry['message']}</s>")
        messages.append(f"<|user|>{user_input}</s><|assistant|>")
        prompt = "\n".join(messages)

    else:  # LLaMA / Mistral / Phi
        history_text = ""
        if history:
            for entry in history:
                speaker = "You" if entry["role"] == "user" else assistant_name
                history_text += f"{speaker}: {entry['message']}\n"
        prompt = f"{system_prompt.strip()}\n\n{history_text}You: {user_input}\n{assistant_name}:"

    output = ""
    for chunk in llm(
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
        top_p=0.95,
        stop=STOP_TOKENS,
        stream=True
    ):
        token = chunk["choices"][0]["text"]
        # print(token, end="", flush=True)
        output += token

    print()
    final = rewrite_for_tone(output.strip(), user_profile, CONFIG)
    return {"final": final, "raw": output.strip()}
