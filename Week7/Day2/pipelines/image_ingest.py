import os
import pickle
import faiss
import pytesseract
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import numpy as np

from embeddings.clip_embedder import CLIPEmbedder

#image -> embedding+ocr+caption
#images ko prepare karke searchable banana--->
#images folder read karta hai->OCR nikalta hai->BLIP caption banata hai->CLIP embedding banata hai->image_index.faiss save karta hai and image_metadata.pkl save karta hai
DATA_PATH = "data/raw/images"
VECTOR_PATH = "data/cleaned/vector_store"

os.makedirs(VECTOR_PATH, exist_ok=True)

embedder = CLIPEmbedder()

# BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    out = model.generate(**inputs, max_new_tokens=50)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return caption


def extract_ocr(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def ingest():  #image db bnana
    image_files = [
        f for f in os.listdir(DATA_PATH)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    embeddings = []
    metadata = []

    for img in image_files:
        path = os.path.join(DATA_PATH, img)
        print(f"Processing: {path}")

        emb = embedder.embed_image(path)
        caption = generate_caption(path)
        ocr_text = extract_ocr(path)

        embeddings.append(emb)
        metadata.append({
            "image_path": path,
            "caption": caption,
            "ocr_text": ocr_text
        })

    # build FAISS
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    embeddings = np.array(embeddings).astype("float32")
    index.add(embeddings)

    
    faiss.write_index(index, f"{VECTOR_PATH}/image_index.faiss")

    with open(f"{VECTOR_PATH}/image_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("Image ingestion complete")


if __name__ == "__main__":
    ingest()