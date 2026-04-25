from groq import Groq
from utils.prompt_loader import load_prompt

client = Groq()  #Groq client object ban gaya->ab isse LLM ko request bhej sakte ho.

#NL->SQL converts(question->sql query): llm use krke sql bnata 
def generate_sql(question: str, schema: str) -> str:  #i/p:user question, and i/p:db schema, o/p:sql query string
    base_prompt = load_prompt("sql_prompt.txt")  #instrcuction template loads
    #db schema + question combine
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
    #deterministic sql
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