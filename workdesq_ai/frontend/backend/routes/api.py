"""
API Routes - FastAPI endpoint definitions
Universal NLP-to-SQL powered by Ollama and SQLAlchemy (PostgreSQL / MySQL / SQLite)
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Add parent workdesq_ai directory to path to use universal core modules
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from db_engine import create_database_engine, get_default_engine, test_connection
from schema_extractor import SchemaExtractor
from query_router import get_sql_from_nlp
from sql_executor import run_sql
from llm_answer import generate_answer
from validators import SQLValidationError

router = APIRouter()

# Global active database engine instance
_current_engine = None


def get_active_engine():
    global _current_engine
    if _current_engine is None:
        _current_engine = get_default_engine()
    return _current_engine


# Request/Response models
class QuestionRequest(BaseModel):
    query: str
    model: Optional[str] = None


class QuestionResponse(BaseModel):
    answer: str
    sql: str
    rows: List[Dict[str, Any]]
    row_count: int


class ConnectRequest(BaseModel):
    db_type: str = "postgresql"  # postgresql, mysql, sqlite
    host: Optional[str] = "localhost"
    port: Optional[int] = 5433
    user: Optional[str] = "postgres"
    password: Optional[str] = ""
    db_name: Optional[str] = "nlptosql"
    sqlite_path: Optional[str] = None


# Routes
@router.get("/")
def root():
    """Root info endpoint"""
    return {
        "title": "Universal NLP-to-SQL API",
        "llm": "Ollama",
        "status": "running"
    }


@router.get("/health")
def health():
    """
    Check backend & database connection health
    """
    try:
        engine = get_active_engine()
        ok, msg = test_connection(engine)
        if ok:
            return {
                "status": "healthy",
                "database": engine.dialect.name.upper(),
                "db_name": getattr(engine.url, "database", "connected"),
                "message": msg
            }
        else:
            return {
                "status": "degraded",
                "database": "disconnected",
                "error": msg
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@router.post("/connect")
def connect_database(req: ConnectRequest):
    """
    Dynamically connect to any database (PostgreSQL, MySQL, SQLite)
    """
    global _current_engine
    try:
        engine = create_database_engine(
            db_type=req.db_type,
            host=req.host or "localhost",
            port=req.port or 3306,
            user=req.user or "root",
            password=req.password or "",
            db_name=req.db_name or "",
            sqlite_path=req.sqlite_path
        )
        ok, msg = test_connection(engine)
        if not ok:
            raise HTTPException(status_code=400, detail=f"Database connection failed: {msg}")

        _current_engine = engine
        return {
            "status": "connected",
            "dialect": engine.dialect.name,
            "message": msg
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting: {str(e)}")


@router.get("/schema")
def get_schema():
    """
    Dynamically extract database schema
    """
    try:
        engine = get_active_engine()
        meta = SchemaExtractor.extract_schema_metadata(engine)
        return {
            "dialect": engine.dialect.name,
            "tables": list(meta["tables"].keys()),
            "schema": meta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract schema: {str(e)}")


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    """
    Universal endpoint:
    1. Extract schema dynamically
    2. Convert NLP to SQL using Ollama
    3. Validate and execute SQL
    4. Generate business answer using Ollama
    """
    question = request.query.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        engine = get_active_engine()

        # Step 1: Format dynamic schema context for the prompt
        schema_text = SchemaExtractor.format_schema_for_prompt(engine)

        # Step 2: Generate dialect-aware SQL via Ollama
        sql = get_sql_from_nlp(
            user_query=question,
            schema_context=schema_text,
            dialect=engine.dialect.name,
            model=request.model
        )

        # Step 3: Execute safe SQL query
        df = run_sql(sql, engine)

        # Step 4: Generate executive AI answer via Ollama
        answer = generate_answer(
            user_question=question,
            df=df,
            model=request.model
        )

        # Format rows for JSON response
        records = df.to_dict(orient="records")

        return QuestionResponse(
            answer=answer,
            sql=sql,
            rows=records,
            row_count=len(records)
        )

    except SQLValidationError as e:
        raise HTTPException(status_code=400, detail=f"SQL Validation Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")
