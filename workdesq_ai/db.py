import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Create MySQL database connection.
    Uses environment variables for configuration (Linux-compatible).
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "workdesq_db_new"),
            port=int(os.getenv("DB_PORT", 3306)),
            charset='utf8mb4',
            use_unicode=True,
            autocommit=False
        )
        return conn
    except mysql.connector.Error as err:
        raise Exception(f"Database connection failed: {err}")
