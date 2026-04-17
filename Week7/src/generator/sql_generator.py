from groq import Groq
from utils.prompt_loader import load_prompt

client = Groq()

#NL->SQL converts(question->sql query)
def generate_sql(question: str, schema: str) -> str:
    base_prompt = load_prompt("sql_prompt.txt")

    prompt = f"""
{base_prompt}

Database Schema:
{schema}

STRICT RULES:
- Use ONLY table names from schema
- Use ONLY column names from schema
- DO NOT invent tables
- DO NOT invent columns
- ONLY SELECT queries

User Question:
{question}

SQL:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    query = response.choices[0].message.content.strip()
    query = query.replace("```sql", "").replace("```", "").strip()

    if query.endswith(";"):
        query = query[:-1]

    return query