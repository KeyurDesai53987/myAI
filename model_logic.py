# myAI/model_logic.py

def get_model_format(model_path):
    model_path = model_path.lower()

    if "tinyllama" in model_path:
        return {
            "chat_format": "chatml",
            "stop": ["<|user|>", "<|system|>", "<|assistant|>", "</s>"],
            "prefix_template": "<|system|>{system_prompt}</s><|user|>{user_input}</s><|assistant|>"
        }
    elif "mistral" in model_path or "llama" in model_path:
        return {
            "chat_format": "llama-2",
            "stop": ["You:", "Assistant:"],
            "prefix_template": "{system_prompt}\n\n{history}You: {user_input}\n{assistant_name}:"
        }
    elif "phi" in model_path:
        return {
            "chat_format": "prompt-style",
            "stop": ["User:", "Assistant:"],
            "prefix_template": "{system_prompt}\n\nUser: {user_input}\nAssistant:"
        }
    else:
        return {
            "chat_format": "plain",
            "stop": ["\n"],
            "prefix_template": "{system_prompt}\n\n{history}{user_input}"
        }
