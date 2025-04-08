# myAI/llm_engine.py

from llama_cpp import Llama

# Load the Phi-2 model
MODEL_PATH = "models/phi-2.Q2_K.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=1024)

def ask_assistant(prompt, assistant_name="Anaya"):
    # Construct a simple, raw prompt since Phi-2 is not chat-optimized
    raw_prompt = (
        f"Keyur is feeling a little low today."
        f" {assistant_name}, as his best friend and voice assistant, what would you say to comfort him?\n"
        f"{assistant_name}:"
    )

    response = llm(
        prompt=raw_prompt,
        temperature=0.7,
        top_p=0.9,
        max_tokens=200,
        stop=["\n"]
    )

    return response["choices"][0]["text"].strip()
