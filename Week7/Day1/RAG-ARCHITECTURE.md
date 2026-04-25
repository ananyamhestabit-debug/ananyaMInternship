# RAG ARCHITECTURE

## Overview

This system implements a Retrieval-Augmented Generation (RAG) pipeline that enables answering questions from documents using embeddings and LLMs.

## Flow

1. Documents (PDF, TXT) are loaded
2. Text is cleaned and chunked (700 tokens, overlap 50)
3. Each chunk is converted into embeddings
4. Embeddings are stored in FAISS vector database
5. User query is embedded
6. Top-k similar chunks are retrieved
7. Context is passed to LLM
8. Final answer is generated

## Components

### 1. Ingestion Pipeline (`ingest.py`)

* Loads documents
* Splits into chunks
* Generates embeddings
* Stores FAISS index + metadata

### 2. Vector Store

* FAISS IndexFlatL2 used
* Fast similarity search over embeddings

### 3. Retriever

* Hybrid retrieval (semantic + keyword)
* Uses cosine similarity + BM25

### 4. Generator

* LLM generates answer from context

## Key Design Decisions

* Chunk size = 700 (balance context vs precision)
* Overlap = 50 (avoid context loss)
* Embeddings = sentence-transformers
* FAISS = scalable retrieval

## Command to Run

```bash
python pipelines/ingest.py
streamlit run app.py
```
