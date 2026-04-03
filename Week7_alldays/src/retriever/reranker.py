import numpy as np
from embeddings.embedder import Embedder


class Reranker:
    def __init__(self):
        self.embedder = Embedder()

    def rerank(self, query, docs):
        texts = [d["text"] for d in docs]

        q_vec = self.embedder.embed_batch([query])[0]
        doc_vecs = self.embedder.embed_batch(texts)

        scores = []

        for vec in doc_vecs:
            score = np.dot(q_vec, vec)
            scores.append(score)

        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

        return [r[0] for r in ranked]