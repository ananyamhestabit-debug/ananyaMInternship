from transformers import pipeline
import yaml


class LLMClient:
    def __init__(self):
        with open("config/model.yaml", "r") as f:
            config = yaml.safe_load(f)

        model_name = config["model_name"]

        print(f"[LLM] Loading {model_name}...")

        self.pipe = pipeline(
            "text-generation",
            model=model_name,
            device_map="auto",   # auto CPU/GPU
            max_new_tokens=150,
            do_sample=True,
            temperature=0.3
        )

    def generate(self, prompt):
        output = self.pipe(prompt)[0]["generated_text"]

        # IMPORTANT: remove prompt part
        return output.replace(prompt, "").strip()