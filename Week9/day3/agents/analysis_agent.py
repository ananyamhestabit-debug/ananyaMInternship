"""
DAY 3 — Analysis Agent
Synthesizes outputs from all tool agents into final business insights
"""

import time
from groq import Groq

client = Groq()

ANALYSIS_PROMPT = """You are the Analysis Agent in a multi-agent AI system.

Your job: Take outputs from multiple tool agents (file reader, code executor, database queries)
and synthesize them into clear, actionable business insights.

Format your response as:
📊 FINAL ANALYSIS REPORT
========================

**Key Findings:**
1. ...
2. ...

**Top Insights:**
1. ...

**Recommendations:**
1. ...

Be specific, use numbers from the data, and be concise."""


def run_analysis_agent(original_query: str, tool_outputs: list) -> str:
    """Synthesizes all tool outputs into final insights"""
    print(f"\n[ANALYSIS AGENT] Synthesizing {len(tool_outputs)} tool outputs...")

    combined = f"Original query: {original_query}\n\n"
    for out in tool_outputs:
        combined += f"=== {out['agent'].upper()} OUTPUT ===\n"
        combined += out["output"] + "\n\n"

    time.sleep(3)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": ANALYSIS_PROMPT},
            {"role": "user", "content": combined}
        ],
        temperature=0.4,
        max_tokens=1000
    )

    result = response.choices[0].message.content.strip()
    print("[ANALYSIS AGENT] Synthesis complete ✓")
    return result
