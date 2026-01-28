import soundfile as sf
import numpy as np
import librosa

from datasets import load_from_disk
from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Trainer,
    TrainingArguments
)

# -----------------------------
# 1. LOAD PREPARED DATASET
# -----------------------------
dataset = load_from_disk("prepared_dataset")

# 🔥 SPEED HACK: use only small subset
dataset = dataset.shuffle(seed=42).select(range(100))

# -----------------------------
# 2. LOAD FASTEST WHISPER MODEL
# -----------------------------
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")

# Force translation to English
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(
    language="en",
    task="translate"
)

# -----------------------------
# 3. PREPROCESS FUNCTION
# -----------------------------
def preprocess(batch):
    audio, sr = sf.read(batch["audio"])

    # Convert stereo → mono
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    # Resample to 16 kHz (MANDATORY)
    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

    batch["input_features"] = processor(
        audio,
        sampling_rate=16000
    ).input_features[0]

    batch["labels"] = processor.tokenizer(
        batch["sentence"],
        truncation=True,
        return_tensors="pt"
    ).input_ids[0]

    return batch


dataset = dataset.map(
    preprocess,
    remove_columns=dataset.column_names
)

# -----------------------------
# 4. FAST TRAINING CONFIG
# -----------------------------
training_args = TrainingArguments(
    output_dir="./trained_model",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=1e-4,
    max_steps=300,          # 🔥 more learning
    logging_steps=10,
    save_steps=300,
    save_total_limit=1,
    fp16=False,
    report_to="none"
)


# -----------------------------
# 5. TRAIN
# -----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

# -----------------------------
# 6. SAVE MODEL
# -----------------------------
model.save_pretrained("trained_model")
processor.save_pretrained("trained_model")

print("✅ FAST TRAINING COMPLETED")
