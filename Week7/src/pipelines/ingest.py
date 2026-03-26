import os
import json

# Loaders for PDF, CSV, TXT, DOCX
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    UnstructuredWordDocumentLoader
)

# Text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings
from embeddings.embedder import embed_texts

# Vector database
from vectorstore.faiss_store import FAISSStore

# Basic retriever
from retriever.query_engine import retrieve

# Day 2 modules
from retriever.keyword import build_bm25
from retriever.hybrid_retriever import hybrid_search
from retriever.reranker import rerank
from pipelines.context_builder import build_context


# Load documents from folder
def load_documents(folder_path):
    docs = []

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())

        elif file.endswith(".csv"):
            docs.extend(CSVLoader(path).load())

        elif file.endswith(".txt"):
            docs.extend(TextLoader(path).load())

        elif file.endswith(".docx"):
            docs.extend(UnstructuredWordDocumentLoader(path).load())

    return docs


# Clean text and add metadata
def clean_documents(docs):
    cleaned = []

    for doc in docs:
        cleaned.append({
            "text": doc.page_content.strip(),
            "metadata": {
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page", 0),
                "type": "document",
                "year": "2024"
            }
        })

    return cleaned


# Split documents into chunks
def chunk_documents(cleaned_docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = []

    for doc in cleaned_docs:
        split_texts = splitter.split_text(doc["text"])

        for chunk in split_texts:
            chunks.append({
                "text": chunk,
                "metadata": doc["metadata"]
            })

    return chunks


# Save chunks to file
def save_chunks(chunks):
    with open("data/chunks/chunks.json", "w") as f:
        json.dump(chunks, f)


# Main pipeline
if __name__ == "__main__":

    # Load data
    print("\nLoading documents...")
    docs = load_documents("data/raw/")
    print("Documents:", len(docs))

    # Clean data
    print("\nCleaning...")
    cleaned = clean_documents(docs)

    # Create chunks
    print("\nChunking...")
    chunks = chunk_documents(cleaned)
    print("Chunks:", len(chunks))

    save_chunks(chunks)

    # Generate embeddings
    texts = [c["text"] for c in chunks]

    print("\nEmbedding...")
    embeddings = embed_texts(texts)

    # Create FAISS vector database
    print("\nCreating FAISS DB...")
    store = FAISSStore(dim=len(embeddings[0]))

    store.add(embeddings, chunks)
    store.save()

    print("FAISS saved")

    # Build BM25 for keyword search
    bm25, tokenized = build_bm25(texts)

    # Query
    query = "product price"

    print("\nHybrid Searching...")

    # Hybrid search (semantic + keyword)
    results = hybrid_search(query, store, chunks, bm25, tokenized)

    # Rerank results
    reranked = rerank(query, results)

    # Apply filters
    filters = {
        "year": "2024",
        "type": "document"
    }

    # Get final top results
    final = build_context(reranked, k=5, filters=filters)

    # Print results
    print("\nFINAL RESULTS:\n")

    for r in final:
        print("TEXT:", r["text"][:150])
        print("META:", r["metadata"])
        print("------")