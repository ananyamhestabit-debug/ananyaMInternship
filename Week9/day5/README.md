# NEXUS AI — Day 5

Autonomous 9-agent AI system. No GPU required.

## Setup & Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_key_here"
python3 nexus_ai/main.py
```

## Example Tasks

| # | Task | Output saved as |
|---|---|---|
| 1 | Plan a startup in AI for healthcare | `.md` |
| 2 | Write a Python FastAPI REST API with CRUD endpoints | `.py` + `.md` |
| 3 | Analyze a CSV sales dataset and create a business strategy | `.md` |
| 4 | Build a machine learning pipeline for text classification | `.py` + `.md` |
| 5 | Design a RAG pipeline for 50000 documents | `.py` + `.md` |
| 6 | Generate backend architecture for a scalable e-commerce app | `.md` |

## Output Files

- **Code queries** → `output_files/output_TIMESTAMP.py` (code) + `output_files/output_TIMESTAMP_report.md`
- **Text queries** → `output_files/output_TIMESTAMP.md`

CLI always shows full output in terminal too.

## Agents

| Agent | Role |
|---|---|
| Orchestrator | Breaks task into high-level steps |
| Planner | Expands steps into detailed sub-tasks |
| Researcher | Gathers relevant information |
| Coder | Writes Python code / technical implementation |
| Analyst | Synthesizes findings into structured insights |
| Critic | Reviews output and finds weaknesses |
| Optimizer | Improves output using critic feedback |
| Validator | Final quality check (score + pass/fail) |
| Reporter | Compiles everything into final report |

## Folder Structure

```
day5/
├── nexus_ai/
│   ├── main.py           <- run this
│   ├── agents.py         <- all 9 agents
│   ├── output_saver.py   <- saves .py or .md based on query
│   ├── memory.py         <- SQLite long-term memory
│   ├── llm_client.py     <- shared Groq client
│   └── config.py         <- settings
├── output_files/         <- .py and .md outputs saved here
├── logs/                 <- JSON run logs
├── memory/               <- nexus_memory.db
├── ARCHITECTURE.md
└── requirements.txt
```
