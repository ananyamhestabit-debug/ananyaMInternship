from rank_bm25 import BM25Okapi
import json

# LOAD CHUNKS
with open("src/data/chunks/chunks.json") as f:
    chunks = json.load(f)

# EXTRACT TEXT
documents = [chunk["text"] for chunk in chunks]


class HybridRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.tokenized = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized)

    def search(self, query, top_k=5):
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            list(enumerate(scores)),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]   # 🔥 return index + score


# INIT
retriever = HybridRetriever(documents)


# FINAL FUNCTION (USED IN DAY 5)
def advanced_search(query, top_k=5):

    ranked_results = retriever.search(query, top_k)

    results = []

    for idx, score in ranked_results:
        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "chunk_id": chunks[idx]["chunk_id"],
            "score": float(score)
        })

    return results