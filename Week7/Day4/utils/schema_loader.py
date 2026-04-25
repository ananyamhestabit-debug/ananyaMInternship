import sqlite3

#llm ko schema deta hai (DB structure nikalta and padhta hai)
def load_schema(db_path: str) -> str:  # thsi function returns schema string of table and columns
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = ""  #final schema string

    for table in tables:    #tuple se table name nikalte
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()  #us table ke columns

        schema += f"\nTable: {table_name}\nColumns:\n"  #readabel format
        for col in columns:
            schema += f" - {col[1]} ({col[2]})\n"  #col[1]:column name, col[2]:data type

    conn.close()
    return schema