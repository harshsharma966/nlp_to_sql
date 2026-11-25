"""
Universal Database Engine Factory
Supports MySQL, PostgreSQL, and SQLite with connection testing and pooling.
"""
from typing import Tuple, Optional
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL
from dotenv import load_dotenv

load_dotenv()


def create_database_engine(
    db_type: str = "mysql",
    host: str = "localhost",
    port: int = 3306,
    user: str = "root",
    password: str = "",
    db_name: str = "",
    sqlite_path: Optional[str] = None
) -> Engine:
    """
    Creates and returns a SQLAlchemy Engine for the specified database dialect.
    """
    db_type = db_type.lower().strip()

    if db_type == "sqlite":
        path = sqlite_path or db_name or "local.db"
        return create_engine(f"sqlite:///{path}")

    elif db_type in ("postgres", "postgresql"):
        connection_url = URL.create(
            drivername="postgresql+psycopg2",
            username=user,
            password=password if password else None,
            host=host,
            port=int(port) if port else 5432,
            database=db_name,
        )
        return create_engine(connection_url, pool_size=5, pool_recycle=3600)

    else:  # default to MySQL
        connection_url = URL.create(
            drivername="mysql+pymysql",
            username=user,
            password=password if password else None,
            host=host,
            port=int(port) if port else 3306,
            database=db_name,
        )
        return create_engine(connection_url, pool_size=5, pool_recycle=3600)


def test_connection(engine: Engine) -> Tuple[bool, str]:
    """
    Verifies that the database engine can successfully connect and execute a ping query.
    Returns (success: bool, message: str).
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, f"Successfully connected to {engine.dialect.name.upper()} database!"
    except Exception as err:
        return False, str(err)


def get_default_engine() -> Engine:
    """
    Creates the default engine from .env environment variables.
    """
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "workdesq_db_new")
    port = int(os.getenv("DB_PORT", 3306))
    db_type = os.getenv("DB_TYPE", "mysql")

    return create_database_engine(
        db_type=db_type,
        host=host,
        port=port,
        user=user,
        password=password,
        db_name=database
    )


# Alias for backwards compatibility
get_engine = get_default_engine
