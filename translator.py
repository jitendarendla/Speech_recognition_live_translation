from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-hi-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
translator = MarianMTModel.from_pretrained(model_name)

def hindi_to_english(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = translator.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)
