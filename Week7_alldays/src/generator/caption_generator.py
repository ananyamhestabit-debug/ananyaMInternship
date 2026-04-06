from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch


class CaptionGenerator:
    def __init__(self):
        print("BLIP LOADED")

        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def generate(self, image_path, ocr_text=None):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(image, return_tensors="pt")

        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=40,
                num_beams=4,
                repetition_penalty=1.3
            )

        caption = self.processor.decode(out[0], skip_special_tokens=True)

        return caption, ""