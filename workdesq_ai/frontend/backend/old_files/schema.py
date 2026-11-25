from db import get_db

def extract_schema():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    schema_text = []

    for table in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()

        cols = []
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            cols.append(f"{col_name} {col_type}")

        schema_text.append(f"{table}({', '.join(cols)})")

    cursor.close()
    conn.close()

    return "\n".join(schema_text)