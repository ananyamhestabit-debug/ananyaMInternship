from rank_bm25 import BM25Okapi

def build_bm25(texts):
    tokenized = [t.split() for t in texts]
    return BM25Okapi(tokenized), tokenized


def keyword_search(query, bm25, tokenized, chunks, k=5):
    """
    keyword search with metadata
    """

    query_tokens = query.split()

    scores = bm25.get_scores(query_tokens)

    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    return [chunks[i] for i in top_idx]