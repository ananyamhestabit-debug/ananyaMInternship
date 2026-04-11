import os

MODEL_PATH = os.getenv("MODEL_PATH", "../model/model-q4.gguf")

MAX_TOKENS = 200
TEMPERATURE = 0.7
TOP_P = 0.9
TOP_K = 40