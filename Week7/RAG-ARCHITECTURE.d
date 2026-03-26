# RAG Architecture — Day 1

## What this system does
This system reads documents (PDF, CSV, TXT, DOCX), breaks them into smaller chunks, converts them into embeddings, stores them in a vector database, and retrieves relevant results based on a user query.

---

## Flow

User Query  
→ Convert to embedding  
→ Search in FAISS  
→ Get top relevant chunks  
→ Return result with metadata  

---

## Steps Implemented

### 1. Load Documents
Loads files from `data/raw/`

Supported formats:
- PDF
- CSV
- TXT
- DOCX

Libraries used:
- PyPDFLoader
- CSVLoader
- TextLoader
- UnstructuredWordDocumentLoader

---

### 2. Clean Data + Metadata
Each document is cleaned and structured.

Metadata added:
- source (file path)
- page (page number)
- type (document)
- year (2024)

---

### 3. Chunking
Large text is split into smaller parts.

Configuration:
- chunk_size = 700
- overlap = 100

Reason:
- Maintains context
- Fits within model token limits

---

### 4. Embeddings
Model used:
- all-MiniLM-L6-v2

Purpose:
- Converts text into vectors
- Enables semantic similarity search

---

### 5. Vector Database (FAISS)
Stores embeddings for fast similarity search.

Files created:
- index.faiss
- data.pkl

---

### 6. Retrieval
User query is converted into embedding and matched with stored vectors.

Returns:
- Top relevant chunks
- Metadata for traceability

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

### Install packages
pip install langchain-community langchain-text-splitters sentence-transformers faiss-cpu pypdf pandas  
Used to install required dependencies

---

### Run pipeline
PYTHONPATH=src python3 src/pipelines/ingest.py  
Used to run the pipeline and resolve import paths

---

## Output

- Documents loaded from dataset
- Chunks created
- Embeddings generated
- FAISS database created
- Relevant results retrieved

---

## Result

The system works correctly and retrieves meaningful results from both CSV and PDF data.