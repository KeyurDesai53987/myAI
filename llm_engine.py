from llama_cpp import Llama
import json
from memory import recall
from smart_features import detect_mood_with_llm

with open('config.json', 'r') as f:
    CONFIG = json.load(f)

MODEL_PATH = 'models/mistral-7b-instruct-v0.1.Q4_K_M.gguf'

VERBOSE_MODE = CONFIG.get('llm_verbose', False)
llm = Llama(model_path=MODEL_PATH, n_ctx=1024, verbose=VERBOSE_MODE)

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

    memory_text = ''
    if CONFIG['use_memory']:
        memory = recall(user_name)
        if memory and 'Nothing remembered' not in memory:
            memory_text = f"\nHere's what you remember about {user_name}:\n{memory}\n"


    history_text = ''
    if history:
        for entry in history:
            speaker = 'You' if entry['role'] == 'user' else assistant_name
            history_text += f"{speaker}: {entry['message']}\n"

    # Control mood injection
    if CONFIG['inject_mood']:
        mood = detect_mood_with_llm(user_input, llm)
        mood_line = f"Current mood of {user_name}: {mood}\n"
    else:
        mood_line = ''

    full_prompt = (
        f"{system_prompt}\n\n"
        f"{memory_text}"
        f"{mood_line}"
        f"{history_text}"
        f"You: {user_input}\n"
        f"{assistant_name}:"
    )


    # print(f"{assistant_name}: ", end='', flush=True)
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
        # print(token, end='', flush=True)
        output += token

    print()

    # Control rewriting
    if CONFIG['use_response_rewriting']:
        if any(phrase in output.lower() for phrase in ['how can i help', 'as your assistant']) or len(output.split()) > 30:
            rewritten = rewrite_for_tone(output.strip(), assistant_name)
        else:
            rewritten = output.strip()
    else:
        rewritten = output.strip()

    return {
        'raw': output.strip(),
        'final': rewritten
    }
