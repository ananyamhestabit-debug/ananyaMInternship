import faiss
import numpy as np
import pickle

class FAISSStore:
    def __init__(self, dim):
        # FAISS index create (L2 distance)
        self.index = faiss.IndexFlatL2(dim)

        # original data store (text + metadata)
        self.data = []

    def add(self, vectors, chunks):
        """
        Add embeddings + chunks to DB
        """
        self.index.add(np.array(vectors))
        self.data.extend(chunks)

    def save(self):
        """
        Save FAISS index + data
        """
        faiss.write_index(self.index, "src/vectorstore/index.faiss")

        with open("src/vectorstore/data.pkl", "wb") as f:
            pickle.dump(self.data, f)

    def search(self, query_vector, k=5):
        """
        Search top-k similar results
        """
        distances, indices = self.index.search(query_vector, k)

        results = []
        for i in indices[0]:
            results.append(self.data[i])

        return results