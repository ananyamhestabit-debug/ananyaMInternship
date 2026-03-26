import os
import json

# Loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    UnstructuredWordDocumentLoader
)

# Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings
from embeddings.embedder import embed_texts

# Vector DB
from vectorstore.faiss_store import FAISSStore

# Retrieval
from retriever.keyword import build_bm25
from retriever.hybrid_retriever import hybrid_search
from retriever.reranker import rerank
from pipelines.context_builder import build_context


# LOAD DOCUMENTS

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


# CLEAN + METADATA
def clean_documents(docs):
    cleaned = []

    for doc in docs:
        source = doc.metadata.get("source", "")

        # detect type
        if source.endswith(".pdf"):
            doc_type = "policy"
        elif source.endswith(".csv"):
            doc_type = "product"
        elif source.endswith(".txt"):
            doc_type = "text"
        elif source.endswith(".docx"):
            doc_type = "document"
        else:
            doc_type = "unknown"

        cleaned.append({
            "text": doc.page_content.strip(),
            "metadata": {
                "source": source,
                "page": doc.metadata.get("page", 0),
                "type": doc_type,
                "year": "2024"
            }
        })

    return cleaned


# CHUNKING
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


# SAVE METADATA JSON
def save_metadata(chunks):
    os.makedirs("data/metadata", exist_ok=True)

    with open("data/metadata/metadata.json", "w") as f:
        json.dump(chunks, f, indent=2)

# MAIN PIPELINE
if __name__ == "__main__":

    print("\nLoading documents...")
    docs = load_documents("data/raw/")
    print("Documents:", len(docs))

    print("\nCleaning...")
    cleaned = clean_documents(docs)

    print("\nChunking...")
    chunks = chunk_documents(cleaned)
    print("Chunks:", len(chunks))

    # Save metadata
    save_metadata(chunks)
    print("Metadata JSON saved")

    # Prepare texts
    texts = [c["text"] for c in chunks]

    # Embeddings
    print("\nEmbedding...")
    embeddings = embed_texts(texts)

    # Vector DB
    print("\nCreating FAISS DB...")
    store = FAISSStore(dim=len(embeddings[0]))
    store.add(embeddings, chunks)
    store.save()
    print("FAISS saved")

    # SEARCH PIPELINE
    bm25, tokenized = build_bm25(texts)

    query = input("\nEnter your query: ") or "product price"

    print("\nHybrid Searching...")

    # Hybrid retrieval
    results = hybrid_search(query, store, chunks, bm25, tokenized)

    # Reranking
    reranked = rerank(query, results)

    # DEDUPLICATION
    unique_docs = []
    seen = set()

    for doc in reranked:
        if doc["text"] not in seen:
            unique_docs.append(doc)
            seen.add(doc["text"])


    # DYNAMIC FILTERING
    query_lower = query.lower()

    if any(word in query_lower for word in ["price", "product", "cost", "buy"]):
        filters = {"type": "product", "year": "2024"}

    elif any(word in query_lower for word in ["policy", "report", "company"]):
        filters = {"type": "policy", "year": "2024"}

    else:
        filters = None

    # Final context
    final = build_context(unique_docs, k=5, filters=filters)

    # OUTPUT
    print("\nFINAL RESULTS:\n")

    for i, r in enumerate(final):
        print(f"\nRESULT {i+1}")
        print("TEXT:", r["text"][:150])
        print("SOURCE:", r["metadata"]["source"])
        print("PAGE:", r["metadata"]["page"])
        print("TYPE:", r["metadata"]["type"])
        print("YEAR:", r["metadata"]["year"])
        print("------")