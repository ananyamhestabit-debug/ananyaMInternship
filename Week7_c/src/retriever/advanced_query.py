import faiss
import json
import numpy as np

from src.embeddings.embedder import generate_embeddings
from src.retriever.hybrid_retriever import HybridRetriever
from src.pipelines.context_builder import build_context

# load FAISS
index = faiss.read_index("src/vectorstore/index.faiss")

# load metadata
with open("src/data/chunks/metadata.json") as f:
    metadata = json.load(f)

# load chunks
with open("src/data/chunks/chunks.json") as f:
    chunks = json.load(f)

# BM25 setup
bm25 = HybridRetriever(chunks)


def advanced_search(query, top_k=5):
    # semantic search
    query_vec = generate_embeddings([query])
    D, I = index.search(np.array(query_vec), top_k)

    semantic_idxs = I[0]

    # keyword search
    keyword_idxs = bm25.search(query, top_k)

    # combine results
    combined_idxs = list(set(semantic_idxs.tolist() + keyword_idxs))

    # fetch metadata
    results = [
    {
        "text": chunks[i],
        "source": metadata[i]["source"],
        "chunk_id": metadata[i]["chunk_id"]
    }
    for i in combined_idxs if i < len(metadata)
]

    # dedup + limit
    final = build_context(results, top_k)

    return final