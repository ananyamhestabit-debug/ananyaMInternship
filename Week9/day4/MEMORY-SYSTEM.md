# DAY 4 - MEMORY SYSTEM

## Three Memory Types

| Type | File | Storage | Persists |
|------|------|---------|---------|
| Short-term | `memory/session_memory.py` | RAM (list) | No - clears on exit |
| Long-term | `memory/long_term_memory.py` | SQLite | Yes - survives restarts |
| Vector | `memory/vector_store.py` | FAISS + JSON | Yes - survives restarts |

## Flow

```
New query
  -> search vector store for similar past exchanges
  -> fetch recent facts from long-term SQLite
  -> inject both into system prompt
  -> generate response with full context
  -> store exchange in vector memory
  -> extract key fact -> save to long-term SQLite
  -> add turn to session memory
```

## Files

```
day4/
  main.py
  requirements.txt
  memory/
    session_memory.py      - short-term, RAM only
    long_term_memory.py    - SQLite facts store
    vector_store.py        - FAISS similarity search
    long_term.db           - auto-created on first run
    vector_store.json      - auto-created on first run
  agents/
    memory_agent.py        - orchestrates all three memory types
  logs/
```

## Commands in chat

- `status`  - show memory counts
- `memory`  - show all long-term facts
- `clear`   - wipe all memory
- `quit`    - exit


## how to run:
(venv) ananyamishra@hestabit-Latitude-3450:~/re_assignment/Week9/day4$ export GROQ_API_KEY=
(venv) ananyamishra@hestabit-Latitude-3450:~/re_assignment/Week9/day4$ python main.py
Day 4 - Memory Agent
Commands: 'status', 'memory', 'clear', 'quit'
Anything else is treated as a query.


[VECTOR] Stored: User is interested in Python and AI development...
You: My name is Ananya and I am learning AI

[USER] My name is Ananya and I am learning AI  <humne likha>
[MEMORY] Found 1 similar memories
[AGENT] Nice to virtually meet you, Ananya. I remember you're interested in AI and Python development, especially multi-agent systems. How can I assist you today? Do you have a specific question or topic you'd like to discuss?
[MEMORY] Stored fact: Ananya is interested in AI and Python development, especially multi-agent systems.
[VECTOR] Stored: User asked: My name is Ananya and I am learning AI | Assista...
You: What do you know about me?

[USER] What do you know about me?  <humne likha>
[MEMORY] Found 2 similar memories
[AGENT] I remember that you're Ananya, and you're learning about AI. Specifically, you're interested in AI and Python development, with a focus on multi-agent systems. That's about it, but I'm happy to help you with any questions or topics related to AI and multi-agent systems.
[MEMORY] Stored fact: Ananya is learning about AI with a focus on Python development and multi-agent systems.
[VECTOR] Stored: User asked: What do you know about me? | Assistant answered:...
You: Status   <ye humne likha>

--- Memory Status ---
Session turns     : 4
Long-term facts   : 3
Vector store size : 3
---------------------

You: memory   <- ye likha humne >

--- Long-term Memories ---
[3] fact | Ananya is learning about AI with a focus on Python development and multi-agent systems.
[2] fact | Ananya is interested in AI and Python development, especially multi-agent systems.
[1] fact | User is learning about AI and multi-agent systems
--------------------------

You: quit