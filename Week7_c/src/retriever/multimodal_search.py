import numpy as np
import json

from src.embeddings.clip_embedder import get_text_embedding

# load image embeddings
image_vecs = np.load("src/embeddings/image_embeddings.npy")

# load metadata (caption)
with open("src/data/chunks/image_meta.json") as f:
    image_meta = json.load(f)


# TEXT → IMAGE SEARCH
def text_to_image_search(query, top_k=3):
    query_vec = get_text_embedding(query)

    scores = np.dot(image_vecs, query_vec.T)

    ranked = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )

    return [image_meta[i] for i, _ in ranked[:top_k]]


# IMAGE → IMAGE SEARCH
def image_to_image_search(query_vec, top_k=3):
    scores = np.dot(image_vecs, query_vec.T)

    ranked = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )

    return [image_meta[i] for i, _ in ranked[:top_k]]


# IMAGE → TEXT ANSWER
def image_to_text_answer(index):
    data = image_meta[index]

    caption = data.get("caption", "")

    return f"Image description: {caption}"