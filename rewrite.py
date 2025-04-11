# myAI/rewrite.py

def rewrite_for_tone(text, user_profile, config):
    if not config.get("response_rewriting", True):
        return text

    name = user_profile.get("name", "friend")
    replacements = {
        "Keyur": name,
        "Can I help you": "Want to talk about it?",
        "How can I assist you": "Anything you want to share?",
        "Want me to do something for you": "Let's just chat if you want."
    }

    for src, tgt in replacements.items():
        text = text.replace(src, tgt)

    return text
