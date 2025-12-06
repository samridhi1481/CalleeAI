import speech_recognition as sr

def transcribe_audio(file_path):
    recog = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recog.record(source)

    try:
        return recog.recognize_google(audio)
    except:
        return "Could not understand audio."
