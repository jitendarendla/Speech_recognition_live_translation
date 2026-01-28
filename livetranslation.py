import tkinter as tk
import threading
import sounddevice as sd
import numpy as np
import queue
import time
import librosa
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

# ===============================
# CONFIG
# ===============================
MIC_INDEX = 1
SAMPLE_RATE = 16000
DURATION = 5
MAX_SAMPLES = SAMPLE_RATE * DURATION

running = False
audio_queue = queue.Queue()

# ===============================
# LOAD MODELS
# ===============================
transcriber = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    generate_kwargs={"return_timestamps": False}
)

translator = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    generate_kwargs={
        "task": "translate",
        "language": "en",
        "return_timestamps": False
    }
)

# ===============================
# AUDIO CALLBACK
# ===============================
def callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

# ===============================
# LIVE TRANSLATION LOOP (FIXED)
# ===============================
def live_translate():
    global running

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        device=MIC_INDEX,
        channels=1,
        dtype="float32",
        callback=callback
    ):
        while running:
            # 🔥 Clear old audio every cycle
            with audio_queue.mutex:
                audio_queue.queue.clear()

            status_label.config(text="Listening...")

            frames = []
            start = time.time()

            while time.time() - start < DURATION:
                if not running:
                    return
                frames.append(audio_queue.get())

            audio = np.concatenate(frames).squeeze()
            audio = audio[:MAX_SAMPLES]

            level = np.max(np.abs(audio))
            if level < 0.01:
                status_label.config(text="Speak louder...")
                continue

            audio = librosa.resample(audio, orig_sr=SAMPLE_RATE, target_sr=16000)

            # Transcribe + Translate
            original = transcriber(audio)["text"]
            english = translator(audio)["text"]

            original_text.delete(1.0, tk.END)
            original_text.insert(tk.END, original)

            translated_text.delete(1.0, tk.END)
            translated_text.insert(tk.END, english)

            status_label.config(text="Translation updated")

            # 🔥 Small pause before next cycle
            time.sleep(0.5)

# ===============================
# BUTTON HANDLERS
# ===============================
def start_translation():
    global running
    if not running:
        running = True
        threading.Thread(target=live_translate, daemon=True).start()
        status_label.config(text="Started")

def stop_translation():
    global running
    running = False
    status_label.config(text="Stopped")

# ===============================
# GUI
# ===============================
root = tk.Tk()
root.title("Live Hindi / Telugu → English Translator")
root.geometry("600x500")

tk.Label(root, text="Live Speech Translator", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(
    root,
    text="🎤 Start Speaking",
    font=("Arial", 12),
    bg="green",
    fg="white",
    command=start_translation
).pack(pady=10)

tk.Button(
    root,
    text="⛔ Stop",
    font=("Arial", 12),
    bg="red",
    fg="white",
    command=stop_translation
).pack(pady=5)

status_label = tk.Label(root, text="Click Start Speaking", fg="blue")
status_label.pack(pady=5)

tk.Label(root, text="Original (Hindi / Telugu):").pack()
original_text = tk.Text(root, height=5, width=70)
original_text.pack(pady=5)

tk.Label(root, text="English Translation:").pack()
translated_text = tk.Text(root, height=5, width=70)
translated_text.pack(pady=5)

root.mainloop()
