import faiss
import pickle
import numpy as np
import re
from rank_bm25 import BM25Okapi
from embeddings.embedder import Embedder

INDEX_PATH = "src/vectorstore/index.faiss"
META_PATH = "src/vectorstore/meta.pkl"


class HybridRetriever:
    def __init__(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.meta = pickle.load(f)

        self.embedder = Embedder()

        # BM25 setup
        corpus = [doc["text"].lower().split() for doc in self.meta]
        self.bm25 = BM25Okapi(corpus)

    def clean_text(self, text):
        return re.sub(r"[^\w\s]", "", text.lower())

    def query(self, query, top_k=5):
        query_lower = query.lower()
        query_clean = self.clean_text(query)

        # -------- semantic search --------
        q_vec = self.embedder.embed_batch([query])
        q_vec = np.array(q_vec).astype("float32")

        D, I = self.index.search(q_vec, 10)

        sem_docs = []
        for idx, score in zip(I[0], D[0]):
            d = self.meta[idx].copy()
            d["sem_score"] = float(score)
            sem_docs.append(d)

        # -------- keyword search --------
        tokenized_query = query_clean.split()
        scores = self.bm25.get_scores(tokenized_query)
        top_idx = np.argsort(scores)[::-1][:10]

        key_docs = []
        for idx in top_idx:
            d = self.meta[idx].copy()
            d["bm25_score"] = float(scores[idx])
            key_docs.append(d)

        # -------- merge --------
        combined = {}

        for d in sem_docs:
            combined[d["text"]] = d

        for d in key_docs:
            if d["text"] in combined:
                combined[d["text"]]["bm25_score"] = d.get("bm25_score", 0)
            else:
                combined[d["text"]] = d

        docs = list(combined.values())

        # -------- FINAL HYBRID SCORING --------
        for d in docs:
            sem = d.get("sem_score", 0)
            bm25 = d.get("bm25_score", 0)

            text = d["text"].lower()
            text_clean = self.clean_text(text)

            score = (0.5 * sem) + (0.5 * bm25)

            # FULL PHRASE MATCH BOOST
            if query_clean in text_clean:
                score += 0.5

            # PARTIAL WORD MATCH BOOST
            for word in query_clean.split():
                if word in text_clean:
                    score += 0.08

            # EXTRA BOOST if multiple words match
            match_count = sum(1 for word in query_clean.split() if word in text_clean)
            if match_count >= 2:
                score += 0.15

            # PENALTY: noisy financial sections
            if "notes to the financial statements" in text:
                score -= 0.3
            if "statement of financial position" in text:
                score -= 0.2

            d["final_score"] = score

        # -------- sort --------
        docs = sorted(docs, key=lambda x: x["final_score"], reverse=True)

        return docs[:top_k]