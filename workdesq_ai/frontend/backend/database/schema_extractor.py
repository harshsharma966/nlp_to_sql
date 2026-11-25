"""
Database schema extraction utility
"""
from .connection import get_db

class SchemaExtractor:
    """Extracts database schema information"""

    @staticmethod
    def extract_schema():
        """
        Extract database schema in a format suitable for LLM

        Returns:
            str: Formatted schema description

        Format:
            table_name(col1 type1, col2 type2, ...)
        """
        conn = get_db()
        cursor = conn.cursor()

        try:
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]

            schema_text = []

            # Get schema for each table
            for table in tables:
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()

                cols = []
                for col in columns:
                    col_name = col[0]
                    col_type = col[1]
                    cols.append(f"{col_name} {col_type}")

                schema_text.append(f"{table}({', '.join(cols)})")

            return "\n".join(schema_text)

        finally:
            cursor.close()
            conn.close()
