import requests
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # from .env

def generate_reply(text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GOOGLE_API_KEY

    body = {
        "contents": [
            {"parts": [{"text": text}]}
        ]
    }

    response = requests.post(url, json=body)
    data = response.json()

    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "Sorry, I could not understand. Please say again."

    return reply
