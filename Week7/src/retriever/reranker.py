from sentence_transformers import CrossEncoder

# reranking model
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, docs):
    """
    best documents ko upar laata hai
    """

    # pair: (query, doc text)
    pairs = [(query, doc["text"]) for doc in docs]

    scores = reranker.predict(pairs)   # relevance scores

    # score ke basis pe sort
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked]