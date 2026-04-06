from generator.llm_client import LLMClient


class SQLSummarizer:
    def __init__(self):
        self.llm = LLMClient()

    def summarize(self, question, columns, rows):

        prompt = f"""
You are a data analyst.

User Question:
{question}

Query Result:
Columns: {columns}
Rows: {rows[:5]}

Task:
- Explain result in simple English
- Highlight key insight
- Do NOT repeat raw numbers fully
- Keep answer short (2-3 lines)

Answer:
"""

        return self.llm.generate(prompt)