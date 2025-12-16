import os
from flask import Flask, render_template, request, jsonify

from asr import speech_to_hindi
from translator import hindi_to_english
from hindi_corrector import correct_hindi

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

history_data = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/history")
def history():
    return render_template("history.html", history=history_data)

@app.route("/translate", methods=["POST"])
def translate():
    audio = request.files["audio"]
    audio_path = os.path.join(UPLOAD_FOLDER, "input.wav")
    audio.save(audio_path)

    hindi_raw = speech_to_hindi(audio_path)
    hindi_corrected = correct_hindi(hindi_raw)
    english = hindi_to_english(hindi_corrected)

    entry = {
        "hindi": hindi_corrected,
        "english": english
    }

    history_data.insert(0, entry)

    return jsonify(entry)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

