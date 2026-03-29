import pytesseract
from PIL import Image
import os
import json

def process_images(folder="src/data/raw"):
    results = []

    for file in os.listdir(folder):
        if file.endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(folder, file)

            image = Image.open(path)

            # OCR extraction
            text = pytesseract.image_to_string(image)

            results.append({
                "file": file,
                "ocr_text": text
            })

    os.makedirs("src/data/chunks", exist_ok=True)

    with open("src/data/chunks/image_metadata.json", "w") as f:
        json.dump(results, f, indent=4)

    return results