import numpy as np

# Graceful import — agar sentence-transformers na ho toh fallback mode
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    _VECTOR_AVAILABLE = True
except ImportError:
    _VECTOR_AVAILABLE = False


class VectorStore:
    """
    FAISS-backed semantic memory.
    Falls back to keyword search if sentence-transformers/faiss not available.
    """

    def __init__(self):
        self.available = _VECTOR_AVAILABLE
        self.texts = []

        if self.available:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                self.index = faiss.IndexFlatL2(384)
            except Exception:
                self.available = False

    def add(self, text: str):
        self.texts.append(text)
        if self.available:
            try:
                emb = self.model.encode([text])
                self.index.add(np.array(emb).astype("float32"))
            except Exception:
                pass  # still stored in self.texts for keyword fallback

    def search(self, query: str, k: int = 3):
        if not self.texts:
            return []

        if self.available:
            try:
                q_vec = self.model.encode([query])
                D, I = self.index.search(np.array(q_vec).astype("float32"), k)
                return [self.texts[i] for i in I[0] if i < len(self.texts)]
            except Exception:
                pass

        # Keyword fallback
        q_words = set(query.lower().split())
        scored = []
        for t in self.texts:
            t_words = set(t.lower().split())
            score = len(q_words & t_words)
            if score > 0:
                scored.append((score, t))
        scored.sort(reverse=True)
        return [t for _, t in scored[:k]]

    @property
    def mode(self):
        return "faiss" if self.available else "keyword"
