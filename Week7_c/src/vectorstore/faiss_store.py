import faiss
import numpy as np
import os

def create_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def save_index(index, path="src/vectorstore/index.faiss"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)