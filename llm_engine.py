# myAI/llm_engine.py

from llama_cpp import Llama

# Load the Mistral GGUF model
MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=512)

# def ask_assistant(prompt, assistant_name="Anaya"):
#     base_context = {
#         "Anaya": "gentle and calming",
#         "Ishita": "motivating and energetic",
#         "Isha": "emotionally soft and poetic",
#         "Sakhi": "cheerful and fun"
#     }

#     tone = base_context.get(assistant_name, "friendly")

#     # Create a free-form, friendly chat prompt
#     raw_prompt = (
#         f"You are {assistant_name}, a {tone} girl who is Keyur's closest friend. "
#         f"Respond like you're having a relaxed, natural conversation with him.\n"
#         f"Keyur: {prompt}\n"
#         f"{assistant_name}:"
#     )

#     response = llm(
#         prompt=raw_prompt,
#         temperature=0.7,
#         top_p=0.95,
#         max_tokens=100,
#         stop=["\n", "</s>"]
#     )

#     return response["choices"][0]["text"].strip()

def ask_assistant(user_input, assistant_name="Anaya", history=None):
    # Build the prompt from history
    history_text = ""
    if history:
        for item in history:
            role = "You" if item["role"] == "user" else assistant_name
            history_text += f"{role}: {item['message']}\n"

    # Append latest user input
    history_text += f"You: {user_input}\n{assistant_name}:"

    # Generate response
    response = llm(
        prompt=history_text,
        temperature=0.7,
        top_p=0.95,
        max_tokens=150,
        stop=["\n", "</s>"]
    )

    return response["choices"][0]["text"].strip()
