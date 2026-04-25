import os
from PyPDF2 import PdfReader

def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    texts = []

    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except:
            t = ""
        if t.strip():
            texts.append(t)

    full = "\n".join(texts)

    # fallback 
    if len(full.strip()) < 50:
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(path)
            texts = [p.get_text() for p in doc]
            full = "\n".join(texts)
        except:
            pass

    return full