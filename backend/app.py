import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
CORS(app)

# Create folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("audio", exist_ok=True)


# ------------------------ SPEECH TO TEXT -------------------------
def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio_data)
    except:
        return "Could not understand the audio."


# ------------------------ TEXT TO SPEECH -------------------------
def text_to_speech(text):
    filename = f"audio_{uuid.uuid4()}.mp3"
    filepath = os.path.join("audio", filename)

    tts = gTTS(text=text, lang="en")
    tts.save(filepath)

    return filename


# ------------------------ AI ENGINE (Gemini API) ------------------------
def ask_ai(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    headers = { "Content-Type": "application/json" }
    params = { "key": GEMINI_API_KEY }

    data = {
        "contents": [
            { "parts": [ { "text": prompt } ] }
        ]
    }

    response = requests.post(url, headers=headers, json=data, params=params)
    res = response.json()

    try:
        return res["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Sorry, I could not process that."


# ------------------------ ROUTES ------------------------
@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    file = request.files["audio"]
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    text = speech_to_text(filepath)
    return jsonify({"text": text})


@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.json["text"]

    ai_reply = ask_ai(user_text)
    audio_file = text_to_speech(ai_reply)

    return jsonify({
        "reply": ai_reply,
        "audio": f"audio/{audio_file}"
    })


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory("audio", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
