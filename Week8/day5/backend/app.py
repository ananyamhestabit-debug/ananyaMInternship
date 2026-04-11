from fastapi import FastAPI
from pydantic import BaseModel
from model_loader import llm
from config import MAX_TOKENS, TEMPERATURE, TOP_P, TOP_K
from utils.logger import logger
import uuid
import time

app = FastAPI(title="LLM API (GGUF)")

# -------- Schemas --------

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = MAX_TOKENS
    temperature: float = TEMPERATURE
    top_p: float = TOP_P
    top_k: int = TOP_K

class ChatRequest(BaseModel):
    message: str


# -------- Chat Memory --------
chat_history = []


# -------- Health --------
@app.get("/")
def home():
    return {"message": "LLM API running "}


# -------- Generate --------
@app.post("/generate")
def generate(req: GenerateRequest):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"REQUEST {request_id}: {req.prompt}")

    output = llm(
        req.prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
        top_k=req.top_k,
    )

    response_text = output["choices"][0]["text"]

    latency = round(time.time() - start_time, 3)

    logger.info(f"RESPONSE {request_id}: {response_text}")
    logger.info(f"LATENCY {request_id}: {latency}s")

    return {
        "request_id": request_id,
        "latency": latency,
        "response": response_text.strip()
    }


# -------- Chat --------
@app.post("/chat")
def chat(req: ChatRequest):
    global chat_history

    request_id = str(uuid.uuid4())
    start_time = time.time()

    chat_history.append(f"User: {req.message}")

    prompt = "\n".join(chat_history) + "\nAssistant:"

    logger.info(f"CHAT REQUEST {request_id}: {req.message}")

    output = llm(
        prompt,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
    )

    reply = output["choices"][0]["text"].strip()

    chat_history.append(f"Assistant: {reply}")

    latency = round(time.time() - start_time, 3)

    logger.info(f"CHAT RESPONSE {request_id}: {reply}")
    logger.info(f"CHAT LATENCY {request_id}: {latency}s")

    return {
        "response": reply,
        "latency": latency
    }