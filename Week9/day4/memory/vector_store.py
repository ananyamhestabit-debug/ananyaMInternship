"""
DAY 4 - Vector Memory (FAISS)
Stores text as embeddings and retrieves similar memories by cosine similarity.
Uses sentence-transformers for embeddings (CPU friendly, no GPU needed).
"""

import os
import json
import numpy as np

# FAISS and sentence-transformers imported lazily so errors are clear
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    VECTOR_AVAILABLE = True
except ImportError:
    VECTOR_AVAILABLE = False

VECTOR_STORE_PATH = "memory/vector_store.json"
model = None


def load_model():
    global model
    if model is None:
        # all-MiniLM-L6-v2 is small, fast, CPU-friendly
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def load_store() -> dict:
    # store = { "texts": [...], "embeddings": [[...], ...] }
    if os.path.exists(VECTOR_STORE_PATH):
        with open(VECTOR_STORE_PATH, "r") as f:
            return json.load(f)
    return {"texts": [], "embeddings": []}


def save_store(store: dict):
    os.makedirs("memory", exist_ok=True)
    with open(VECTOR_STORE_PATH, "w") as f:
        json.dump(store, f)


def add_to_vector_store(text: str):
    if not VECTOR_AVAILABLE:
        print("[VECTOR] faiss/sentence-transformers not installed, skipping")
        return

    m = load_model()
    embedding = m.encode([text])[0].tolist()

    store = load_store()
    store["texts"].append(text)
    store["embeddings"].append(embedding)
    save_store(store)
    print(f"[VECTOR] Stored: {text[:60]}...")


def search_similar(query: str, top_k: int = 3) -> list:
    # Returns list of most similar stored texts
    if not VECTOR_AVAILABLE:
        return []

    store = load_store()
    if not store["texts"]:
        return []

    m = load_model()
    query_embedding = m.encode([query])[0]

    embeddings = np.array(store["embeddings"]).astype("float32")
    query_vec = np.array([query_embedding]).astype("float32")

    # normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    faiss.normalize_L2(query_vec)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    distances, indices = index.search(query_vec, min(top_k, len(store["texts"])))

    results = []
    for i, idx in enumerate(indices[0]):
        if idx >= 0:
            results.append({
                "text": store["texts"][idx],
                "score": float(distances[0][i])
            })
    return results


def clear_vector_store():
    if os.path.exists(VECTOR_STORE_PATH):
        os.remove(VECTOR_STORE_PATH)
        print("[VECTOR] Store cleared")
