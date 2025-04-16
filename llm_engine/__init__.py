import json

with open("config.json", "r") as f:
    config = json.load(f)

if config.get("llm_backend") == "hf":
    print("🧠 Using Hugging Face Transformers backend")
    from llm_engine_hf import ask_assistant
else:
    print("🧠 Using llama-cpp backend")
    from llm_engine_cpp import ask_assistant

