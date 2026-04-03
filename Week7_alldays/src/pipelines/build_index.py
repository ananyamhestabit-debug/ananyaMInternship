from pipelines.ingest import ingest
from pipelines.chunker import chunk_text
from embeddings.embedder import Embedder
from vectorstore.faiss_store import VectorStore
from utils.logger import log
from tqdm import tqdm


def build():
    log("Starting ingestion")

    docs = ingest()
    log(f"Documents loaded: {len(docs)}")

    all_chunks = []
    metadata = []

    log("Chunking documents")

    for doc in tqdm(docs):
        chunks = chunk_text(doc["text"])

        for chunk in chunks:
            text = chunk.lower()

            # LIGHT FILTER (correct approach)
            if "contents" in text:
                continue
            if "officers and professional advisers" in text:
                continue
            if len(chunk.split()) < 30:
                continue

            all_chunks.append(chunk)

            metadata.append({
                "text": chunk,
                "source": doc["source"],
                "page": doc["page"],
                "type": doc["type"]
            })

    log(f"Total chunks: {len(all_chunks)}")

    log("Generating embeddings")

    embedder = Embedder()
    vectors = embedder.embed_batch(all_chunks)

    log("Building FAISS index")

    vs = VectorStore(dim=len(vectors[0]))
    vs.add(vectors, metadata)
    vs.save()

    log("Index saved successfully")
    log("Day 2 indexing completed")


if __name__ == "__main__":
    build()