from fastapi import FastAPI, UploadFile, File
from utils.ocr_utils import extract_text
from utils.forensic_utils import detect_forgery
from PIL import Image
import io

app = FastAPI()

@app.post("/verify-bill/")
async def verify_bill(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))

    extracted_text = extract_text(image)
    is_fake, reason = detect_forgery(image, extracted_text)

    return {
        "status": "fake" if is_fake else "real",
        "reason": reason,
        "extracted_text": extracted_text
    }
