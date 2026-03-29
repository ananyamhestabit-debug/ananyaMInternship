import numpy as np

def search_images(query_vec, image_vecs, top_k=3):
    scores = np.dot(image_vecs, query_vec.T)

    ranked = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )

    return [idx for idx, _ in ranked[:top_k]]