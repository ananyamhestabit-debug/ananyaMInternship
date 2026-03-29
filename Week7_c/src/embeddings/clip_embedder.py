from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        image_features = model.get_image_features(pixel_values=inputs["pixel_values"])

    if hasattr(image_features, "cpu"):
        emb = image_features
    elif hasattr(image_features, "pooler_output"):
        emb = image_features.pooler_output
    else:
        raise ValueError("Unexpected output")

    return emb.cpu().numpy()

def get_text_embedding(text):
    inputs = processor(text=[text], return_tensors="pt", padding=True)

    with torch.no_grad():
        text_features = model.get_text_features(**inputs)

    if hasattr(text_features, "cpu"):
        emb = text_features
    elif hasattr(text_features, "pooler_output"):
        emb = text_features.pooler_output
    else:
        raise ValueError("Unexpected output")

    return emb.cpu().numpy()