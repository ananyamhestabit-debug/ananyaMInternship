#Import embedding model
from sentence_transformers import SentenceTransformer

#Load lightweight model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    """
    Input: list of texts
    Output: embeddings (vectors)
    Converts text → vector embeddings
    Used in both indexing and search
    """
    return model.encode(texts, convert_to_numpy=True)