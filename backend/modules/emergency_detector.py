def detect_emergency(text):
    emergency_keywords = ["help", "emergency", "danger", "fire", "hurt", "accident"]
    text_lower = text.lower()

    for w in emergency_keywords:
        if w in text_lower:
            return True

    return False
