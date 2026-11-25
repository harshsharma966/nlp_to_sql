from db import get_db

def run_sql(sql):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(sql)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data