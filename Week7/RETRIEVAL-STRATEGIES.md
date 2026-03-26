# Retrieval Strategies — Day 2

## Overview
This system improves retrieval accuracy using hybrid search, reranking, and filtering.

---

## Hybrid Retrieval
Two search methods are combined:
- Semantic search using FAISS and embeddings
- Keyword search using BM25

This ensures better matching of both meaning and exact words.

---

## Reranking
A CrossEncoder model is used to rank results based on relevance.

This improves the order of results and brings the most relevant content to the top.

---

## Deduplication
Duplicate chunks are removed after combining results from semantic and keyword search.

---

## Context Selection
Top 5 results are selected as final context.

---

## Filters
Metadata-based filtering is applied:
- year
- type

This ensures only relevant documents are selected.

---

## Commands Used

### Create virtual environment
python3 -m venv venv  
Used to create an isolated environment

---

### Activate environment
source venv/bin/activate  
Used to activate the environment

---

### Install dependencies
pip install langchain-community langchain-text-splitters sentence-transformers faiss-cpu pypdf pandas rank-bm25  
Used to install required libraries

---

### Run pipeline
PYTHONPATH=src python3 src/pipelines/ingest.py  
Used to run the system and resolve import paths

---

## Result
- Improved retrieval accuracy
- Better ranking of results
- Removal of duplicate data
- Filtered and traceable context output