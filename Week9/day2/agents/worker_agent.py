import concurrent.futures   #Python module for parallel execution
from groq import Groq  #Used to call LLM API

client = Groq()   #Creates connection to Groq API

# Each role has a different system prompt — strict job separationand role specialization :role ke basis pe prompt select dynamically
ROLE_PROMPTS = {
    "researcher": """You are the Researcher Worker Agent.
Your ONLY job: gather and present factual information relevant to the given instruction.
- Write in clear bullet points
- State ONLY facts and findings
- Do NOT provide analysis or conclusions
- Do NOT write code
Format: Start your response with "RESEARCH FINDINGS:" then bullet points.""",

    "analyst": """You are the Analyst Worker Agent.
Your ONLY job: analyze information and extract insights, patterns, and recommendations.
- Focus on implications and meaning
- Provide structured analysis
- Do NOT do research or gather raw facts
- Do NOT write code unless asked
Format: Start your response with "ANALYSIS REPORT:" then your structured analysis.""",

    "coder": """You are the Coder Worker Agent.
Your ONLY job: write clean, working code solutions.
- Provide code in proper markdown code blocks
- Add brief comments explaining key parts
- Do NOT do research or analysis, only code
- Include example usage
Format: Start your response with "CODE SOLUTION:" then the code block."""
}


def run_single_worker(task: dict) -> dict:
    #Runs one worker for one task, returns result dict
    task_id = task["task_id"]  #dictionary keys access
    role = task["assigned_to"]
    instruction = task["instruction"]

    print(f"  [WORKER-{task_id}] {role.upper()} starting task...")

    system_prompt = ROLE_PROMPTS.get(role, ROLE_PROMPTS["analyst"])  #fallback: if rle exist->use it or fallabakc to analst

#api call to llm
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  #fast inference, good reasoning, available via groq free tier
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction}
        ],
        temperature=0.5,  
        max_tokens=800   #limits output length
    )

    result_text = response.choices[0].message.content.strip()  #removes saces from actual text of first response
    print(f"  [WORKER-{task_id}] {role.upper()} completed ✓")

#reflection agent need structured input
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
