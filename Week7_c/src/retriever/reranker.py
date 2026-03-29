import numpy as np

def rerank(query_embedding, doc_embeddings):
    scores = np.dot(doc_embeddings, query_embedding.T)
    return scores