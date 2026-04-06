from generator.sql_generator import SQLGenerator
from generator.sql_summarizer import SQLSummarizer
from utils.schema_loader import load_schema
from utils.sql_validator import validate_sql
from utils.db_executor import execute_query
from generator.llm_client import LLMClient

DB_PATH = "src/data/raw/day4.db"


class SQLPipeline:
    def __init__(self):
        print("[SQL PIPELINE INIT]")

        self.schema = load_schema(DB_PATH)
        print("\n[SCHEMA LOADED]")
        print(self.schema)

        self.generator = SQLGenerator()
        self.summarizer = SQLSummarizer()
        self.llm = LLMClient()

    def clean_sql(self, sql):
        sql = sql.lower()

        if "select" in sql:
            sql = sql[sql.index("select"):]

        sql = sql.split(";")[0]

        return sql.strip()

    def run(self, question):

        print("\n[STEP 1] Generating SQL...")
        sql = self.generator.generate(question, self.schema)
        sql = self.clean_sql(sql)

        print("SQL:", sql)

        if not sql:
            print("Failed to generate SQL")
            return

        print("\n[STEP 2] Validating...")
        valid, msg = validate_sql(sql)

        if not valid:
            print("Invalid:", msg)
            return

        print("Valid")

        print("\n[STEP 3] Executing...")

        attempts = 2

        for i in range(attempts):

            cols, rows = execute_query(DB_PATH, sql)

            if cols is not None:
                break

            print("Execution Error:", rows)
            print("Retrying...")

            fix_prompt = f"""
Fix this SQL query.

Query:
{sql}

Error:
{rows}

Schema:
{self.schema}

Rules:
- Use only valid tables
- Do not invent tables
- Use case-insensitive matching if needed
- Return ONLY SQL
"""

            sql = self.llm.generate(fix_prompt)
            sql = self.clean_sql(sql)

            print("New SQL:", sql)

        if cols is None:
            print("Failed after retries")
            return

        print("\n[STEP 4] Summarizing...")
        answer = self.summarizer.summarize(question, cols, rows)

        print("\nFINAL ANSWER:")
        print(answer)


if __name__ == "__main__":
    pipeline = SQLPipeline()

    while True:
        q = input("\nAsk SQL Question (or 'exit'): ")

        if q.lower() == "exit":
            break

        pipeline.run(q)