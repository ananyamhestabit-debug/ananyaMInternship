import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from nexus_ai.pipeline import run_pipeline
from nexus_ai.memory import get_past_runs, get_all_facts
from nexus_ai.config import DATA_DIR

app = FastAPI(title="NEXUS AI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR.mkdir(exist_ok=True)


class RunRequest(BaseModel):
    task: str
    csv_filename: Optional[str] = None


@app.get("/")
def root():
    return {"status": "NEXUS AI running"}


@app.get("/memory")
def get_memory():
    runs = get_past_runs(10)
    facts = get_all_facts(10)
    return {"past_runs": runs, "facts": facts}


@app.get("/csv-files")
def list_csv_files():
    """List all CSV files available in the data/ folder."""
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    return {"files": files}


@app.post("/run")
def run_task(req: RunRequest):
    """Run the NEXUS AI pipeline on a task."""
    logs = []

    def capture(msg):
        logs.append(msg)

    csv_path = None
    if req.csv_filename:
        p = DATA_DIR / req.csv_filename
        if p.exists():
            csv_path = str(p)
        else:
            raise HTTPException(400, f"CSV not found in data/ folder: {req.csv_filename}")

    result = run_pipeline(req.task, csv_path=csv_path, stream_callback=capture)
    result["logs"] = logs
    return result
