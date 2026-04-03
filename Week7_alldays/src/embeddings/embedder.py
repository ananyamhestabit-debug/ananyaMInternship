from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en")

    def embed_batch(self, texts, batch_size=32):
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            emb = self.model.encode(
                batch,
                normalize_embeddings=True,
                show_progress_bar=False
            )

            embeddings.extend(emb)

        return embeddings