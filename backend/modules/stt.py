import subprocess
import os

WHISPER_CPP_PATH = r"C:\Users\DELL\Desktop\whisper.cpp\whisper.cpp-master\build\bin\Release\whisper-cli.exe"
MODEL_PATH = r"C:\Users\DELL\Desktop\whisper.cpp\whisper.cpp-master\models\ggml-base.en.bin"

def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        return "Audio file not found!"

    output_txt = audio_path + ".txt"

    if os.path.exists(output_txt):
        os.remove(output_txt)

    cmd = [
        WHISPER_CPP_PATH,
        "-m", MODEL_PATH,
        "-f", audio_path,
        "-otxt",
        "--language", "en",
        "--no-timestamps"
    ]

    subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(output_txt):
        with open(output_txt, "r", encoding="utf-8") as f:
            return f.read().strip()

    return "Failed to transcribe audio!"
