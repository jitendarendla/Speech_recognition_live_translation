import os

# 🔥 FORCE FFMPEG PATH FOR FLASK + WHISPER
os.environ["PATH"] += os.pathsep + r"C:\Users\jiten\Downloads\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"

import whisper

model = whisper.load_model("small")  # Neural network

def speech_to_hindi(audio_path):
    result = model.transcribe(audio_path, language="hi")
    return result["text"]
