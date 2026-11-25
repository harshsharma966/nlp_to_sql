from typing import Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from db_engine import get_default_engine
from validators import validate_sql


def run_sql(query: str, engine: Optional[Engine] = None) -> pd.DataFrame:
    """
    Validates the query for safety (read-only SELECT only, no destructive commands)
    and executes it against the database engine, returning results as a pandas DataFrame.
    """
    if not query or not query.strip():
        raise ValueError("Query string is empty.")

    # Validate query safety before sending to database
    validate_sql(query)

    active_engine = engine or get_default_engine()
    with active_engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return df
