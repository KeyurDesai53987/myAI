import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers import BitsAndBytesConfig
from rewrite import rewrite_for_tone
from context_injection import inject_context  # if using dynamic values

# Load config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

# Load assistant profiles
with open('prompts/assistant_profiles.json', 'r', encoding='utf-8') as f:
    assistant_profiles = json.load(f)

MODEL_NAME = CONFIG["hf_model"]
MAX_TOKENS = CONFIG.get("max_tokens", 512)
USE_TONE = CONFIG.get("enable_tone", True)

# Quantization config
bnb_config = None

# Load model + tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto"
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def format_prompt(system_prompt, history, user_input, assistant_name):
    prompt = system_prompt.strip() + "\n"
    for h in history:
        speaker = "You" if h["role"] == "user" else assistant_name
        prompt += f"{speaker}: {h['message']}\n"
    prompt += f"You: {user_input}\n{assistant_name}:"
    return prompt

def ask_assistant(user_input, assistant_name, history=None, user_profile=None):
    user_name = user_profile["name"]
    profile = assistant_profiles[assistant_name]
    system_prompt = profile["system_prompt"].replace("{user_name}", user_name)
    system_prompt = inject_context(system_prompt)  # <-- THIS IS NEEDED

    prompt = format_prompt(system_prompt, history or [], user_input, assistant_name)

    response = generator(prompt, max_new_tokens=MAX_TOKENS, do_sample=True, temperature=0.7)
    output = response[0]["generated_text"].split(f"{assistant_name}:")[-1].strip()

    final = rewrite_for_tone(output, user_profile, CONFIG) if USE_TONE else output
    return {"final": final}
