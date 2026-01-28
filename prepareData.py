import pandas as pd
from datasets import Dataset
from pathlib import Path

def load_common_voice(tsv_path, clips_dir, language):
    df = pd.read_csv(tsv_path, sep="\t")
    data = []

    for _, row in df.iterrows():
        audio_path = Path(clips_dir) / row["path"]
        if audio_path.exists():
            data.append({
                "audio": str(audio_path),
                "sentence": row["sentence"],
                "language": language
            })
    return data


# 🔹 CHANGE THESE PATHS TO MATCH YOUR FOLDERS
hi_data = load_common_voice(
    "datasets/mcv-scripted-hi-v23.0/train.tsv",
    "datasets/mcv-scripted-hi-v23.0/clips",
    "hi"
)

te_data = load_common_voice(
    "datasets/te/train.tsv",
    "datasets/te/clips",
    "te"
)


dataset = Dataset.from_list(hi_data + te_data)
dataset.save_to_disk("prepared_dataset")

print("Dataset prepared successfully!")
