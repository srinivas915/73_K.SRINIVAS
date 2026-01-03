def compute_advanced_confidence(docs, answer_text):
    if not docs:
        return 0.0

    base_conf = min(len(docs) / 5, 1.0)

    # Penalize uncertainty phrases
    uncertainty_phrases = [
        "i don't know",
        "i don't have",
        "not available in the context",
        "cannot determine"
    ]

    if any(p in answer_text.lower() for p in uncertainty_phrases):
        base_conf *= 0.3

    # Penalize extremely short answers
    if len(answer_text.split()) < 6:
        base_conf *= 0.5

    return round(base_conf, 2)
