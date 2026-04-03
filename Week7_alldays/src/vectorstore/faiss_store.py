import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "src/vectorstore/index.faiss"
META_PATH = "src/vectorstore/meta.pkl"


class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, vectors, meta):
        self.index.add(np.array(vectors))
        self.metadata.extend(meta)

    def save(self):
        os.makedirs("src/vectorstore", exist_ok=True)

        faiss.write_index(self.index, INDEX_PATH)

        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)