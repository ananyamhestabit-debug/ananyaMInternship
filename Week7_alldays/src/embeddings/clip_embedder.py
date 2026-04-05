from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np

class CLIPEmbedder:
    def __init__(self):
        print("CLIP LOADED")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def embed_image(self, image_path):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            features = self.model.get_image_features(**inputs)

        vec = features[0].cpu().numpy()
        vec = vec / np.linalg.norm(vec)

        return vec.astype("float32")

    def embed_text(self, text):
        inputs = self.processor(text=[text], return_tensors="pt")

        with torch.no_grad():
            features = self.model.get_text_features(**inputs)

        vec = features[0].cpu().numpy()
        vec = vec / np.linalg.norm(vec)

        return vec.astype("float32")