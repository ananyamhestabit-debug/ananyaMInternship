from src.pipelines.ingest import ingest_data
from src.utils.chunker import chunk_text
from src.embeddings.embedder import generate_embeddings
from src.vectorstore.faiss_store import create_index, save_index
from src.utils.metadata_store import save_metadata
import json
import os

documents = ingest_data()

all_chunks = []
metadata = []

for doc in documents:
    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):
        all_chunks.append({
        "text": chunk,
        "chunk_id": i,
        "source": doc["metadata"]["source"]
    })

    metadata.append({
        "source": doc["metadata"]["source"],
        "type": doc["metadata"]["type"],
        "chunk_id": i
    })

print(f"Total chunks: {len(all_chunks)}")

# embeddings
embeddings = generate_embeddings(all_chunks)

# vector db
index = create_index(embeddings)
save_index(index)

# save metadata
save_metadata(metadata)

# save chunks (IMPORTANT FOR DAY 2)
os.makedirs("src/data/chunks", exist_ok=True)

with open("src/data/chunks/chunks.json", "w") as f:
    json.dump(all_chunks, f, indent=4)

print("Day 1 + Day 2 Base Setup Completed")