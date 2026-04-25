import faiss
import numpy as np
import json
import os

#embeddings -> faiss index builder (embeddings load->vectors extract->FAISS index bnata->index save):[embedding leta hai aur faiss index bnata hai]
def build_faiss_index(embeddings_path, index_path):
    embeddings_data = np.load(embeddings_path, allow_pickle=True)  
    vectors = np.array([e["vector"] for e in embeddings_data]).astype("float32")  #sirf vector nikal rhe 
    index = faiss.IndexFlatL2(vectors.shape[1])  
    index.add(vectors)  #vectors add 
    faiss.write_index(index, index_path)  #index save
    print(f"FAISS index saved to {index_path}")
    return index

if __name__ == "__main__":
    build_faiss_index("../data/embeddings/chunks.npy", "../vectorstore/index.faiss")  # embeddings.npy → indexer → index.faiss