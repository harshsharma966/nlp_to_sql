"""
Configuration settings for the FastAPI Backend.
Loads credentials from .env and supports any database + Ollama.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically load from root workdesq_ai/.env if exists
CORE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PARENT_ENV = CORE_DIR / ".env"
if PARENT_ENV.exists():
    load_dotenv(PARENT_ENV)
load_dotenv()


class Settings:
    # Database configuration
    DB_TYPE = os.getenv("DB_TYPE", "postgresql")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5433"))
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "MyNewPassword123")
    DB_NAME = os.getenv("DB_NAME", "nlptosql")
    SQLITE_PATH = os.getenv("SQLITE_PATH", "sample_sales.db")

    # Ollama LLM configuration
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    # API configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8032"))
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8032",
        "*"
    ]


settings = Settings()
