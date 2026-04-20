"""
DAY 2 — Reflection Agent
Reviews all worker outputs and synthesizes/improves them into one coherent response
"""

from groq import Groq

client = Groq()

REFLECTION_SYSTEM_PROMPT = """You are the Reflection Agent in a multi-agent AI system.

Your job: Review outputs from multiple worker agents and synthesize them into ONE improved, coherent response.

You will receive:
- The original user query
- Multiple worker outputs (from researcher, analyst, coder roles)

Your task:
1. Identify gaps, contradictions, or weak points in the worker outputs
2. Synthesize all outputs into a single well-structured response
3. Fill any gaps using your own knowledge
4. Improve clarity and remove redundancy

Output format:
Start with "🔍 REFLECTION NOTES:" — briefly note what you improved or noticed
Then write "📝 SYNTHESIZED RESPONSE:" — the complete improved answer

Be thorough but concise. The final response should be better than any individual worker output."""


def reflect_and_improve(original_query: str, worker_results: list) -> str:
    """
    Takes original query + all worker results,
    returns a synthesized and improved combined response
    """
    print("\n[REFLECTION AGENT] Reviewing all worker outputs...")

    # Build a combined context of all worker outputs
    combined_outputs = ""
    for r in worker_results:
        combined_outputs += f"\n\n--- {r['role'].upper()} (Task {r['task_id']}) ---\n"
        combined_outputs += f"Instruction given: {r['instruction']}\n"
        combined_outputs += f"Output:\n{r['output']}"

    user_message = f"""Original user query: {original_query}

Worker outputs to review and synthesize:
{combined_outputs}

Please reflect, identify improvements, and produce a synthesized response."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": REFLECTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.4,
        max_tokens=1200
    )

    result = response.choices[0].message.content.strip()
    print("[REFLECTION AGENT] Synthesis complete ✓")
    return result
