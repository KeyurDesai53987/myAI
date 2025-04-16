import json

with open("config.json", "r") as f:
    config = json.load(f)

backend = config.get("llm_backend", "hf").lower()

if backend == "llama-cpp":
    print("🧠 Using llama-cpp backend")
    from llm_engine_cpp import ask_assistant
else:
    print("🧠 Using Hugging Face Transformers backend")
    from llm_engine_hf import ask_assistant
