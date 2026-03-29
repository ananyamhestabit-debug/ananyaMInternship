import faiss
import numpy as np
import json
from embeddings.embedder import generate_embeddings

index = faiss.read_index("src/vectorstore/index.faiss")

with open("src/data/chunks/metadata.json") as f:
    metadata = json.load(f)

def search(query, top_k=5):
    query_vec = generate_embeddings([query])

    D, I = index.search(np.array(query_vec), top_k)

    results = []
    for idx in I[0]:
        results.append(metadata[idx])

    return results