# AGENT FUNDAMENTALS — DAY 1

## What is an AI Agent?
An AI agent is a program that:
1. **Perceives** input (user message, data, tool output)
2. **Reasons** about what to do (using an LLM)
3. **Acts** (replies, calls tools, delegates)
4. **Loops** until the task is done

## Agent vs Chatbot vs Pipeline
| Feature | Chatbot | Pipeline | Agent |
|---------|---------|----------|-------|
| Memory | None | None | Yes |
| Tools | No | Sometimes | Yes |
| Planning | No | Fixed | Dynamic |
| Autonomy | No | No | Yes |

## ReAct Pattern
Reason → Act → Observe → Reason again

## Message Protocol
Each agent sends/receives structured messages:
- sender: who sent it
- receiver: who gets it  
- content: the message body
- role: "user" or "assistant"

## Day 1 Flow
User -> ResearchAgent -> SummarizerAgent -> AnswerAgent -> User

## How to Run

# USE LIKE THIS:
🔹 Development (fast)
-> export MODEL_NAME=tinyllama
-> python main.py

--------

🔹 Final demo / submission
-> export MODEL_NAME=mistral
-> python main.py

# model download:
-> ollama pull mistral

# start ollama:
-> ollama serve

# run model once:
-> ollama run mistral

# run project:
```bash
export MODEL_NAME=mistral

 python3 main.py
```

## Agents Implemented
1. Research Agent
2. Summarizer Agent
3. Answer Agent

## Memory
- max_consecutive_auto_reply = 10

## Advanced Features
- Request ID tracking
- Structured logging (agent_trace.log)
- Strict role enforcement
- Query-scoped reasoning
- Error handling

## Execution Flow
User Query
→ Research Agent (raw data)
→ Summarizer Agent (filtered insights)
→ Answer Agent (final output)

## Notes
Each agent performs a single responsibility.
No overlap in roles ensures clean reasoning pipeline.