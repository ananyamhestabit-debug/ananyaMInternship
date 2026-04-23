# NEXUS AI — Architecture

## Flow

USER --> ORCHESTRATOR --> PLANNER --> RESEARCHER --> CODER --> ANALYST --> CRITIC --> OPTIMIZER --> VALIDATOR --> REPORTER --> DONE

## Agents

| Agent | Role |
|---|---|
| Orchestrator | Decides which agents to activate based on task |
| Planner | Breaks task into numbered steps |
| Researcher | Gathers context, reads CSV data |
| Coder | Writes Python code when needed |
| Analyst | Data analysis, insights from CSV or research |
| Critic | Scores output, finds issues |
| Optimizer | Improves output based on critic feedback |
| Validator | Final quality check, triggers self-reflection if score < 7 |
| Reporter | Produces final structured report |

## Memory

- Short-term: session turns (in-memory, max 20)
- Long-term: SQLite (memory/long_term.db) — facts and run history
- Vector: FAISS via sentence-transformers (memory/vectors.pkl) — semantic recall

## Tool Use

- CSV Tool: reads any CSV, extracts stats, column info, sample rows
- Output Saver: code tasks → .py + .md, other tasks → CLI only

## API

- POST /run — run pipeline
- POST /upload-csv — upload CSV file
- GET /memory — view stored memory

## Stack

- Groq API (llama-3.1-8b-instant) — no GPU needed
- FastAPI + Uvicorn — backend
- Streamlit — UI
- SQLite — long-term memory
- sentence-transformers + numpy — vector memory
