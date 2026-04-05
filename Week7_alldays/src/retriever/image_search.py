import faiss
import pickle
import numpy as np
from embeddings.clip_embedder import CLIPEmbedder
from utils.logger import log_info

INDEX_PATH = "src/vectorstore/image_index.faiss"
META_PATH = "src/vectorstore/image_meta.pkl"


def fix_vector(vec):
    return np.array(vec).reshape(1, -1).astype("float32")


class ImageSearch:
    def __init__(self):
        log_info("[INIT] Loading FAISS index...")

        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.meta = pickle.load(f)

        self.embedder = CLIPEmbedder()

        log_info("[INIT] ImageSearch ready")


    # TEXT → IMAGE
    def search_by_text(self, query, top_k=5):
        log_info(f"[SEARCH TEXT] {query}")

        query_lower = query.lower()

        q_vec = fix_vector(self.embedder.embed_text(query))

        D, I = self.index.search(q_vec, 20)

        results = []

        for idx, score in zip(I[0], D[0]):
            if idx >= len(self.meta):
                continue

            data = self.meta[idx]
            filename = data["file"].lower()
            ocr_text = data.get("ocr", "").lower()

            boost = 0

            # TYPE BOOST 
            if "pie" in query_lower and "pie" in filename:
                boost += 0.6
            if "bar" in query_lower and "bar" in filename:
                boost += 0.6
            if "graph" in query_lower and "graph" in filename:
                boost += 0.6

            # OCR BOOST 
            if any(word in ocr_text for word in query_lower.split()):
                boost += 0.2

            final_score = float(score) + boost

            results.append({
                **data,
                "score": final_score
            })

        # sort
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        log_info(f"[RESULTS FOUND] {len(results)}")

        return results[:top_k]

    # IMAGE → IMAGE
    def search_by_image(self, image_path, top_k=5):
        log_info(f"[SEARCH IMAGE] {image_path}")

        q_vec = fix_vector(self.embedder.embed_image(image_path))

        name = image_path.lower()

        # detect type from input image
        query_type = ""
        if "pie" in name:
            query_type = "pie"
        elif "bar" in name:
            query_type = "bar"
        elif "graph" in name:
            query_type = "graph"

        D, I = self.index.search(q_vec, 20)

        results = []

        for idx, score in zip(I[0], D[0]):
            if idx >= len(self.meta):
                continue

            data = self.meta[idx]
            filename = data["file"].lower()

#strict filter
            if query_type and query_type not in filename:
                continue

            results.append({
                **data,
                "score": float(score)
            })

        # SORT
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        log_info(f"[RESULTS FOUND] {len(results)}")

        return results[:top_k]