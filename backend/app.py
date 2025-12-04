from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import subprocess

from modules.stt import transcribe_audio
from modules.ai_engine import generate_reply
from modules.emergency_detector import detect_emergency
from modules.tts import text_to_speech

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------
# Convert WebM → WAV using FFmpeg
# --------------------------
def convert_webm_to_wav(webm_path):
    wav_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.wav")

    cmd = ["ffmpeg", "-y", "-i", webm_path, wav_path]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return wav_path


# --------------------------
#  TRANSCRIBE ROUTE
# --------------------------
@app.route("/transcribe", methods=["POST"])
def transcribe_route():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]

    # Save uploaded WebM
    webm_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.webm")
    audio_file.save(webm_path)

    # Convert WebM → WAV
    wav_path = convert_webm_to_wav(webm_path)

    # Send to Whisper.cpp
    text = transcribe_audio(wav_path)

    return jsonify({"text": text})


# --------------------------
#  CHAT ROUTE
# --------------------------
@app.route("/chat", methods=["POST"])
def chat_route():
    data = request.json
    user_text = data.get("text", "")

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    emergency = detect_emergency(user_text)
    reply = generate_reply(user_text)
    audio_path = text_to_speech(reply)

    return jsonify({
        "reply": reply,
        "audio": audio_path,
        "emergency": emergency
    })


@app.route("/", methods=["GET"])
def home():
    return "CalleeAI backend running successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
