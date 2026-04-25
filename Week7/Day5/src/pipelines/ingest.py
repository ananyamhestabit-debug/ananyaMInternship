import os
import json
import yaml
import pickle  #metadat save/python object save
from utils.file_loader import load_text_files
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np  # vector db + array
from transformers import AutoTokenizer #hugging face ka smart loader

#PDF -> text -> chunks -> embeddings -> FAISS(vector DB)
# load config.yaml
with open(os.path.join(os.path.dirname(__file__), "../config/config.yaml")) as f:
    config = yaml.safe_load(f)

# tokenizer (token-based chunking)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

#chunking
def chunk_text(text, chunk_size=700, overlap=50):
    tokens = tokenizer.encode(text)

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(tokens): 
        end = start + chunk_size
        chunk_tokens = tokens[start:end] #slice
        chunk_content = tokenizer.decode(chunk_tokens)  #tokens->readable text

        chunks.append({
            "chunk_id": chunk_id,
            "content": chunk_content
        }) # <-- chunk store

        start += chunk_size - overlap  # overlap logic=700 size, 50 overlap -> next start = 650
        chunk_id += 1

    return chunks


# CREATE CHUNKS (pdf-> chunks.json)
def create_chunks(data_folder, save_folder):
    os.makedirs(save_folder, exist_ok=True)

    texts = load_text_files(data_folder) # loads pdf

    #global tracking
    all_chunks = []
    global_chunk_id = 0

    for doc in texts:
        doc_chunks = chunk_text(
            doc["content"],
            config["chunk_size"],
            config["chunk_overlap"]
        )

        for c in doc_chunks:
            chunk_data = {
                "chunk_id": global_chunk_id,
                "content": c["content"],
                "metadata": {
                    "source": doc.get("source"),
                    "page_number": doc.get("page_number", None),
                    "tags": []
                }
            }

            all_chunks.append(chunk_data)
            global_chunk_id += 1

    chunks_path = os.path.join(save_folder, "chunks.json")

    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Saved {len(all_chunks)} chunks")

    return chunks_path, all_chunks


#  EMBEDDINGS (chunks->vector)
def generate_embeddings(chunks, model_name):
    model = SentenceTransformer(model_name)

    vectors = []
    metadata = []

    for c in chunks:
        vec = model.encode(c["content"])  # (text->vector)

        vectors.append(vec)

        #mapping store
        metadata.append({
            "chunk_id": c["chunk_id"],
            "content": c["content"],
            "metadata": c["metadata"]
        })

    return np.array(vectors).astype("float32"), metadata


#faiss
def build_faiss_index(vectors):
    index = faiss.IndexFlatL2(vectors.shape[1]) #L2 distance(similarity) :euclidean distance(sees magnitude too:absolute distance)
    index.add(vectors)  #vectors add
    return index

#saves vector DB and metadata
def save_vectorstore(index, metadata):
    save_path = "data/cleaned/vector_store"
    os.makedirs(save_path, exist_ok=True)

    faiss.write_index(index, os.path.join(save_path, "index.faiss"))

    with open(os.path.join(save_path, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)

    print("Vectorstore saved")


if __name__ == "__main__":

    base_dir = os.path.dirname(__file__)

    data_folder = os.path.abspath(
        os.path.join(base_dir, "../data/raw/pdf") #input pdf
    )

    chunks_folder = os.path.abspath(
        os.path.join(base_dir, "../data/chunks")  #output chunks
    )

    # STEP 1: chunking
    chunks_path, chunks = create_chunks(data_folder, chunks_folder)

    # STEP 2: embeddings
    print("Generating embeddings...")
    vectors, metadata = generate_embeddings(chunks, config["embedding_model"])

    # STEP 3: FAISS
    print("Building FAISS index...")
    index = build_faiss_index(vectors)

    # STEP 4: save
    save_vectorstore(index, metadata)

    print("Ingestion completed successfully")