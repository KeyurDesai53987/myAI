# myAI/llm_engine.py

from llama_cpp import Llama

MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=1024)

def ask_assistant(user_input, assistant_name="Anaya", history=None):
    prompt_intro = (
        f"You are {assistant_name}, a warm, emotionally intelligent best friend to Keyur.\n"
        "You speak casually, like a caring friend. Here's the conversation:\n\n"
    )

    history_text = ""
    if history:
        for entry in history:
            speaker = "You" if entry["role"] == "user" else assistant_name
            history_text += f"{speaker}: {entry['message']}\n"

    full_prompt = f"{prompt_intro}{history_text}You: {user_input}\n{assistant_name}:"

    # 🧠 Stream response token-by-token
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

    print()  # new line after response
    return output.strip()
