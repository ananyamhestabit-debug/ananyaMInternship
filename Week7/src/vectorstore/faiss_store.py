import faiss
import numpy as np
import pickle


class FAISSStore:
    def __init__(self, dim):
        # FAISS index (L2 distance)
        self.index = faiss.IndexFlatL2(dim)

        # store original data (text / image + metadata)
        self.data = []

    def add(self, vectors, chunks):
        """
        Add embeddings + chunks to FAISS
        """

        # ensure correct type + shape
        vectors = np.array(vectors).astype("float32")

        if len(vectors.shape) == 1:
            vectors = vectors.reshape(1, -1)

        # add to index
        self.index.add(vectors)

        # store metadata
        self.data.extend(chunks)

    def save(self):
        """
        Save FAISS index + metadata
        """
        faiss.write_index(self.index, "src/vectorstore/index.faiss")

        with open("src/vectorstore/data.pkl", "wb") as f:
            pickle.dump(self.data, f)

    def search(self, query_vector, k=5):
        """
        Search top-k similar results
        """

        # ensure correct shape + type
        query_vector = np.array(query_vector).astype("float32")

        if len(query_vector.shape) == 1:
            query_vector = query_vector.reshape(1, -1)

        # FAISS search
        distances, indices = self.index.search(query_vector, k)

        results = []

        for i in indices[0]:
            if i < len(self.data):   # safety check
                results.append(self.data[i])

        return results