from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import librosa
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

# 🔥 ENABLE CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
transcriber = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)

translator = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    generate_kwargs={"task": "translate", "language": "en"}
)

@app.post("/translate")
async def translate_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            path = tmp.name

        audio, sr = librosa.load(path, sr=16000)

        original = transcriber(audio)["text"]
        english = translator(audio)["text"]

        return {
            "original_text": original,
            "english_translation": english
        }

    except Exception as e:
        return {
            "error": str(e)
        }
