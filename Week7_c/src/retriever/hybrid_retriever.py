from rank_bm25 import BM25Okapi

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

        return [idx for idx, _ in ranked[:top_k]]