# MULTIMODAL RAG (IMAGE SYSTEM)

## Overview

This system supports image understanding using CLIP, OCR, and captioning.

## Pipeline

### Image Ingestion (`image_ingest.py`)

* Load images
* Extract OCR text (Tesseract)
* Generate captions (BLIP)
* Generate embeddings (CLIP)
* Store FAISS index

### Image Search (`image_search.py`)

Supports:

* Text → Image
* Image → Image

### Image Pipeline (`image_pipeline.py`)

Acts as UI wrapper

## Modes

### 1. Local Mode

* Uses FAISS
* Searches only stored images

### 2. Global Mode

* Extract caption
* Uses web API to fetch images

## Embedding Strategy

* CLIP used for shared embedding space
* Enables cross-modal retrieval

## Commands

```bash
python pipelines/image_ingest.py
streamlit run app.py
```
