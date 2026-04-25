import sqlite3

#It executes a SQL query on the database and returns column names and result rows: SQL query -> database run -> result return
def execute_sql(db_path, sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()  #object hai query run krne wala

    try:
        cursor.execute(sql)  #executes sql query 
        rows = cursor.fetchall()  #saare results list karo
        columns = [desc[0] for desc in cursor.description]  #cursor.des: gives metadata and desc[0]: column name toh metadat ka column name first wala

        return columns, rows

    finally:
        conn.close()