# emergency.py
import re
from datetime import datetime

# List of emergency trigger keywords
EMERGENCY_KEYWORDS = [
    r"help",
    r"emergency",
    r"save me",
    r"accident",
    r"fire",
    r"injured",
    r"bleeding",
    r"danger",
    r"not safe",
    r"please help",
    r"call police",
    r"call ambulance"
]

def detect_emergency(text: str):
    """Returns True if emergency keyword detected and the matched keyword."""
    text = text.lower()

    for word in EMERGENCY_KEYWORDS:
        if re.search(word, text):
            return True, word
    return False, None


def log_emergency_event(keyword, transcription):
    """Stores emergency event as a safe log entry."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("backend/emergency_log.txt", "a") as f:
        f.write(
            f"[{timestamp}] EMERGENCY TRIGGERED | keyword: {keyword} | text: {transcription}\n"
        )
