import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
#image->vector + text->vector (in same space so that comparison is possible)

#clip embedder:CLIP projects both image and text into a shared embedding space, enabling cross-modal retrieval

class CLIPEmbedder:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")  #preprocessing:resize image, normalize, tokenize text
    def embed_image(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            vision_outputs = self.model.vision_model(**inputs)  #image -> feature map
            pooled = vision_outputs.pooler_output  #images summary vector

            features = self.model.visual_projection(pooled)  #projection layer: to convert raw features to embedding space (image space->clip shared space)

        features = features / features.norm(p=2, dim=-1, keepdim=True)

        return features.detach().cpu().numpy()[0]

    def embed_text(self, text):
        inputs = self.processor(text=[text], return_tensors="pt").to(self.device)  #text->tokens->tensors

        with torch.no_grad():
            text_outputs = self.model.text_model(**inputs)  #text->features
            pooled = text_outputs.pooler_output   #summary vector

            features = self.model.text_projection(pooled)  #same space as image

        # normalizing : to make unit vector so that cosine similarity sahi kaam kre
        features = features / features.norm(p=2, dim=-1, keepdim=True)

        return features.detach().cpu().numpy()[0]  #detahc: graph htata, gpu->cpu, numpy:array, [0]:first item