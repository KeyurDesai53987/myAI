# myAI/model_logic.py

def get_model_format(model_path):
    model_path = model_path.lower()

    if "mistral" in model_path:
        return {
            "chat_format": "llama-2",
            "stop": ["You:", "Assistant:"],
            "prefix": ""
        }
    elif "llama" in model_path:
        return {
            "chat_format": "llama-2",
            "stop": ["You:", "Assistant:"],
            "prefix": ""
        }
    elif "phi" in model_path:
        return {
            "chat_format": "prompt-style",
            "stop": ["User:", "Assistant:"],
            "prefix": "User: "
        }
    else:
        return {
            "chat_format": "plain",
            "stop": ["\n"],
            "prefix": ""
        }
