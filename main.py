import os
os.environ["PATH"] += os.pathsep + r"C:\Users\jiten\Downloads\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"

from recordAudio import record_audio
from asr import speech_to_hindi
from translator import hindi_to_english
from hindi_corrector import correct_hindi

# Record audio
record_audio(seconds=4, filename="input.wav")

# Speech → Hindi text
hindi_text = speech_to_hindi("input.wav")
print("Hindi (raw):", hindi_text)

# ✅ Correct Hindi
hindi_text_corrected = correct_hindi(hindi_text)
print("Hindi (corrected):", hindi_text_corrected)

# Hindi → English
english_text = hindi_to_english(hindi_text_corrected)
print("English Translation:", english_text)
