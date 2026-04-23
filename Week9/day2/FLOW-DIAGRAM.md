# DAY 2 — FLOW DIAGRAM

## Multi-Agent Orchestration Pipeline

```
USER QUERY
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│              ORCHESTRATOR / PLANNER                     │
│                                                         │
│  • Receives user query                                  │
│  • Breaks it into 2-4 atomic sub-tasks                  │
│  • Assigns each task to a role: researcher/analyst/coder│
│  • Outputs a structured JSON execution plan             │
│                                                         │
│  File: orchestrator/planner.py                          │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
   ┌────────────┐ ┌──────────┐ ┌────────────┐
   │  WORKER    │ │  WORKER  │ │  WORKER    │
   │  (T1)      │ │  (T2)    │ │  (T3)      │
   │ researcher │ │ analyst  │ │  coder     │
   └─────┬──────┘ └────┬─────┘ └─────┬──────┘
         │             │              │
         └─────────────┴──────────────┘
                       │
              (ALL RUN IN PARALLEL via ThreadPoolExecutor)
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               REFLECTION AGENT                          │
│                                                         │
│  • Reviews all worker outputs                           │
│  • Identifies gaps and contradictions                   │
│  • Synthesizes into one coherent improved response      │
│                                                         │
│  File: agents/reflection_agent.py                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               VALIDATOR AGENT                           │
│                                                         │
│  Checks for:                                            │
│  ✔ Relevance to original query                          │
│  ✔ Completeness                                         │
│  ✔ Accuracy (no obvious errors)                         │
│  ✔ Clarity                                              │
│                                                         │
│  Outputs: JSON with status, score/10, final_answer      │
│  File: agents/validator.py                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
               FINAL ANSWER
             (saved to logs/)
```

## Agent Responsibilities

| Agent | File | Role | Output |
|-------|------|------|--------|
| Orchestrator | `orchestrator/planner.py` | Creates task plan | JSON plan |
| Worker | `agents/worker_agent.py` | Executes tasks (parallel) | Task results |
| Reflection | `agents/reflection_agent.py` | Synthesizes outputs | Improved response |
| Validator | `agents/validator.py` | Quality gate | Validated final answer |

## Key Design Decisions

- **Parallel Workers**: `ThreadPoolExecutor` runs all worker tasks simultaneously — not sequentially
- **Role Isolation**: Each worker role has a different system prompt; they cannot "drift" into each other's jobs
- **Strict JSON**: Planner and Validator use regex-guarded JSON parsing to prevent output format failures
- **Execution Tree**: Printed at runtime showing full pipeline visually
- **Logging**: Every run saved to `logs/run_TIMESTAMP.json`

## Tech Stack
- **Model**: `llama3-8b-8192` via Groq API (free tier, CPU-friendly, no GPU needed)
- **Parallelism**: Python `concurrent.futures.ThreadPoolExecutor`
- **No GPU required**: Groq runs inference in the cloud on their hardware
