from groq import Groq
from utils.prompt_loader import load_prompt

client = Groq()

def generate_sql(question: str, schema: str) -> str:
    base_prompt = load_prompt("sql_prompt.txt")

    prompt = f"""
{base_prompt}

Database Schema:
{schema}

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

    return query


def validate_sql(query: str) -> bool:
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

    for keyword in dangerous_keywords:
        if keyword in query.upper():
            return False

    return query.strip().lower().startswith("select")