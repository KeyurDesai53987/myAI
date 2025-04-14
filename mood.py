from transformers import pipeline

_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', return_all_scores=True)

def detect_mood(text):
    results = _classifier(text)[0]
    top = max(results, key=lambda x: x['score'])
    return top['label'].lower(), top['score']
