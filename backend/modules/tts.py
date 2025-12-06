from gtts import gTTS
import uuid
import os

def text_to_speech(text):
    filename = f"uploads/{uuid.uuid4()}.mp3"
    tts = gTTS(text)
    tts.save(filename)
    return filename
