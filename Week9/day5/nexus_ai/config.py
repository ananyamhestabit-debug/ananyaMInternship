import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
print("DEBUG KEY:", API_KEY)
MODEL_INFO = {
    "provider": "groq",
    "family": "llama",
    "context_length": 8192,
    "vision": False,
    "function_calling": False,
    "json_output": False,
    "structured_output": False,
}