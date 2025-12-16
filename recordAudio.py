import sounddevice as sd
import scipy.io.wavfile as wav

def record_audio(seconds=5, filename="input.wav"):
    fs = 16000
    print("🎤 Speak in Hindi...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, audio)
    print("✅ Recording saved")
