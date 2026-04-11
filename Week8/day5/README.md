# Local LLM API (GGUF + FastAPI + Streamlit)

## Overview

This project demonstrates a full LLM pipeline:

- Fine-tuning (LoRA / QLoRA)
- Quantisation (INT8, INT4, GGUF)
- Benchmarking (Speed, VRAM, Latency)
- Deployment using FastAPI + Streamlit

The final system runs a **GGUF quantized model locally on CPU**.

---

## Features

✔ FastAPI backend  
✔ Streamlit UI  
✔ GGUF model (CPU inference)  
✔ Chat + Generate endpoints  
✔ Adjustable parameters (temperature, top_p, etc.)  
✔ Lightweight & portable  

---

## Project Structure
Week8/
│
├── model/
│ └── model-q4.gguf
│
├── day5/
│ ├── backend/
│ │ ├── app.py
│ │ ├── model_loader.py
│ │ ├── config.py
│ │
│ ├── frontend/
│ │ └── ui.py
│
│ ├── requirements.txt
│ └── README.md


---

## Installation

```bash
cd day5
pip install -r requirements.txt

Run Backend
cd backend
uvicorn app:app --reload

Run Frontend
cd frontend
streamlit run ui.py

Access UI
http://localhost:8501

API Endpoints
POST /generate
{
  "prompt": "What is GST?"
}
POST /chat
{
  "message": "Explain GST"
}

Tech Stack:
-Transformers
-PEFT (LoRA / QLoRA)
-BitsAndBytes
-llama.cpp (GGUF)
-FastAPI
-Streamlit

Key Learnings:
-Efficient LLM deployment on CPU
-Quantisation trade-offs
-API-based LLM serving
-UI integration with backend

Conclusion:
This project demonstrates how to deploy a lightweight, production-ready LLM locally without requiring GPUs.


