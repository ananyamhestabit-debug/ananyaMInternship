import sys
import os
import re
from datetime import datetime
from openai import OpenAI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tools.code_executor import execute_code
from tools.file_agent import write_txt, write_md
from memory.session_memory import SessionMemory
from memory.long_term import LongTermMemory
from memory.vector_store import VectorStore
from config import MODEL_NAME, API_KEY, BASE_URL

OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")


class NexusAI:

    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.session_memory   = SessionMemory()
        self.long_term_memory = LongTermMemory()
        self.vector_store     = VectorStore()
        self._load_long_term_into_vector()

    def _load_long_term_into_vector(self):
        for text in self.long_term_memory.retrieve_all():
            self.vector_store.add(text)

    def call_model(self, prompt: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            if not resp or not resp.choices:
                return "No response from model"
            msg = resp.choices[0].message
            return msg.content.strip() if msg and msg.content else f"(Fallback) {prompt[:100]}..."
        except Exception as e:
            return f"Error: {e}"

    def route(self, query: str):
        q = query.lower()
        personal_triggers = [
            "what is my name","what's my name","my name","who am i","do you know me",
            "do you remember me","what do you know about me","what is my age",
            "how old am i","where am i from","where do i live","what is my job","what do i do",
        ]
        if any(t in q for t in personal_triggers):
            return ["personal"]
        if any(w in q for w in ["write code","write a function","implement","python script",
                                  "code for","program to","create a script","generate code","code"]):
            return ["researcher", "coder", "reporter"]
        if any(w in q for w in ["plan","roadmap","schedule","startup","strategy",
                                  "design a","architect","build a system","steps to"]):
            return ["researcher", "optimizer", "reporter"]
        return ["researcher", "reporter"]

    def recall_similar(self, query: str) -> str:
        results = self.vector_store.search(query, k=3)
        if not results:
            return ""
        return "Relevant past context:\n" + "\n".join(f"- {r}" for r in results)

    def store_to_memory(self, text: str, category: str = "general"):
        self.long_term_memory.store(text, category)
        self.vector_store.add(text)

    def handle_personal_query(self, query: str) -> str:
        facts = self.long_term_memory.get_all_facts()
        if not facts:
            return "I don't know anything about you yet!\nTell me something like 'my name is ...' and I'll remember it."
        q = query.lower()
        if any(w in q for w in ["name","who am i","called"]):
            name = facts.get("name")
            return f"Your name is **{name}**." if name else "I don't know your name yet."
        if any(w in q for w in ["age","old"]):
            age = facts.get("age")
            return f"You are **{age}** years old." if age else "I don't know your age yet."
        if any(w in q for w in ["job","work","do"]):
            job = facts.get("job")
            return f"You work as a **{job}**." if job else "I don't know your job yet."
        if any(w in q for w in ["from","live","location"]):
            loc = facts.get("location")
            return f"You are from **{loc}**." if loc else "I don't know your location yet."
        lines = "\n".join(f"  - **{k.title()}**: {v}" for k, v in facts.items())
        return f"Here's everything I know about you:\n{lines}"

    def get_prompt(self, agent: str, query: str, pipeline_context: str, memory_context: str = "") -> str:
        memory_block = f"\n\nVECTOR MEMORY (similar past context):\n{memory_context}" if memory_context else ""
        prompts = {
            "researcher": (
                f"You are a research agent. Answer the following clearly and thoroughly.\n\n"
                f"CONVERSATION CONTEXT:\n{pipeline_context}{memory_block}\n\n"
                f"USER QUERY: {query}\n\n"
                f"Provide well-structured, accurate information. If casual, respond naturally."
            ),
            "coder": (
                f"You are an expert Python developer.\n\nTASK: {query}\n\n"
                f"BACKGROUND FROM RESEARCHER:\n{pipeline_context}\n\n"
                f"Instructions:\n- Write COMPLETE, WORKING Python code\n"
                f"- Wrap ALL code in a single ```python ... ``` block\n"
                f"- Include a runnable example at the bottom\n- Add clear inline comments\n"
                f"- Do NOT write any prose outside the code block"
            ),
            "optimizer": (
                f"You are a strategic planning agent.\n\nORIGINAL REQUEST: {query}\n\n"
                f"RESEARCH OUTPUT:\n{pipeline_context}\n\n"
                f"Restructure into a clear, step-by-step actionable plan with milestones and priorities."
            ),
            "reporter": (
                f"You are the final reporting agent. Produce one clean, complete, final answer.\n\n"
                f"ORIGINAL USER REQUEST: {query}\n\nCONTENT TO PRESENT:\n{pipeline_context}\n\n"
                f"Instructions:\n- If code: keep 100% intact, then plain-English explanation\n"
                f"- If no code: clear, well-structured answer\n- Do NOT repeat yourself\n"
                f"- Be helpful, professional, concise\n- NEVER say 'I cannot answer'"
            ),
        }
        return prompts.get(agent, f"Answer this query helpfully:\n{query}")

    def run_agent(self, agent: str, query: str, pipeline_context: str, memory_context: str = "") -> str:
        prompt = self.get_prompt(agent, query, pipeline_context, memory_context)
        output = self.call_model(prompt)
        if not output or output.strip().lower() in ["", "none"]:
            return self.call_model(f"Context:\n{pipeline_context}\n\nAnswer this helpfully: {query}")
        return output

    def save_code_files(self, query: str, code_output: str, exec_output: str):
        code_match = re.search(r"```python(.*?)```", code_output, re.DOTALL)
        code = code_match.group(1).strip() if code_match else code_output.strip()
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        py_file = os.path.join(OUTPUTS_DIR, f"code_{timestamp}.py")
        md_file = os.path.join(OUTPUTS_DIR, f"code_{timestamp}.md")
        write_txt(py_file, code)
        md_content = (
            "# Code Execution Report\n\n"
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Task:** {query}\n\n---\n\n## Generated Code\n\n```python\n{code}\n```\n\n"
            f"---\n\n## Execution Output\n\n```\n"
            f"{exec_output.strip() if exec_output and exec_output.strip() else 'No output captured.'}\n```\n"
        )
        write_md(md_file, md_content)
        return py_file, md_file

    def run(self, query: str) -> dict:
        """Returns dict with pipeline, steps, memory_hits, final."""
        print("\n=== NEXUS AI ===\n")
        self.session_memory.add_message("User", query)
        context = self.session_memory.get_context()

        memory_context = self.recall_similar(query)
        memory_hits = [line.lstrip("- ") for line in memory_context.split("\n") if line.startswith("- ")] if memory_context else []

        print("[ROUTER]")
        agent_sequence = self.route(query)
        print("Pipeline:", " → ".join(agent_sequence))

        result = {"pipeline": agent_sequence, "steps": [], "memory_hits": memory_hits, "final": ""}

        if agent_sequence == ["personal"]:
            final_output = self.handle_personal_query(query)
            self.session_memory.add_message("Agent", final_output)
            result["final"] = final_output
            result["steps"].append({"agent": "personal", "output": final_output})
            return result

        pipeline_context = f"Session context:\n{context}\n\nUser query:\n{query}"
        code_output = ""

        for agent in agent_sequence:
            print(f"\n[{agent.upper()}]")
            mem_ctx = memory_context if agent == "researcher" else ""
            output = self.run_agent(agent, query, pipeline_context, mem_ctx)
            result["steps"].append({"agent": agent, "output": output})
            if agent == "coder":
                code_output = output
            pipeline_context = output

        if "coder" in agent_sequence and code_output:
            exec_output = ""
            code_match = re.search(r"```python(.*?)```", code_output, re.DOTALL)
            if code_match:
                exec_output = execute_code(code_match.group(1).strip())
            py_file, md_file = self.save_code_files(query, code_output, exec_output)
            print(f"  Code saved: {py_file}")

        final_output = pipeline_context
        if not final_output or str(final_output).strip().lower() in ["", "none"]:
            final_output = self.call_model(f"Context:\n{context}\n\nAnswer this helpfully: {query}")

        summary = f"Q: {query[:120]} | A: {str(final_output)[:200]}"
        self.store_to_memory(summary, category="qa")
        self.session_memory.add_message("Agent", final_output)
        result["final"] = final_output

        print("\n=== FINAL OUTPUT ===")
        print("-" * 50)
        print(final_output)
        print("-" * 50)
        return result
