# myAI/setup.py

import os
import json
from pathlib import Path

def run_setup():
    print("🔧 Starting setup...")

    # Create folders
    Path("data").mkdir(exist_ok=True)
    Path("prompts").mkdir(exist_ok=True)

    # Sample user
    user_profiles = {
        "keyur": {
            "name": "Keyur",
            "voice": "Anaya"
        }
    }

    # Sample assistants
    assistant_profiles = {
        "Anaya": {
            "name": "Anaya",
            "style": "warm, supportive",
            "system_prompt": "You are Anaya, a supportive, warm and cheerful best friend to {user_name}. Talk like a caring friend, not a robot or assistant. Keep it short and natural."
        },
        "Ishita": {
            "name": "Ishita",
            "style": "smart and intuitive",
            "system_prompt": "You are Ishita, {user_name}'s intuitive best friend. Keep your responses thoughtful and human, not robotic. Offer support like a real person."
        }
    }

    # Config
    config = {
        "model_path": "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "n_ctx": 1024,
        "n_gpu_layers": 40,
        "n_threads": 8,
        "llm_verbose": False,
        "use_memory": True,
        "enable_voice": True,
        "response_rewriting": True
    }

    # Write files
    with open("prompts/user_profiles.json", "w") as f:
        json.dump(user_profiles, f, indent=2)
    with open("prompts/assistant_profiles.json", "w") as f:
        json.dump(assistant_profiles, f, indent=2)
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("✅ Setup complete!")

if __name__ == "__main__":
    run_setup()
