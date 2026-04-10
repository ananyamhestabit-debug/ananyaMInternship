from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        
        print("Loaded API Key")
        if not api_key:
            raise ValueError("API KEY NOT FOUND")

        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        text = response.choices[0].message.content.strip()
        return text.replace("```sql", "").replace("```", "").strip()