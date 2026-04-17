import os, json, yaml
from transformers import AutoTokenizer

# config load
BASE = os.path.dirname(__file__)
with open(os.path.join(BASE, "../config/config.yaml")) as f:
    cfg = yaml.safe_load(f)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def chunk_text_tokens(text, chunk_size, overlap):
    tokens = tokenizer.encode(text)
    chunks = []
    start, cid = 0, 0

    while start < len(tokens):
        end = start + chunk_size
        piece = tokenizer.decode(tokens[start:end])

        chunks.append({
            "chunk_id": f"user_{cid}",  # ⚠️ collision avoid
            "content": piece,
            "metadata": {"source": "user_pdf"}
        })

        start += chunk_size - overlap
        cid += 1

    return chunks


def create_user_chunks(pdf_text: str, save_path: str):
    chunks = chunk_text_tokens(
        pdf_text,
        cfg["chunk_size"],
        cfg["chunk_overlap"]
    )

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(chunks, f)

    return save_path, chunks