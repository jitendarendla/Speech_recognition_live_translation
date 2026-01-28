from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/translate")
async def translate(file: UploadFile = File(...)):
    # ⚠️ demo response for cloud
    return {
        "original": "नमस्ते दुनिया",
        "translation": "Hello world"
    }
