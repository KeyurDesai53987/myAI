import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers import BitsAndBytesConfig
from rewrite import rewrite_for_tone

# Load config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

MODEL_NAME = CONFIG["hf_model"]
MAX_TOKENS = CONFIG.get("max_tokens", 512)
USE_TONE = CONFIG.get("enable_tone", True)

# Quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# Load model + tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
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
    from prompts.assistant_profiles import assistant_profiles
    user_name = user_profile["name"]
    profile = assistant_profiles[assistant_name]
    system_prompt = profile["system_prompt"].replace("{user_name}", user_name)

    prompt = format_prompt(system_prompt, history or [], user_input, assistant_name)

    response = generator(prompt, max_new_tokens=MAX_TOKENS, do_sample=True, temperature=0.7)
    output = response[0]["generated_text"].split(f"{assistant_name}:")[-1].strip()

    final = rewrite_for_tone(output, user_profile, CONFIG) if USE_TONE else output
    return {"final": final}
