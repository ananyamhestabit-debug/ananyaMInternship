import faiss
import pickle
import numpy as np
from embeddings.clip_embedder import CLIPEmbedder

VECTOR_PATH = "data/cleaned/vector_store"


class ImageSearchEngine:
    def __init__(self):
        self.embedder = CLIPEmbedder()

        # load IMAGE FAISS index
        self.index = faiss.read_index(f"{VECTOR_PATH}/image_index.faiss")

        # load IMAGE metadata
        with open(f"{VECTOR_PATH}/image_metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)

    # TEXT → IMAGE
    def search_by_text(self, query, k=5):
        q_emb = self.embedder.embed_text(query)
        D, I = self.index.search(np.array([q_emb]), k)
        return D[0], I[0]

    # IMAGE → IMAGE
    def search_by_image(self, image_path, k=5):
        q_emb = self.embedder.embed_image(image_path)
        D, I = self.index.search(np.array([q_emb]), k)
        return D[0], I[0]

    # PRINT RESULTS
    def pretty_print(self, scores, indices):
        print("\nRetrieved Images:\n")

        for i, (score, idx) in enumerate(zip(scores, indices)):
            data = self.metadata[idx]

            print(f"Result {i+1}")
            print(f"Image Path : {data['image_path']}")
            print(f"Caption    : {data['caption']}")
            print(f"OCR Text   : {data['ocr_text'][:200]}")
            print("-" * 50)


# ---------------- CLI ----------------
def main():
    engine = ImageSearchEngine()

    while True:
        print("\nImage Search Menu")
        print("1 → Text to Image")
        print("2 → Image to Image")
        print("3 → Image to Text")   
        print("4 → Exit")

        choice = input("Select option: ")

        # TEXT → IMAGE
        if choice == "1":
            query = input("Enter text query: ")
            scores, indices = engine.search_by_text(query)
            engine.pretty_print(scores, indices)

        # IMAGE → IMAGE
        elif choice == "2":
            path = input("Enter image path: ")
            scores, indices = engine.search_by_image(path)
            engine.pretty_print(scores, indices)

        # IMAGE → TEXT (TOP RESULT ONLY)
        elif choice == "3":
            path = input("Enter image path: ")
            scores, indices = engine.search_by_image(path)

            top = indices[0]
            data = engine.metadata[top]

            print("\nBest Match Text:\n")
            print("Caption:", data["caption"])
            print("OCR Text:", data["ocr_text"])
        

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()