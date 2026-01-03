CONFIDENCE_THRESHOLD = 0.6

def check_escalation(response):
    return response["confidence"] < CONFIDENCE_THRESHOLD
