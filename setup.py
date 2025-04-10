import os
import json
import shutil

PROMPTS_DIR = 'prompts'
os.makedirs(PROMPTS_DIR, exist_ok=True)

USER_FILE = os.path.join(PROMPTS_DIR, 'user_profiles.json')
ASSISTANT_FILE = os.path.join(PROMPTS_DIR, 'assistant_profiles.json')

def list_models():
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    return [f for f in os.listdir(models_dir) if f.endswith('.gguf')]

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def prompt_user_profile():
    user_name = input('Enter name: ').strip()
    style = input('Preferred reply style: ').strip()
    tone = input('Preferred tone: ').strip()
    voice = input('Default assistant: ').strip()
    return user_name.lower(), {
        'name': user_name,
        'style': style,
        'tone': tone,
        'voice': voice,
        'personality': f'{style} and {tone}'
    }

def prompt_assistant_profile(name=None):
    name = name or input('Assistant name: ').strip()
    tone = input(f'Tone for {name}: ').strip()
    style = input(f'Style for {name}: ').strip()
    expertise = input(f'{name} is good at: ').strip()

    models = list_models()
    if models:
        print('📦 Available models:')
        for i, m in enumerate(models):
            print(f'{i+1}. {m}')
        while True:
            try:
                choice = int(input('Select model number: ')) - 1
                if 0 <= choice < len(models):
                    model_path = os.path.join('models', models[choice])
                    break
            except:
                print('Invalid choice.')
    else:
        model_path = input('Enter model path: ').strip()

    prompt = (
        f'You are {name}, {{user_name}}\'s best friend. '
        f'Keep responses short and simple. Never sound like an assistant. '
        f'Speak in a {tone} tone and {style} style. Show empathy if {{user_name}} seems down.'
    )

    return name, {
        'system_prompt': prompt,
        'tone': tone,
        'style': style,
        'expertise': expertise,
        'model_path': model_path
    }

def export_data():
    shutil.copy(USER_FILE, 'user_profiles_backup.json')
    shutil.copy(ASSISTANT_FILE, 'assistant_profiles_backup.json')
    print('✅ Exported to user_profiles_backup.json and assistant_profiles_backup.json')

def import_data():
    try:
        with open('user_profiles_backup.json') as f:
            save_json(USER_FILE, json.load(f))
        with open('assistant_profiles_backup.json') as f:
            save_json(ASSISTANT_FILE, json.load(f))
        print('✅ Imported backup profiles.')
    except:
        print('⚠️ Failed to import. Check backup files exist.')

def edit_mode():
    print('\n🛠️ Edit Mode')
    print('1. Add/Edit user\n2. Remove user\n3. Add/Edit assistant\n4. Remove assistant\n5. Export profiles\n6. Import profiles\n7. Exit')

    user_profiles = load_json(USER_FILE)
    assistant_profiles = load_json(ASSISTANT_FILE)

    while True:
        choice = input('\nEnter choice: ').strip()
        if choice == '1':
            k, v = prompt_user_profile()
            user_profiles[k] = v
            save_json(USER_FILE, user_profiles)
            print(f'✅ Saved user {v["name"]}')
        elif choice == '2':
            name = input('Enter user name to remove: ').strip().lower()
            if name in user_profiles:
                confirm = input(f'⚠️ Are you sure you want to delete user {name}? (y/n): ').strip().lower()
                if confirm == 'y':
                    del user_profiles[name]
                    save_json(USER_FILE, user_profiles)
                    print(f'❌ Removed user {name}')
        elif choice == '3':
            k, v = prompt_assistant_profile()
            assistant_profiles[k] = v
            save_json(ASSISTANT_FILE, assistant_profiles)
            print(f'✅ Saved assistant {k}')
        elif choice == '4':
            name = input('Enter assistant name to remove: ').strip()
            if name in assistant_profiles:
                confirm = input(f'⚠️ Are you sure you want to delete assistant {name}? (y/n): ').strip().lower()
                if confirm == 'y':
                    del assistant_profiles[name]
                    save_json(ASSISTANT_FILE, assistant_profiles)
                    print(f'❌ Removed assistant {name}')
        elif choice == '5':
            export_data()
        elif choice == '6':
            import_data()
        elif choice == '7':
            break
        else:
            print('Invalid option.')

def run_setup():
    if os.path.exists(USER_FILE) and os.path.exists(ASSISTANT_FILE):
        return

    print('🛠️ First-time setup\n')

    user_profiles = {}
    assistant_profiles = {}

    print('👤 Add at least one user:')
    while True:
        k, v = prompt_user_profile()
        user_profiles[k] = v
        if input('Add another user? (y/n): ').strip().lower() != 'y':
            break
    save_json(USER_FILE, user_profiles)

    print('\n🤖 Add at least one assistant (press Enter to use default):')
    name = input('Assistant name: ').strip()
    if not name:
        assistant_profiles['Anaya'] = {
            'system_prompt': "You are Anaya, {user_name}'s best friend. Keep responses short and simple. Be warm and casual. Never sound like an assistant. Respond with care and lightness.",
            'tone': 'warm',
            'style': 'simple and friendly',
            'expertise': 'emotional support',
            'model_path': 'models/mistral-7b-instruct-v0.1.Q4_K_M.gguf'
        }
        print('✅ Using default assistant Anaya')
    else:
        k, v = prompt_assistant_profile(name)
        assistant_profiles[k] = v
        while input('Add another assistant? (y/n): ').strip().lower() == 'y':
            k, v = prompt_assistant_profile()
            assistant_profiles[k] = v

    save_json(ASSISTANT_FILE, assistant_profiles)
    print('\n🎉 Setup complete.')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'edit':
        edit_mode()
    else:
        run_setup()
