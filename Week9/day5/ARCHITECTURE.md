# NEXUS AI — Architecture

## Agent Pipeline

```
USER INPUT
  -> ORCHESTRATOR   breaks task into high-level steps
  -> PLANNER        expands steps into detailed sub-tasks with owners
  -> RESEARCHER     gathers information and context
  -> CODER          writes Python code or technical implementation
  -> ANALYST        synthesizes findings into structured insights
  -> CRITIC         reviews output, finds weaknesses and gaps
  -> OPTIMIZER      improves output using critic feedback
  -> VALIDATOR      final quality check — pass/fail + score
  -> REPORTER       compiles everything into a final report
```

## Output File Saving

System decides file type based on the query:

| Query type | Detection | Files saved |
|---|---|---|
| Code (build/write/api/pipeline/implement) | keyword match or ```python block in output | `.py` (code) + `.md` (report) |
| Plan / strategy / analysis / design | everything else | `.md` only |

CLI always shows full output regardless of file type.

## Memory

- Long-term: SQLite at `memory/nexus_memory.db`
- Stores task, score, saved filename, timestamp per run
- Shown at startup for context

## Logs

- Every run: `logs/nexus_run_TIMESTAMP.json`

## Tech

- LLM: Groq API (`llama-3.1-8b-instant`) — no GPU needed
- Language: Python 3.10+
- No heavy dependencies
