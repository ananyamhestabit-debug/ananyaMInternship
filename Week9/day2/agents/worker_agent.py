"""
DAY 2 — Worker Agent
Executes assigned tasks in parallel (researcher / analyst / coder roles)
"""

import concurrent.futures
from groq import Groq

client = Groq()

# Each role has a different system prompt — strict job separation
ROLE_PROMPTS = {
    "researcher": """You are the Researcher Worker Agent.
Your ONLY job: gather and present factual information relevant to the given instruction.
- Write in clear bullet points
- State ONLY facts and findings
- Do NOT provide analysis or conclusions
- Do NOT write code
Format: Start your response with "📋 RESEARCH FINDINGS:" then bullet points.""",

    "analyst": """You are the Analyst Worker Agent.
Your ONLY job: analyze information and extract insights, patterns, and recommendations.
- Focus on implications and meaning
- Provide structured analysis
- Do NOT do research or gather raw facts
- Do NOT write code unless asked
Format: Start your response with "📊 ANALYSIS REPORT:" then your structured analysis.""",

    "coder": """You are the Coder Worker Agent.
Your ONLY job: write clean, working code solutions.
- Provide code in proper markdown code blocks
- Add brief comments explaining key parts
- Do NOT do research or analysis, only code
- Include example usage
Format: Start your response with "💻 CODE SOLUTION:" then the code block."""
}


def run_single_worker(task: dict) -> dict:
    """Runs one worker for one task, returns result dict"""
    task_id = task["task_id"]
    role = task["assigned_to"]
    instruction = task["instruction"]

    print(f"  [WORKER-{task_id}] {role.upper()} starting task...")

    system_prompt = ROLE_PROMPTS.get(role, ROLE_PROMPTS["analyst"])

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction}
        ],
        temperature=0.5,
        max_tokens=800
    )

    result_text = response.choices[0].message.content.strip()
    print(f"  [WORKER-{task_id}] {role.upper()} completed ✓")

    return {
        "task_id": task_id,
        "role": role,
        "instruction": instruction,
        "output": result_text
    }


def run_workers_parallel(tasks: list) -> list:
    """
    Runs all worker tasks in PARALLEL using ThreadPoolExecutor.
    Returns list of results in order.
    """
    print(f"\n[WORKERS] Starting {len(tasks)} workers in PARALLEL...")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_task = {executor.submit(run_single_worker, task): task for task in tasks}
        for future in concurrent.futures.as_completed(future_to_task):
            result = future.result()
            results.append(result)

    # Sort by task_id so output is always ordered T1, T2, T3...
    results.sort(key=lambda x: x["task_id"])
    print(f"[WORKERS] All {len(tasks)} workers completed ✓")
    return results
