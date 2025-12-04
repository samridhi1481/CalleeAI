import uuid
import os

def text_to_speech(text: str) -> str:
    """
    Placeholder TTS.
    Instead of generating audio, we just save text as a .txt file.
    Later, we will add real TTS.
    """

    filename = f"tts_output_{uuid.uuid4().hex}.txt"
    filepath = os.path.join("uploads", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    return filepath
