# DAY 2 — COMPLETE SETUP GUIDE (Linux + VS Code)

## ⚠️ Why Groq instead of local model?
Your laptop has no GPU. TinyLlama on CPU gives wrong/broken JSON output for structured agent tasks.
**Solution: Groq API** — free, cloud inference, llama3-8b-8192, no GPU needed, blazing fast.

---

## STEP 1 — Get Free Groq API Key (2 minutes)

1. Go to: https://console.groq.com
2. Sign up (free, no credit card)
3. Click **"API Keys"** → **"Create API Key"**
4. Copy the key (starts with `gsk_...`)

---

## STEP 2 — Open Terminal in VS Code

```
Ctrl + `   (backtick — opens integrated terminal)
```

---

## STEP 3 — Navigate to your project

```bash
cd ~/Desktop          # or wherever you saved the project
cd day2
```

---

## STEP 4 — Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal prompt.

---

## STEP 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs only the `groq` package. That's it. No heavy installs.

---

## STEP 6 — Set Groq API Key

**Option A: For this terminal session only (recommended for testing)**
```bash
export GROQ_API_KEY="gsk_your_actual_key_here"
```

**Option B: Permanent (add to ~/.bashrc)**
```bash
echo 'export GROQ_API_KEY="gsk_your_actual_key_here"' >> ~/.bashrc
source ~/.bashrc
```

---

## STEP 7 — Run the Multi-Agent System

```bash
python3 main.py
```

You'll see a menu with example queries. Either:
- Press Enter → uses default query
- Type `1`, `2`, or `3` → picks an example
- Type your own query → runs it through the pipeline

---

## STEP 8 — Expected Output

You should see something like:

```
══════════════ MULTI-AGENT SYSTEM — DAY 2 ══════════════
Query: Explain the differences between SQL and NoSQL databases
Time : 14:32:01

══════════════ STEP 1: ORCHESTRATOR ══════════════
[ORCHESTRATOR] Received query: ...
[ORCHESTRATOR] Plan created with 3 tasks
  → T1 | Assigned to: researcher | Research SQL vs NoSQL...
  → T2 | Assigned to: analyst | Analyze use cases...
  → T3 | Assigned to: coder | Show code examples...

══════════════ STEP 2: PARALLEL WORKERS ══════════════
[WORKERS] Starting 3 workers in PARALLEL...
  [WORKER-T1] RESEARCHER starting task...
  [WORKER-T2] ANALYST starting task...
  [WORKER-T3] CODER starting task...
  [WORKER-T1] RESEARCHER completed ✓
  [WORKER-T2] ANALYST completed ✓
  [WORKER-T3] CODER completed ✓

...

══════════════ ✅ FINAL ANSWER ══════════════
[Full validated answer here]

══════════════ EXECUTION TREE ══════════════
[Visual tree diagram here]

⏱  Total time: 8.34s
[LOG] Saved to logs/run_20240120_143209.json
```

---

## Folder Structure

```
day2/
├── main.py                    ← RUN THIS
├── requirements.txt
├── FLOW-DIAGRAM.md
├── SETUP.md                   ← this file
├── orchestrator/
│   ├── __init__.py
│   └── planner.py             ← Orchestrator Agent
├── agents/
│   ├── __init__.py
│   ├── worker_agent.py        ← Worker Agents (parallel)
│   ├── reflection_agent.py    ← Reflection Agent
│   └── validator.py           ← Validator Agent
└── logs/
    └── run_TIMESTAMP.json     ← auto-created after each run
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: groq` | Run `pip install groq` with venv active |
| `AuthenticationError` | Check your GROQ_API_KEY is set correctly |
| `(venv)` not showing | Run `source venv/bin/activate` again |
| JSON parse error | Re-run — model occasionally gives malformed output, retry usually works |
| Rate limit error | Free Groq tier allows 30 req/min — wait 1 min and retry |

---

## Groq Free Tier Limits
- 30 requests/minute
- 14,400 requests/day
- Completely free, no credit card

This is more than enough for your assessment.
