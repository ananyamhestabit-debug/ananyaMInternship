import os
import cv2
import pytesseract
from tqdm import tqdm
from embeddings.clip_embedder import CLIPEmbedder
from utils.logger import log_info, log_error
import numpy as np
import faiss
import pickle

IMAGE_PATH = "src/data/raw/images/"
INDEX_PATH = "src/vectorstore/image_index.faiss"
META_PATH = "src/vectorstore/image_meta.pkl"


def clean_ocr(text):
    words = text.split()

    # remove garbage words
    clean = []
    for w in words:
        if any(c.isalpha() for c in w) and len(w) > 2:
            clean.append(w)

    return " ".join(clean)


def extract_text(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # adaptive threshold (better for charts)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    thresh = cv2.resize(thresh, None, fx=2, fy=2)

    config = r'--oem 3 --psm 11'   # sparse text mode

    text = pytesseract.image_to_string(thresh, config=config)

    return text.strip()


def ingest_images():
    embedder = CLIPEmbedder()

    vectors = []
    metadata = []

    files = os.listdir(IMAGE_PATH)

    for file in tqdm(files):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        log_info(f"[INGEST] Processing: {file}")

        path = os.path.join(IMAGE_PATH, file)

        try:
            vec = embedder.embed_image(path)
            log_info(f"[EMBED] Shape: {vec.shape}")

            ocr = extract_text(path)

            vectors.append(vec)

            metadata.append({
                "file": file,
                "path": path,
                "ocr": ocr
            })

        except Exception as e:
            log_error(str(e))

    vectors = np.vstack(vectors).astype("float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    os.makedirs("src/vectorstore", exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    log_info("INDEX BUILT")

if __name__=="__main__":
    ingest_images()