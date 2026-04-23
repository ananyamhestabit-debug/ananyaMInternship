import os
import pickle
import numpy as np
from nexus_ai.config import MEMORY_DIR

VECTOR_PATH = MEMORY_DIR / "vectors.pkl"

# Lazy imports so startup is fast
_model = None
_store = []  # list of (embedding, text)


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _load_store():
    global _store
    if VECTOR_PATH.exists():
        with open(VECTOR_PATH, "rb") as f:
            _store = pickle.load(f)
    return _store


def _save_store():
    with open(VECTOR_PATH, "wb") as f:
        pickle.dump(_store, f)


def store_vector(text):
    _load_store()
    model = _get_model()
    emb = model.encode(text)
    _store.append((emb, text))
    _save_store()


def search_similar(query, top_k=3):
    _load_store()
    if not _store:
        return []
    model = _get_model()
    q_emb = model.encode(query)
    scores = []
    for emb, text in _store:
        score = float(np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb) + 1e-9))
        scores.append((score, text))
    scores.sort(reverse=True)
    return [text for _, text in scores[:top_k]]
