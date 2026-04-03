import faiss
import pickle
import numpy as np
from embeddings.embedder import Embedder

INDEX_PATH = "src/vectorstore/index.faiss"
META_PATH = "src/vectorstore/meta.pkl"


class QueryEngine:
    def __init__(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.meta = pickle.load(f)

        self.embedder = Embedder()

    def query(self, query, top_k=5):
        q_vec = self.embedder.embed_batch([query])
        q_vec = np.array(q_vec).astype("float32")

        D, I = self.index.search(q_vec, top_k * 3)

        results = []

        for idx, score in zip(I[0], D[0]):
            data = self.meta[idx]

            if data["type"] != "pdf":
                continue

            results.append({
                "text": data["text"][:300],
                "source": data["source"],
                "page": data["page"],
                "score": float(score)  # now higher = better
            })

            if len(results) >= top_k:
                break

        return results