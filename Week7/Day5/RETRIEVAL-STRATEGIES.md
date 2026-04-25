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

# context_builder.py
--> retrieval engine hai

## work:
query leta hai 
relevant chunks dhundhta hai
rerank krta hai
best chunks deta hai
simple:
query → search → best context

# rag_pipeline.py
ye main RAG logic hai

## work:
context_builder से chunks लेता है
prompt banata hai
LLM ko bhejta hai
answer deta hai
flow:
question → context → LLM → answer
5. user_rag_pipeline.py:

  user uploaded PDF ke liye same RAG है

# llm_client.py:
ye LLM wrapper hai

work:
Groq API call krna 
prompt bhejna
response lana
simple:
prompt → LLM → answer

# query engine flow:(query process karta)
User question
   ↓
query_engine(query process krta)
   ↓
hybrid_retriever(search krte)
   ↓
reranker(best chunta hai)
   ↓
best chunks

### MAIN ###----->
# RETRIEVAL STRATEGIES

## Overview

To improve retrieval accuracy, we use hybrid retrieval techniques.

## Methods Used

### 1. Semantic Search

* Uses embeddings
* Cosine similarity

### 2. Keyword Search (BM25)

* Exact word matching
* Handles edge cases

### 3. Hybrid Retrieval

Final score =
0.7 * semantic + 0.3 * keyword

### 4. Reranking

* Cross-encoder model
* Reorders results for better relevance

### 5. MMR (Max Marginal Relevance)

* Reduces duplicate chunks
* Improves diversity

## Context Optimization

* top_k = 5
* snippet trimming = 300 chars
* sentence filtering

## Benefits

* Higher precision
* Lower hallucination
* Better context relevance

## Command

```bash
python pipelines/context_builder.py
```
