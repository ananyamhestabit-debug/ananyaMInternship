import sys
import os
import re
import logging
from datetime import datetime  #timestamp for code file saveing and dat efor log file
from openai import OpenAI  #openai ka official pyhton client, groq ke liey yehi use krlete 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tools.code_executor import execute_code
from tools.file_agent import write_txt, write_md, read_csv
from tools.db_agent import create_table_from_csv, get_schema, run_sql, DB
from memory.session_memory import SessionMemory
from memory.long_term import LongTermMemory
from memory.vector_store import VectorStore
from config import MODEL_NAME, API_KEY, BASE_URL

OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
LOGS_DIR    = os.path.join(BASE_DIR, "logs")
CSV_PATH    = os.path.join(BASE_DIR, "data", "sales.csv")

# ── LOGGING ────────────────────────────────────────────────────────────────────
os.makedirs(LOGS_DIR, exist_ok=True)
_log_file = os.path.join(LOGS_DIR, f"nexus_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(_log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("nexus")


class NexusAI:

    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)  #groq ka connection bnata 
        self.session_memory   = SessionMemory()  #naya session memeory object : is session ki conversation track krta 
        self.long_term_memory = LongTermMemory()  #sqlit edb connect
        self.vector_store     = VectorStore()
        self._load_long_term_into_vector()
        self._ensure_db_loaded()  #sqlite me jo oehle se memories hain unhe vector store me daal rha
        logger.info(f"NexusAI initialized | model={MODEL_NAME} | vector={self.vector_store.mode} | log={_log_file}")

    # ── STARTUP: load CSV into SQLite once ────────────────────────────────────
    def _ensure_db_loaded(self): #ses ki sales.csv ka data sqlit eme hai ya nhi 
        """Load sales.csv into SQLite DB on startup if table is empty/missing."""
        try:
            import sqlite3
            conn = sqlite3.connect(DB)
            cur  = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM sales")
            count = cur.fetchone()[0]
            conn.close()
            if count == 0:
                raise Exception("empty")
        except Exception:
            if os.path.exists(CSV_PATH):
                data = read_csv(CSV_PATH)
                create_table_from_csv(data)
                logger.info(f"[DB] Loaded {CSV_PATH} → SQLite ({len(data)} rows)")
            else:
                logger.warning(f"[DB] CSV not found at {CSV_PATH}")

    def _load_long_term_into_vector(self):
        for text in self.long_term_memory.retrieve_all():
            self.vector_store.add(text)

    # ── MODEL CALL ─
    # ────────────────────────────────────────────────────────────
    def call_model(self, prompt: str, max_tokens: int = 2048) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=MODEL_NAME,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            if not resp or not resp.choices:
                return "No response from model"
            msg = resp.choices[0].message
            return msg.content.strip() if msg and msg.content else f"(Fallback) {prompt[:100]}..."
        except Exception as e:
            logger.error(f"call_model failed: {e}")
            return f"Error: {e}"

    # ── ROUTER ─────────────────────────────────────────────────────────────────
    def route(self, query: str):
        q = query.lower()

        personal_triggers = [
            "what is my name","what's my name","my name","who am i","do you know me",
            "do you remember me","what do you know about me","what is my age",
            "how old am i","where am i from","where do i live","what is my job","what do i do",
        ]
        if any(t in q for t in personal_triggers):
            return ["personal"]

        # Real-time web search triggers
        if any(w in q for w in [
            "latest", "news", "current events", "today", "right now", "live score",
            "recent", "trending", "what is happening", "search for", "look up",
            "real time", "realtime", "abhi kya", "aaj kya",
        ]):
            return ["search"]

        # CSV / DB / data analysis triggers
        if any(w in q for w in [
            "csv", "sales", "database", "db", "sql", "query", "analyze", "analyse",
            "insight", "top", "revenue", "product", "category", "stock",
            "best selling", "report", "data", "table", "rows", "records",
        ]):
            return ["analyst"]

        if any(w in q for w in ["write code","write a function","implement","python script",
                                  "code for","program to","create a script","generate code","code"]):
            return ["researcher", "coder", "reporter"]

        if any(w in q for w in ["plan","roadmap","schedule","startup","strategy",
                                  "design a","architect","build a system","steps to"]):
            return ["researcher", "optimizer", "reporter"]

        return ["researcher", "reporter"]

    # ── VECTOR MEMORY ──────────────────────────────────────────────────────────
    def recall_similar(self, query: str) -> str:
        results = self.vector_store.search(query, k=3)
        if not results:
            return ""
        return "Relevant past context:\n" + "\n".join(f"- {r}" for r in results)

    def store_to_memory(self, text: str, category: str = "general"):
        self.long_term_memory.store(text, category)
        self.vector_store.add(text)


    # ── WEB SEARCH (Real-time) ─────────────────────────────────────────────────
    def run_search(self, query: str) -> str:
        """Search the web via DuckDuckGo and summarize results with LLM."""
        logger.info(f"[SEARCH] query: {query}")

        results = web_search(query, max_results=5)
        raw_text = format_search_results(results)
        logger.info(f"[SEARCH] {len(results)} results fetched")

        # Ask LLM to summarize the search results into a clean answer
        summary_prompt = (
            f"You are a helpful assistant. Based on these web search results, "
            f"give a clear and concise answer to the user's question.\n\n"
            f"User question: {query}\n\n"
            f"Search results:\n{raw_text}\n\n"
            f"Write a direct, well-structured answer. Mention sources where relevant."
        )
        summary = self.call_model(summary_prompt)
        logger.info(f"[SEARCH] summary generated | len={len(summary)}")

        final = f"{summary}\n\n---\n**Raw Search Results:**\n{raw_text}"
        return final

        # ── ANALYST: CSV → SQL → Insights ─────────────────────────────────────────
    def run_analyst(self, query: str) -> str:
        logger.info("[ANALYST] CSV/DB pipeline started")

        # Step 1: Read CSV directly — source of truth
        try:
            csv_data = read_csv(CSV_PATH)
            columns  = list(csv_data[0].keys()) if csv_data else get_schema()
            # Build a clean markdown table for the LLM
            header   = " | ".join(columns)
            divider  = " | ".join(["---"] * len(columns))
            rows_md  = "\n".join(" | ".join(str(row[c]) for c in columns) for row in csv_data)
            csv_table = f"{header}\n{divider}\n{rows_md}"
            logger.info(f"[ANALYST] loaded {len(csv_data)} rows | columns: {columns}")
        except Exception as e:
            logger.error(f"[ANALYST] CSV read failed: {e}")
            return f"Could not read sales data: {e}"

        # Step 2: Generate ONE simple SQL query
        sql_prompt = (
            f"SQLite table: sales\n"
            f"Columns: {', '.join(columns)}\n"
            f"All columns are TEXT. Use CAST(col AS REAL) for numbers.\n\n"
            f"Write exactly ONE SELECT query for: {query}\n\n"
            f"Rules:\n"
            f"- ONE statement only, no semicolons\n"
            f"- CAST(price AS REAL) and CAST(stock_quantity AS REAL) for numeric ops\n"
            f"- ORDER BY CAST(col AS REAL) for numeric sorting\n"
            f"- Return ONLY the raw SQL — no explanation, no markdown"
        )
        sql_query = self.call_model(sql_prompt, max_tokens=256).strip()
        sql_query = sql_query.replace("```sql","").replace("```","").strip()
        if ";" in sql_query:
            sql_query = sql_query.split(";")[0].strip()
        logger.info(f"[ANALYST] SQL: {sql_query}")

        # Step 3: Run SQL
        db_result = run_sql(sql_query)
        logger.info(f"[ANALYST] DB result: {type(db_result)}")

        if isinstance(db_result, str):
            # SQL failed — use full CSV directly
            logger.warning(f"[ANALYST] SQL failed: {db_result}, using raw CSV")
            result_table = f"(SQL error: {db_result})\nUsing full dataset instead."
            result_for_insight = csv_table
        else:
            cols  = db_result["columns"]
            rows  = db_result["rows"]
            h     = " | ".join(cols)
            d     = " | ".join(["---"] * len(cols))
            lines = "\n".join(" | ".join(str(v) for v in row) for row in rows)
            result_table     = f"{h}\n{d}\n{lines}"
            result_for_insight = result_table
            logger.info(f"[ANALYST] {len(rows)} rows returned")

        # Step 4: Insights ONLY from actual query results
        insight_prompt = (
            f"You are a data analyst. Answer based ONLY on the data below — do not invent numbers.\n\n"
            f"User question: {query}\n\n"
            f"Actual data from database:\n{result_for_insight}\n\n"
            f"Give 3-5 insights using ONLY the exact product names, prices, and numbers shown above.\n"
            f"End with one business recommendation based on this data."
        )
        insights = self.call_model(insight_prompt, max_tokens=1024)
        logger.info(f"[ANALYST] insights len={len(insights)}")

        return (
            f"**SQL executed:**\n```sql\n{sql_query}\n```\n\n"
            f"**Results:**\n| {result_table.replace(chr(10), ' |\n| ')}\n\n"
            f"**Insights:**\n{insights}"
        )

    # ── PERSONAL QUERY ─────────────────────────────────────────────────────────
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

    # ── AGENT PROMPTS ──────────────────────────────────────────────────────────
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

    # ── RUN SINGLE AGENT ───────────────────────────────────────────────────────
    def run_agent(self, agent: str, query: str, pipeline_context: str, memory_context: str = "") -> str:
        logger.info(f"[AGENT:{agent.upper()}] running")
        prompt = self.get_prompt(agent, query, pipeline_context, memory_context)
        output = self.call_model(prompt)
        if not output or output.strip().lower() in ["", "none"]:
            output = self.call_model(f"Context:\n{pipeline_context}\n\nAnswer this helpfully: {query}")
        logger.info(f"[AGENT:{agent.upper()}] done | output_len={len(output)}")
        return output

    # ── SAVE CODE FILES ────────────────────────────────────────────────────────
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
        logger.info(f"[CODE] saved → {py_file}")
        return py_file, md_file

    # ── MAIN RUN ───────────────────────────────────────────────────────────────
    def run(self, query: str) -> dict:
        logger.info("=" * 60)
        logger.info(f"[QUERY] {query}")

        self.session_memory.add_message("User", query)
        context = self.session_memory.get_context()

        memory_context = self.recall_similar(query)
        memory_hits = [line.lstrip("- ") for line in memory_context.split("\n") if line.startswith("- ")] if memory_context else []
        if memory_hits:
            logger.info(f"[MEMORY] {len(memory_hits)} relevant memories recalled")

        agent_sequence = self.route(query)
        logger.info(f"[ROUTER] pipeline = {' → '.join(agent_sequence)}")

        result = {"pipeline": agent_sequence, "steps": [], "memory_hits": memory_hits, "final": ""}

        # ── PERSONAL ──
        if agent_sequence == ["personal"]:
            final_output = self.handle_personal_query(query)
            self.session_memory.add_message("Agent", final_output)
            result["final"] = final_output
            result["steps"].append({"agent": "personal", "output": final_output})
            logger.info("[PERSONAL] answered from stored facts")
            logger.info("=" * 60)
            return result

        # ── WEB SEARCH ──
        if agent_sequence == ["search"]:
            final_output = self.run_search(query)
            self.session_memory.add_message("Agent", final_output)
            summary = f"Q: {query[:120]} | A: {str(final_output)[:200]}"
            self.store_to_memory(summary, category="qa")
            result["final"] = final_output
            result["steps"].append({"agent": "search", "output": final_output})
            logger.info("[DONE] search complete")
            logger.info("=" * 60)
            return result

        # ── ANALYST (CSV/DB) ──
        if agent_sequence == ["analyst"]:
            final_output = self.run_analyst(query)
            self.session_memory.add_message("Agent", final_output)
            summary = f"Q: {query[:120]} | A: {str(final_output)[:200]}"
            self.store_to_memory(summary, category="qa")
            result["final"] = final_output
            result["steps"].append({"agent": "analyst", "output": final_output})
            logger.info(f"[DONE] analyst complete | final_len={len(final_output)}")
            logger.info("=" * 60)
            return result

        # ── NORMAL PIPELINE ──
        pipeline_context = f"Session context:\n{context}\n\nUser query:\n{query}"
        code_output = ""

        for agent in agent_sequence:
            mem_ctx = memory_context if agent == "researcher" else ""
            output  = self.run_agent(agent, query, pipeline_context, mem_ctx)
            result["steps"].append({"agent": agent, "output": output})
            if agent == "coder":
                code_output = output
            pipeline_context = output

        if "coder" in agent_sequence and code_output:
            exec_output = ""
            code_match = re.search(r"```python(.*?)```", code_output, re.DOTALL)
            if code_match:
                exec_output = execute_code(code_match.group(1).strip())
                logger.info(f"[CODE] executed | result_len={len(exec_output)}")
            self.save_code_files(query, code_output, exec_output)

        final_output = pipeline_context
        if not final_output or str(final_output).strip().lower() in ["", "none"]:
            logger.warning("[FALLBACK] empty output, retrying")
            final_output = self.call_model(f"Context:\n{context}\n\nAnswer this helpfully: {query}")

        summary = f"Q: {query[:120]} | A: {str(final_output)[:200]}"
        self.store_to_memory(summary, category="qa")
        self.session_memory.add_message("Agent", final_output)
        result["final"] = final_output

        logger.info(f"[DONE] final_len={len(str(final_output))} | memory_entries={len(self.long_term_memory.retrieve_all())}")
        logger.info("=" * 60)
        return result
