import os
import yaml
from transformers import pipeline


class LLMClient:
    def __init__(self):
        with open("config/model.yaml", "r") as f:
            config = yaml.safe_load(f)

        self.provider = config["provider"]
        self.model_name = config["model_name"]
        self.api_key_env = config["api_key_env"]

        # -------- LOCAL --------
        if self.provider == "local":
            print("[LLM] Using LOCAL model")

            self.llm = pipeline(
                "text2text-generation",
                model=self.model_name,
                max_new_tokens=100
            )

        # -------- OPENAI --------
        elif self.provider == "openai":
            print("[LLM] Using OPENAI")

            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv(self.api_key_env))

        # -------- GEMINI --------
        elif self.provider == "gemini":
            print("[LLM] Using GEMINI")

            import google.generativeai as genai
            genai.configure(api_key=os.getenv(self.api_key_env))
            self.model = genai.GenerativeModel(self.model_name)

        else:
            raise ValueError("Unsupported provider")

    def generate(self, prompt):

        # LOCAL
        if self.provider == "local":
            return self.llm(prompt)[0]["generated_text"]

        # OPENAI
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        # GEMINI
        elif self.provider == "gemini":
            response = self.model.generate_content(prompt)
            return response.text