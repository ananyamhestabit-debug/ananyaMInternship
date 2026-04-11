from llama_cpp import Llama
from config import MODEL_PATH

print("Loading GGUF model...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    verbose=False
)

print("Model loaded successfully!")