import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_assistant(prompt, assistant_name="Anaya"):
    system_msg = f"You are {assistant_name}, a warm and friendly voice assistant who supports Keyur emotionally like a best friend."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Sorry, I couldn’t think of a good reply because of a technical issue: {e}"
