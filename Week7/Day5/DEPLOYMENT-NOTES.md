# Enterprise Knowledge Intelligence System — Documentation

---

## 1. Overview

This project implements a multimodal Generative AI system capable of:

- Answering questions from textual documents
- Retrieving and analyzing images
- Converting natural language queries into SQL and executing them

The system integrates multiple AI and data processing components into a unified pipeline.

### Technology Stack

- Streamlit (User Interface)
- FAISS (Vector Database)
- Sentence Transformers (Text Embeddings)
- SQLite (Structured Data)
- CLIP (Image Embeddings)
- LLM APIs (Groq/OpenAI/Gemini)

---

## 2. Project Structure

```

src/
├── app.py
├── pipelines/
├── generator/
├── retriever/
├── embeddings/
├── memory/
├── evaluation/
├── utils/
├── data/
├── database/

````

---

## 3. Setup Instructions

### 3.1 Clone Repository

```bash
git clone <repository-url>
cd Week7/src
````

---

### 3.2 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3.4 Configure Environment Variables

```bash
export GROQ_API_KEY=your_api_key
```

---

## 4. Database Setup

```bash
python database/sample_db.py
```

This creates:

* `sample.db`
* Sample dataset for SQL queries

---

## 5. Document Ingestion Pipeline

```bash
python pipelines/ingest.py

python pipelines/image_ingest.py
```

This step:

* Loads documents (PDF, TXT, DOCX) and images
* Splits them into chunks
* Generates embeddings
* Stores vectors in FAISS

---

## 6. Running the Application

```bash
streamlit run app.py
```

Access the application at:

```
http://localhost:8501
```

---

## 7. System Capabilities

### 7.1 Text-based Retrieval (RAG)

* Hybrid retrieval (semantic + keyword)
* Context reranking
* Session-based memory
* Hallucination detection
* Confidence scoring

---

### 7.2 SQL Question Answering

* Natural language to SQL conversion
* Schema-aware query generation
* Safe execution on SQLite
* Result summarization

---

### 7.3 Image Retrieval System

Supports:

* Text to image retrieval
* Image similarity search
* Image to text extraction (OCR + captions)

---

## 8. Retrieval Strategies

Efficient retrieval is critical for generating accurate responses.
The system uses a combination of multiple retrieval techniques.

---

### 8.1 Semantic Retrieval

Uses vector embeddings to capture meaning.

* Model: Sentence Transformers
* Storage: FAISS
* Similarity: Cosine similarity

**Advantage:** Handles paraphrased queries effectively.

---

### 8.2 Keyword-Based Retrieval (BM25)

Uses statistical matching for exact keyword relevance.

* Library: rank-bm25
* Algorithm: BM25Okapi

**Advantage:** Strong for exact matches.

---

### 8.3 Hybrid Retrieval

Combines semantic and keyword approaches.

**Workflow:**

1. Perform semantic search
2. Perform keyword search
3. Merge results
4. Rank final outputs

**Benefit:** Improves recall and precision.

---

### 8.4 Reranking

Reorders retrieved results based on relevance.

* Uses similarity scoring
* Can be extended to cross-encoders

---

### 8.5 Top-K Selection

Only top relevant chunks are used.

* User-controlled (via UI slider)
* Default limit: 5

**Purpose:** Reduces noise and improves answer quality.

---

### 8.6 Context Deduplication

Removes repeated or redundant chunks.

---

### 8.7 Context Construction

Final input to LLM includes:

* Selected chunks
* Metadata (source, page)
* Ranked order

---

### 8.8 Image Retrieval Strategy

Separate pipeline using:

* CLIP embeddings
* FAISS search
* OCR extraction
* Caption matching

Supports:

* Text → Image
* Image → Image
* Image → Text

---

### 8.9 SQL Query Strategy

Instead of retrieval:

1. Convert natural language to SQL
2. Validate query
3. Execute on database
4. Summarize results

---

### 8.10 Hallucination Reduction

Implemented using:

* Context-grounded responses
* Hybrid retrieval
* Top-K filtering
* Evaluation scoring

---

## 9. Evaluation Metrics

* Hallucination Score
* Confidence Score
* Context Traceability

---

## 10. Memory System

* Stores recent interactions
* Improves conversational continuity
* Session-based (non-persistent)

---

## 11. Logging

Logs are stored in:

```
logs/CHAT-LOGS.json
```

Each log contains:

* Query
* Response
* Confidence score
* Hallucination score

---

## 12. Important Notes

### Virtual Environment

```
venv/
```

Should be added to `.gitignore`

---

### Temporary Data

* Uploaded images are not permanently stored
* Processing is temporary

---

### API Security

Do not commit:

* `.env` files
* API keys

---

## 13. Deployment Options

### Local Deployment

```bash
streamlit run app.py
```

---

### Cloud Deployment

* Push to GitHub
* Deploy via Streamlit Cloud
* Add environment variables

---

### Containerization (Optional)

* Use Python base image
* Expose port 8501

---

## 14. Testing Checklist

* RAG returns accurate answers with context
* SQL queries execute correctly
* Image retrieval works properly
* Memory retains recent interactions
* Logs are generated correctly

---

## 15. Outcome

This system demonstrates:

* End-to-end RAG pipeline
* Multimodal retrieval (text + image)
* Natural language SQL querying
* Memory integration
* Evaluation metrics
* Modular architecture

---

## 16. Future Enhancements

* Persistent memory (Redis)
* Advanced reranking (cross-encoder)
* Streaming responses
* UI improvements
* Cloud deployment (AWS/GCP)

### Production Considerations
Use vector DB like Pinecone/Qdrant
Add caching layer
Use async APIs
Add logging & monitoring

### Limitations
Depends on embedding quality
SQL generation not perfect
Image search limited by model

