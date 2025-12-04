def detect_emergency(text: str) -> bool:
    emergency_keywords = [
        "accident", "emergency", "help me", "bleeding", 
        "unconscious", "not breathing", "danger", "fire"
    ]

    text = text.lower()

    for word in emergency_keywords:
        if word in text:
            return True

    return False
