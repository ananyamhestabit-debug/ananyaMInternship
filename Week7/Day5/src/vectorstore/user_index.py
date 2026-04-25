import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

#user chunks->faiss
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def build_user_index(chunks):
    texts = [c["content"] for c in chunks]
    vecs = model.encode(texts)  #user PDF embedding
    vecs = np.array(vecs).astype("float32")

    index = faiss.IndexFlatL2(vecs.shape[1])  #temp index
    index.add(vecs)

    return index, chunks  # metadata = chunks itself