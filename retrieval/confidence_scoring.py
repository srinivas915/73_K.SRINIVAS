def compute_confidence(docs):
    if not docs:
        return 0.0
    return round(min(len(docs) / 5, 1.0), 2)
