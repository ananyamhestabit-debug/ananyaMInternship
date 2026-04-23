# 🚀 NEXUS AI

### Autonomous Multi-Agent AI System — Week 9 Capstone

---

## 🧠 What is NEXUS AI?

**NEXUS AI** is a fully autonomous multi-agent AI system designed to solve complex tasks using coordinated intelligence.

It orchestrates **8 specialized agents** that work together to:

* Plan
* Research
* Code
* Analyze
* Critique
* Optimize
* Validate
* Report

Unlike traditional chatbots, NEXUS AI behaves like a **complete AI system**, capable of reasoning, execution, and self-improvement.

---

## ⚡ Capabilities

* 🧩 Multi-agent orchestration
* 🧠 Multi-step planning
* ⚡ Parallel task execution
* 🐍 Python code generation & execution
* 🔄 Self-reflection & optimization loop
* 💾 Memory system:

  * Session Memory
  * Vector Memory (FAISS)
  * Long-Term Memory (SQLite)
* 📊 CSV data analysis
* 🧾 Logs & tracing
* 🛠 Tool integration (code, file, DB)
* 🔁 Failure recovery

---

## 🧰 Tech Stack

| Component       | Technology                    |
| --------------- | ----------------------------- |
| Agent Framework | AutoGen                       |
| LLM             | Groq (llama-3.1-8b-instant)   |
| Vector Memory   | FAISS + sentence-transformers |
| Database        | SQLite                        |
| Code Execution  | Python (exec)                 |
| File Handling   | CSV / TXT                     |
| Environment     | Python 3.12 + venv            |

---

## 📦 Prerequisites

```bash
pip install autogen-agentchat autogen-ext faiss-cpu sentence-transformers python-dotenv openai
```

---

## ⚙️ Setup

```bash
cd Week9
```

Create `.env`:

```env
OPENAI_API_KEY=your_groq_api_key_here
```

---

## ▶️ Run Project

```bash
cd day5/nexus_ai
python main.py
```

---

## 💡 Example Queries

```
what is array
write binary search code
plan AI startup
analyze CSV data
exit
```

---

## 🏗 Project Structure (ACTUAL)

```
Week9/
│
├── day1/
│   ├── agents/
│   ├── orchestrator.py
│   ├── main.py
│   └── AGENT-FUNDAMENTALS.md
│
├── day2/
│   ├── agents/
│   ├── orchestrator/
│   ├── main.py
│   └── FLOW-DIAGRAM.md
│
├── day3/
│   ├── agents/
│   ├── tools/
│   ├── data/
│   ├── orchestrator/
│   ├── main.py
│   └── TOOL-CHAIN.md
│
├── day4/
│   ├── memory/
│   ├── main.py
│   └── MEMORY-SYSTEM.md
│
├── day5/
│   ├── nexus_ai/
│   │   ├── agents/
│   │   ├── orchestrator/
│   │   │   └── nexus.py
│   │   ├── main.py
│   │   ├── config.py
│   │   └── outputs/
│   │
│   ├── ARCHITECTURE.md
│   ├── FINAL-REPORT.md
│   └── README.md
│
├── .env
├── requirements.txt
└── venv/
```

---

## 🔄 How It Works

1. User enters query
2. Router selects agents
3. Agents execute step-by-step
4. Tools are used (code / file / DB)
5. Memory is injected
6. Final output is generated
7. Code (if any) is executed + saved

---

## 📜 Logs

Stored in:

```
day5/nexus_ai/outputs/
```

---

## 🎯 Key Highlights

* Fully autonomous agent system
* Works for both code + general queries
* Saves executed code automatically
* Uses memory + tools
* Real-world AI system architecture

---

## 🏁 Final Outcome

This project demonstrates the transition:

➡️ Prompt Engineering
➡️ AI System Engineering

**NEXUS AI is not a chatbot — it is a complete autonomous AI system.**

---
