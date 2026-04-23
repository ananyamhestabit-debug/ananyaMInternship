# NEXUS AI — Day 5

Autonomous 9-agent AI system with FastAPI backend + Streamlit UI.

## Setup (one time)

```bash
cd ~/re_assignment/Week9/day5

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

Open **two terminals**. Both need the venv activated and API key set.

### Terminal 1 — FastAPI backend

```bash
cd ~/re_assignment/Week9/day5
source venv/bin/activate
export GROQ_API_KEY="your_key_here"
python -m uvicorn api:app --reload --port 8000
```

### Terminal 2 — Streamlit UI

```bash
cd ~/re_assignment/Week9/day5
source venv/bin/activate
export GROQ_API_KEY="your_key_here"
streamlit run ui.py
```

Then open: http://localhost:8501

## Agents

1. Orchestrator — decides pipeline
2. Planner — creates step-by-step plan
3. Researcher — gathers context, reads CSV
4. Coder — writes Python code
5. Analyst — data analysis and insights
6. Critic — reviews output quality
7. Optimizer — improves based on critic
8. Validator — final quality check + self-reflection
9. Reporter — produces final report

## Features

- CSV upload via UI — any CSV file, agents analyze real data
- Memory — SQLite long-term + FAISS vector memory
- Self-reflection — if score < 7, optimizer runs again
- Output files — code tasks save .py + .md, others CLI only
- Logs — every run saved to logs/
