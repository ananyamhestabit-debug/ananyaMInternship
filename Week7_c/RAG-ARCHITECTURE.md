# DAY 1 — LOCAL RAG SYSTEM

## Objective

The goal of Day 1 is to build a basic Retrieval-Augmented Generation (RAG) pipeline that:

- Loads multiple file formats (PDF, CSV, TXT, DOCX)  
- Splits text into chunks (500–800 tokens)  
- Generates embeddings for each chunk  
- Stores embeddings in a FAISS vector database  
- Retrieves relevant chunks based on user queries  

---

## Data Used

The project uses the following raw data:

- An enterprise-level PDF (10-K report)  
- A CSV dataset  
- Some images (for future use in multimodal RAG)  

The PDF is the primary data source because it contains detailed textual information.

---

## Pipeline Flow

The pipeline works as follows:

1. Load raw data (PDF, CSV, TXT, DOCX)  
2. Extract and clean text  
3. Split text into chunks (500–800 tokens)  
4. Generate embeddings for each chunk  
5. Store embeddings in FAISS  
6. Save metadata in a JSON file  
7. Retrieve relevant chunks based on query  

---

## How to Run the Pipeline

### Step 1: Navigate to project root
cd /home/ananyamishra/re_assignment/Week7_c

### Step 2: Run the ingestion pipeline
python -m src.pipelines.run_ingest

## Expected Output (Terminal)
Total chunks: XXXX
Day 1 Completed Successfully


---

## Output Files

### FAISS Index


src/vectorstore/index.faiss


This file stores embeddings and is used for similarity search.

---

### Metadata JSON


src/data/chunks/metadata.json


Example:

```json
[
  {
    "source": "NextNav.pdf",
    "type": "pdf",
    "chunk_id": 0
  }
]

This file stores metadata for each chunk and is used during retrieval.

Query Testing
Step 1: Open Python
python
Step 2: Run query
from src.retriever.query_engine import search

results = search("What is TerraPoiNT?", 3)
print(results)
Output Example
[
  {'source': 'NextNav.pdf', 'type': 'pdf', 'chunk_id': 12},
  {'source': 'NextNav.pdf', 'type': 'pdf', 'chunk_id': 18}
]
