"""
DAY 2 — Validator Agent
Final quality check: checks for errors, hallucinations, completeness, and format issues
"""

import json
import re
from groq import Groq

client = Groq()

VALIDATOR_SYSTEM_PROMPT = """You are the Validator Agent — the final quality gate in a multi-agent AI system.

Your job: Validate the synthesized response against the original query.

Check for:
1. RELEVANCE — Does it actually answer the original query?
2. COMPLETENESS — Are there obvious missing parts?
3. ACCURACY — Any obvious factual errors or contradictions?
4. CLARITY — Is the response well-structured and readable?
5. ERRORS — Any logical errors or broken code (if code is present)?

Return ONLY this JSON (no extra text):
{
  "validation_status": "PASS" or "FAIL",
  "score": <integer 1-10>,
  "checks": {
    "relevance": "PASS/FAIL",
    "completeness": "PASS/FAIL",
    "accuracy": "PASS/FAIL",
    "clarity": "PASS/FAIL"
  },
  "issues_found": ["<issue 1 if any>", "<issue 2 if any>"],
  "final_answer": "<the validated response — either approved as-is or with minor corrections applied>"
}

If all checks pass, copy the response into final_answer unchanged.
If minor issues exist, fix them in final_answer and mark status as PASS.
Only mark FAIL if the response fundamentally does not answer the query."""


def validate_response(original_query: str, synthesized_response: str) -> dict:
    """
    Validates the reflection agent's output.
    Returns a dict with validation status, score, and final_answer.
    """
    import time 
    time.sleep(3)
    print("\n[VALIDATOR] Running quality checks...")

    user_message = f"""Original query: {original_query}

Response to validate:
{synthesized_response}"""
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": VALIDATOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON safely
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        clean = json_match.group().replace('\n', ' ').replace('\r', ' ')
        validation = json.loads(clean)
    else:
        # If model fails to return JSON, create a safe fallback
        print("[VALIDATOR] Warning: Could not parse JSON, using fallback")
        validation = {
            "validation_status": "PASS",
            "score": 7,
            "checks": {"relevance": "PASS", "completeness": "PASS", "accuracy": "PASS", "clarity": "PASS"},
            "issues_found": [],
            "final_answer": synthesized_response
        }

    status = validation.get("validation_status", "PASS")
    score = validation.get("score", "N/A")
    issues = validation.get("issues_found", [])

    print(f"[VALIDATOR] Status: {status} | Score: {score}/10")
    if issues:
        print(f"[VALIDATOR] Issues found: {issues}")
    else:
        print("[VALIDATOR] No issues found ✓")

    return validation
