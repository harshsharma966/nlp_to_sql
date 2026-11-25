#!/usr/bin/env python3
"""
Quick Start Script for Universal NLP-to-SQL FastAPI Backend
"""
import sys
import os
from pathlib import Path

# Add root workdesq_ai directory to path
CORE_DIR = Path(__file__).resolve().parent.parent.parent
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from config.settings import settings
from db_engine import get_default_engine, test_connection


def check_dependencies():
    """Check if required python packages are installed"""
    required = ['fastapi', 'uvicorn', 'ollama', 'sqlalchemy', 'pandas', 'dotenv']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstall with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    print("✅ All Python dependencies are installed.")
    return True


def check_database():
    """Check database connection"""
    try:
        engine = get_default_engine()
        ok, msg = test_connection(engine)
        if ok:
            print(f"✅ Database connection successful: {engine.dialect.name.upper()} ({settings.DB_NAME})")
            return True
        else:
            print(f"❌ Database connection failed: {msg}")
            return False
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def check_ollama():
    """Check if Ollama is accessible"""
    try:
        import ollama
        res = ollama.list()
        models = [m.get("model") or m.get("name") for m in res.get("models", [])]
        print(f"✅ Ollama connected! Available models: {', '.join(models) if models else 'None'}")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not reach Ollama at {settings.OLLAMA_HOST}: {e}")
        print("   Make sure Ollama is running ('ollama serve')")
        return True


def main():
    print("🚀 Starting Universal NLP-to-SQL FastAPI Backend\n")

    if not check_dependencies():
        sys.exit(1)

    check_database()
    check_ollama()

    print(f"\n🌐 Server starting on http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📘 API Docs available at http://localhost:{settings.API_PORT}/docs\n")

    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )


if __name__ == "__main__":
    main()
