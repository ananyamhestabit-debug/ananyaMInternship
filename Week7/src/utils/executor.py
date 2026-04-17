import sqlite3

#sql execute krta hai: SQL query -> database run -> result return
def execute_sql(db_path, sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()  #object hai query run krne wala

    try:
        cursor.execute(sql)  #executes sql query 
        rows = cursor.fetchall()  #saare results list karo
        columns = [desc[0] for desc in cursor.description]

        return columns, rows

    finally:
        conn.close()