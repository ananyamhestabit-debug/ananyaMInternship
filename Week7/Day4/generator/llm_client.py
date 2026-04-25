import os
import yaml
from dotenv import load_dotenv

load_dotenv()

#calls llm (api call to llm after we give question so that llm answers)
#config se provider read karna, API key load karna ,Groq/OpenAI jaisa backend choose karna, prompt bhejna, answer wapas lana
class LLMClient:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "../config/config.yaml")

        with open(config_path) as f:
            config = yaml.safe_load(f)

        self.provider = config["provider"]
        self.model_name = config["model_name"]
        api_key = os.getenv(config["api_key_env"])

        if not api_key:
            raise ValueError("API KEY NOT FOUND")

        if self.provider == "groq":
            from groq import Groq
            self.client = Groq(api_key=api_key)
        else:
            raise ValueError("Unsupported provider")

    def generate(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0 #deterministic(same ans har baar) and reproducible outputs (same input->same output)/ randomness control in llm output (randomness nahi as 0 )
        )

        return response.choices[0].message.content.strip()