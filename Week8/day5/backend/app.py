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

SYSTEM_PROMPT = (
    "You are a professional finance assistant.\n"
    "Answer clearly, concisely, and only about finance.\n"
    "If question is outside finance, say: 'I specialize in finance topics.'"
)


# -------- Helper: Clean Output --------

def clean_output(text: str) -> str:
    # Remove role tags
    for tag in ["Assistant:", "User:", "System:"]:
        if tag in text:
            text = text.split(tag)[-1]

    # Remove repeated lines
    lines = text.strip().split("\n")
    cleaned = []
    for line in lines:
        if line.strip() and line not in cleaned:
            cleaned.append(line)

    return " ".join(cleaned).strip()


# -------- Helper: Build Prompt --------

def build_chat_prompt(history):
    return SYSTEM_PROMPT + "\n\n" + "\n".join(history) + "\nAssistant:"


# -------- Health --------

@app.get("/")
def home():
    return {"message": "LLM API running"}


# -------- Generate --------

@app.post("/generate")
def generate(req: GenerateRequest):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"REQUEST {request_id}: {req.prompt}")

    # prompt formatting
    prompt = f"{SYSTEM_PROMPT}\n\nUser: {req.prompt}\nAssistant:"

    output = llm(
        prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
        top_k=req.top_k,
        stop=["User:"]
    )

    raw_text = output["choices"][0]["text"]
    response_text = clean_output(raw_text)

    latency = round(time.time() - start_time, 3)

    logger.info(f"RESPONSE {request_id}: {response_text}")
    logger.info(f"LATENCY {request_id}: {latency}s")

    return {
        "request_id": request_id,
        "latency": latency,
        "response": response_text
    }


# -------- Chat --------

@app.post("/chat")
def chat(req: ChatRequest):
    global chat_history

    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Add user message
    chat_history.append(f"User: {req.message}")

    # Limit memory (last 6 exchanges)
    chat_history = chat_history[-6:]

    prompt = build_chat_prompt(chat_history)

    logger.info(f"CHAT REQUEST {request_id}: {req.message}")

    output = llm(
        prompt,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        top_k=TOP_K,
        stop=["User:"]
    )

    raw_reply = output["choices"][0]["text"]
    reply = clean_output(raw_reply)

    # Save assistant reply
    chat_history.append(f"Assistant: {reply}")

    latency = round(time.time() - start_time, 3)

    logger.info(f"CHAT RESPONSE {request_id}: {reply}")
    logger.info(f"CHAT LATENCY {request_id}: {latency}s")

    return {
        "request_id": request_id,
        "response": reply,
        "latency": latency
    }