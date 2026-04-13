from retriever.image_search import ImageSearchEngine
from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration

# -------- INIT --------
engine = ImageSearchEngine()

# BLIP model load (only once)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


# -------- TEXT → IMAGE --------
def image_query_text(query):
    scores, indices = engine.search_by_text(query)

    results = []
    for score, idx in zip(scores, indices):
        data = engine.metadata[idx]

        results.append({
            "image": data["image_path"],
            "caption": data.get("caption", ""),
            "ocr": data.get("ocr_text", ""),
            "score": float(score)   # ✅ important
        })

    return results


# -------- IMAGE → IMAGE --------
def image_query_image(image_path):
    scores, indices = engine.search_by_image(image_path)

    results = []
    for score, idx in zip(scores, indices):
        data = engine.metadata[idx]

        results.append({
            "image": data["image_path"],
            "caption": data.get("caption", ""),
            "ocr": data.get("ocr_text", ""),
            "score": float(score)   # ✅ important
        })

    return results


# -------- IMAGE → TEXT (OCR + CAPTION) --------
def extract_image_text(image_path):
    image = Image.open(image_path).convert("RGB")

    # OCR extraction
    ocr_text = pytesseract.image_to_string(image)

    # Caption generation
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=50)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return {
        "caption": caption,
        "ocr": ocr_text.strip() if ocr_text else ""
    }