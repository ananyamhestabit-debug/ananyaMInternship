# NEXUS AI — Final Report

## Week 9 Day 5 Capstone

### What was built

NEXUS AI is a fully autonomous multi-agent AI system with 9 specialized agents, persistent memory, tool use, self-reflection, and a web UI.

### Agents implemented

All 9 required agents: Orchestrator, Planner, Researcher, Coder, Analyst, Critic, Optimizer, Validator, Reporter.

### Capabilities

- Multi-agent orchestration with dynamic pipeline selection
- Tool use: CSV file reading, Python code generation, output file saving
- Memory: short-term session, long-term SQLite, vector FAISS memory
- Self-reflection: Validator triggers a second optimization pass if quality score < 7
- Self-improvement: Critic + Optimizer loop
- Multi-step planning via Planner agent
- Role switching: pipeline adapts based on task type
- Logs and tracing: every run saved to logs/ as JSON
- Failure recovery: all agents have fallback responses

### Stack

- Groq API (no GPU required)
- FastAPI backend
- Streamlit UI (black and white, simple)
- SQLite + FAISS memory

### How to run

See README.md
