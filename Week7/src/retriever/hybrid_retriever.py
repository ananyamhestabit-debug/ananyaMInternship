# semantic search
from retriever.query_engine import retrieve

# keyword search
from retriever.keyword import keyword_search

def hybrid_search(query, vectorstore, chunks, bm25, tokenized):
    """
    semantic + keyword combine karta hai
    """

    # semantic (FAISS)
    semantic_results = retrieve(query, vectorstore)

    # keyword (BM25)
    keyword_results = keyword_search(query, bm25, tokenized, chunks)

    # combine results
    combined = semantic_results + keyword_results

    # remove duplicates
    unique = list({doc["text"]: doc for doc in combined}.values())

    return unique