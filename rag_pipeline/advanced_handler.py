import re

def detect_intent(query: str):
    q = query.lower().strip()

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    gratitude = ["thanks", "thank you"]
    farewells = ["bye", "exit", "quit"]

    if q in greetings:
        return "GREETING"
    if q in gratitude:
        return "THANKS"
    if q in farewells:
        return "EXIT"

    # Very short or meaningless input
    if len(q) < 4:
        return "INVALID"

    return "TELECOM_QUERY"


def is_low_information_query(query: str):
    vague_patterns = [
        r"help",
        r"problem",
        r"issue",
        r"not working",
        r"slow",
        r"error"
    ]
    return any(re.fullmatch(p, query.lower()) for p in vague_patterns)
