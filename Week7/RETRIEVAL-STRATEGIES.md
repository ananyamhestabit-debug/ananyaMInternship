# Retrieval Strategies (Day 2)

## 1. Hybrid Retrieval

The system uses a combination of:

- Semantic search (FAISS + embeddings)
- Keyword search (BM25)

This approach helps in:
- Understanding the meaning of queries (semantic)
- Matching exact terms when needed (keyword)

---

## 2. Reranking

After retrieving results, they are ranked again based on relevance.

- Uses similarity between query and chunks
- Improves the order of results

Note: More advanced models (like cross-encoders) can be added for better accuracy.

---

## 3. Deduplication

Duplicate or very similar chunks are removed before final selection.

- Simple comparison based on chunk content
- Keeps results clean and avoids repetition

---

## 4. Context Selection (Top-K)

Only a limited number of chunks are used as final context.

- Typically top 5 results are selected
- Helps stay within LLM token limits
- Improves response quality by reducing noise

---

## 5. Traceable Context

Each retrieved chunk includes metadata such as:

- Source file name
- Page number
- Chunk ID

This ensures:
- Transparency in answers
- Easy debugging and verification