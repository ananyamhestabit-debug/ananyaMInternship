from generator.llm_client import LLMClient


class SQLGenerator:
    def __init__(self):
        self.llm = LLMClient()

    def generate(self, question, schema):

        prompt = f"""
You are a SQL expert.

DATABASE SCHEMA:
{schema}

IMPORTANT RULES:
- Use only these tables: artists, albums, sales
- Do NOT invent table names
- country is a column inside artists table
- Use case-insensitive matching for text (use COLLATE NOCASE or LOWER())
- Return ONLY SQL query (no explanation)

EXAMPLES:

Q: Show artists from India
SQL: SELECT name FROM artists WHERE country COLLATE NOCASE = 'india';

Q: Which artist has highest revenue
SQL: SELECT artist_id FROM sales ORDER BY revenue DESC LIMIT 1;

Q: List album titles with artist names
SQL: SELECT albums.title, artists.name FROM albums 
JOIN artists ON albums.artist_id = artists.artist_id;

Now generate SQL:

Q: {question}
SQL:
"""

        res = self.llm.generate(prompt)

        # CLEAN OUTPUT
        sql = res.lower()

        if "select" in sql:
            sql = sql[sql.index("select"):]
        else:
            return ""

        sql = sql.split(";")[0]

        return sql.strip()