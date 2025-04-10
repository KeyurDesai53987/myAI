from llama_cpp import Llama
import json
from memory import recall

MODEL_PATH = 'models/mistral-7b-instruct-v0.1.Q4_K_M.gguf'
llm = Llama(model_path=MODEL_PATH, n_ctx=1024, verbose=False)

# Load assistant profiles
with open('prompts/assistant_profiles.json', 'r') as f:
    assistant_profiles = json.load(f)

def rewrite_for_tone(response: str, assistant_name: str):
    prompt = (
        f"Rewrite the following response from {assistant_name} so it sounds like a caring, emotionally intelligent best friend. "
        f"Keep it short and natural. No robotic or assistant-like tone.\n\n"
        f"Original:\n{response}\n\nRewritten:"
    )
    result = llm(prompt=prompt, temperature=0.5, top_p=0.9, max_tokens=200, stop=["</s>", "\n\n"], stream=False)
    rewritten = result["choices"][0]["text"].strip()
    return rewritten if rewritten else response

def ask_assistant(user_input, assistant_name='Anaya', history=None, user_profile=None):
    profile = assistant_profiles.get(assistant_name, {})
    system_prompt = profile.get('system_prompt', 'You are a friendly best friend.')

    user_name = user_profile.get('name', 'User') if user_profile else 'User'
    user_style = user_profile.get('style', 'friendly') if user_profile else 'friendly'
    user_tone = user_profile.get('tone', 'casual') if user_profile else 'casual'

    # Inject placeholders
    system_prompt = system_prompt.replace('{user_name}', user_name)
    system_prompt = system_prompt.replace('{style}', user_style)
    system_prompt = system_prompt.replace('{tone}', user_tone)

    memory = recall(user_name)
    memory_text = f"\nHere’s what you remember about {user_name}:\n{memory}\n" if memory and 'Nothing remembered' not in memory else ''

    history_text = ''
    if history:
        for entry in history:
            speaker = 'You' if entry['role'] == 'user' else assistant_name
            history_text += f"{speaker}: {entry['message']}\n"

    full_prompt = (
        f"{system_prompt}\n\n"
        f"{memory_text}"
        f"{history_text}"
        f"You: {user_input}\n"
        f"{assistant_name}:"
    )

    print(f"{assistant_name}: ", end='', flush=True)
    output = ''
    for chunk in llm(
        prompt=full_prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.95,
        stop=['\n', '</s>'],
        stream=True
    ):
        token = chunk['choices'][0]['text']
        print(token, end='', flush=True)
        output += token

    print()
    rewritten = rewrite_for_tone(output.strip(), assistant_name)
    return {
        'raw': output.strip(),
        'final': rewritten
    }
