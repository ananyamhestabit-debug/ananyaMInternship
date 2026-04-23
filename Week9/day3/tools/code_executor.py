from autogen.agentchat import AssistantAgent, UserProxyAgent #AssistantAgent → LLM agent (code likhega)/UserProxyAgent → human simulator (execution karega)
import subprocess, tempfile, os, re  #subporcess:code run krne ke liye, regex:pattern matching, tempfile:temp file bnan ekeliey
from config import LLM_CONFIG   #llm ka config(model, api key)

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(HERE), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

#  EXECUTION 
def execute_python(code: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:  #temp file ban rhi hai
        f.write(code)  #llm ka code file me likh diya
        tmp = f.name  #file ka path store

    try:
        #code execute ho rha
        r = subprocess.run(
            ["python3", tmp],
            capture_output=True,  #ouput capture krta hai
            text=True,   #string me convert
            timeout=30    #infinte run avoid
        )
        return r.stdout.strip() or r.stderr.strip() or "No output."

    except subprocess.TimeoutExpired:  #infinite loop stop
        return "ERROR: Timed out."
    except Exception as e:   #unknown error 
        return f"ERROR: {e}"
    finally:
        os.unlink(tmp)   #temp file delete

# save code to permanent file
def save_code_to_file(code: str, filename: str) -> str:
    base = re.sub(r"[^\w\-.]", "_", os.path.basename(filename))
    if not base.endswith(".py"):
        base += ".py"

    path = os.path.join(OUTPUT_DIR, base)

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"\n File saved at: {path}")
    return path

# extract code:llm ke output se python code extract
def extract_code_block(text: str) -> str | None:
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    return m.group(1).strip() if m else None

#query->filename bnata
def infer_filename(query: str) -> str:
    name = re.sub(r"[^a-z0-9\s]", "", query.lower())
    name = "_".join(name.split()[:5])
    return name + ".py"

# prompt
CODE_AGENT_PROMPT = """
You are the Code Agent.

Generate correct, executable Python code.

OUTPUT FORMAT:
1. One-line explanation
2. ONE python code block
3. SAVE_AS: filename.py

RULES:
- Always include demo/test so output is visible
- Always end with SAVE_AS

DATA RULES (CRITICAL):
- If CSV is used:
    import pandas as pd
    df = pd.read_csv("file_path")

    print("Columns:", df.columns)

    df.columns = df.columns.str.lower().str.strip()

    Then use lowercase column names like:
    df.groupby("product")["revenue"].sum()

- NEVER assume column names
"""

# agent:llm agent
code_agent = AssistantAgent(
    name="CodeAgent",
    system_message=CODE_AGENT_PROMPT,  #rules
    llm_config=LLM_CONFIG,
    human_input_mode="NEVER",  #auto run
    max_consecutive_auto_reply=3   #retry
)

# proxy:execution agent : error ho toh fix karwata hai → sahi ho toh save karta hai
class CodeExecutorProxy(UserProxyAgent):

    def __init__(self, original_query: str):
        super().__init__(
            name="CodeProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
            code_execution_config=False,
        )
        self.query = original_query   #state store
        self.done = False

    def generate_reply(self, messages=None, sender=None, **kwargs):  #jab llm reply kre to ye run hota hia

        if self.done:
            return None

        last = (messages or [{}])[-1].get("content", "")  #last message niaklta
        code = extract_code_block(last)   #code nikalta

        if not code:  #safety
            return "Please provide code in ```python block"

        # Execute
        output = execute_python(code)

        # Filename extract
        match = re.search(r"SAVE_AS:\s*(\S+\.py)", last)
        filename = match.group(1) if match else infer_filename(self.query)

        # If error -> retry by llm
        if output.startswith("ERROR") or "Traceback" in output:
            return f"Execution failed:\n{output}\nFix the code."

        # Save
        path = save_code_to_file(code, filename)

        print("\n Executed successfully")
        print(f" Saved → {path}")
        print(f" Output → {output[:200]}")

        self.done = True  #stop loop 
        return None

#new proxy create karta
def make_code_proxy(query: str = "") -> CodeExecutorProxy:
    return CodeExecutorProxy(query)