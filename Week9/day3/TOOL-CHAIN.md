# DAY 3 — TOOL CHAIN DIAGRAM

## Architecture

```
USER QUERY
    │
    ▼
┌──────────────────────────────────────────────────────┐
│  ORCHESTRATOR                                        │
│  Reads query → decides which tools → ordered plan    │
│  File: orchestrator/tool_orchestrator.py             │
└─────────────────────┬────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
   ┌────────────┐ ┌──────────┐ ┌────────────┐
   │ FILE AGENT │ │ DB AGENT │ │ CODE AGENT │
   │            │ │          │ │            │
   │ Reads .csv │ │ SQLite   │ │ Generates  │
   │ and .txt   │ │ SQL query│ │ + executes │
   │ files      │ │ runner   │ │ Python code│
   └─────┬──────┘ └────┬─────┘ └─────┬──────┘
         │             │              │
         └─────────────┴──────────────┘
                       │
                       ▼ (all outputs collected)
        ┌──────────────────────────────────┐
        │  ANALYSIS AGENT                  │
        │  Synthesizes tool outputs into   │
        │  business insights & report      │
        └──────────────────────────────────┘
                       │
                       ▼
              ✅ FINAL REPORT
```

## Tool Agents

| Agent | File | Tool Used | Input | Output |
|-------|------|-----------|-------|--------|
| File Agent | `tools/file_agent.py` | CSV/TXT reader | filepath | File analysis |
| DB Agent | `tools/db_agent.py` | SQLite + SQL | instruction | Query results |
| Code Agent | `tools/code_executor.py` | subprocess Python | instruction | Execution output |
| Analysis Agent | `agents/analysis_agent.py` | LLM synthesis | all outputs | Final report |

## Example Flow

**Query:** "Analyze sales.csv and generate top 5 business insights"

```
Step 1 → FILE AGENT   reads data/sales.csv → structure + stats
Step 2 → DB AGENT     SQL: SELECT product, SUM(revenue) ... GROUP BY → top products
Step 3 → CODE AGENT   Python: month-wise aggregation → trend numbers
         │
         ▼
ANALYSIS AGENT → combines all 3 outputs → 📊 Final Report
```

## Tech Stack
- SQLite (built into Python — zero install)
- subprocess (safe Python execution)
- Groq API — llama-3.1-8b-instant (free, no GPU)
