import librosa
from transformers import pipeline

# -------- Transcription (force Hindi/Telugu detection) --------
transcriber = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    generate_kwargs={
        "language": "hi"   # change to "te" for Telugu audio
    }
)

# -------- Translation to English --------
translator = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    generate_kwargs={
        "task": "translate",
        "language": "en"
    }
)

audio_path = r"datasets\te\clips\common_voice_te_38821717.mp3"

audio, sr = librosa.load(audio_path, sr=16000)

original_text = transcriber(audio)["text"]
english_text = translator(audio)["text"]

print("\n🟡 Original Sentence (Hindi / Telugu):")
print(original_text)

print("\n🟢 English Translation:")
print(english_text)
