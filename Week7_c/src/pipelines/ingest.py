import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for i, page in enumerate(reader.pages):
        content = page.extract_text()
        if content:
            text += f"\n[PAGE {i}]\n" + content
    return text

def load_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_csv(path):
    df = pd.read_csv(path)
    return df.to_string()

def load_file(path):
    if path.endswith(".txt"):
        return load_txt(path)
    elif path.endswith(".pdf"):
        return load_pdf(path)
    elif path.endswith(".docx"):
        return load_docx(path)
    elif path.endswith(".csv"):
        return load_csv(path)
    return ""

def ingest_data(raw_dir="src/data/raw"):
    documents = []

    for file in os.listdir(raw_dir):
        path = os.path.join(raw_dir, file)
        text = load_file(path)

        if text.strip() == "":
            continue

        documents.append({
            "text": text,
            "metadata": {
                "source": file,
                "type": file.split(".")[-1]
            }
        })

    return documents