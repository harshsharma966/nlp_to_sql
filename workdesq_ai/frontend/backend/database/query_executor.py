"""
SQL query executor
"""
from .connection import get_db

class QueryExecutor:
    """Executes SQL queries safely"""

    @staticmethod
    def execute(sql: str):
        """
        Execute SQL query and return results

        Args:
            sql (str): SQL query to execute

        Returns:
            list: Query results as list of dictionaries

        Raises:
            Exception: If query execution fails
        """
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            return data

        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")

        finally:
            cursor.close()
            conn.close()
