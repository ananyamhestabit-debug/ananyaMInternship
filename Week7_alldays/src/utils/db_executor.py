import sqlite3


def execute_query(db_path, query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(query)

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        conn.close()

        return cols, rows

    except Exception as e:
        return None, str(e)