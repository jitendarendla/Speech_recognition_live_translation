# Simple Hindi correction dictionary
CORRECTIONS = {
    "महुत": "बहुत",
    "अच्चा": "अच्छा",
    "अचा": "अच्छा",
    "है": "है"
}

def correct_hindi(text):
    words = text.split()
    corrected = [CORRECTIONS.get(w, w) for w in words]
    return " ".join(corrected)
