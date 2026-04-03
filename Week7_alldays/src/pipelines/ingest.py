import os
import fitz
import re
from tqdm import tqdm

RAW_PATH = "src/data/raw/"


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def load_pdf(path):
    doc = fitz.open(path)
    data = []

    for i, page in enumerate(doc):
        text = page.get_text()
        text = clean_text(text)

        if len(text) > 50:
            data.append({
                "text": text,
                "page": i + 1,
                "source": os.path.basename(path),
                "type": "pdf"
            })

    return data


def ingest():
    all_docs = []

    for file in tqdm(os.listdir(RAW_PATH)):
        path = os.path.join(RAW_PATH, file)

        if not file.lower().endswith(".pdf"):
           continue
        
        all_docs.extend(load_pdf(path))

    return all_docs