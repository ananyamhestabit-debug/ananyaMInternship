import os
import json
import numpy as np

from src.embeddings.clip_embedder import get_image_embedding
from src.embeddings.blip_caption import generate_caption

def generate_image_embeddings(folder="src/data/raw"):
    embeddings = []
    metadata = []

    for file in os.listdir(folder):
        if file.endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(folder, file)

            emb = get_image_embedding(path)
            caption = generate_caption(path)

            embeddings.append(emb[0])

            metadata.append({
                "file": file,
                "caption": caption
            })

    # 🔥 IMPORTANT FIX
    save_path = "src/embeddings"
    os.makedirs(save_path, exist_ok=True)

    np.save(f"{save_path}/image_embeddings.npy", embeddings)

    os.makedirs("src/data/chunks", exist_ok=True)
    with open("src/data/chunks/image_meta.json", "w") as f:
        json.dump(metadata, f, indent=4)

    return embeddings