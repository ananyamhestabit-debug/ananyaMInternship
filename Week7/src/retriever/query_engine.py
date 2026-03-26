from embeddings.embedder import embed_texts

def retrieve(query, vectorstore):
    """
    Convert query → embedding
    Retrieve similar chunks
    --> Basic semantic search
    """
    query_vec = embed_texts([query])
    return vectorstore.search(query_vec, k=5)