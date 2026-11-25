"""
Universal Query Router - NLP to SQL
Converts natural language questions to SQL for any database dialect (MySQL, PostgreSQL, SQLite).
"""
from typing import Optional
import os
import re
import ollama
from dotenv import load_dotenv

load_dotenv()

def get_sql_from_nlp(
    user_query: str,
    schema_context: Optional[str] = None,
    dialect: str = "mysql",
    model: Optional[str] = None
) -> str:
    """
    Translates a natural language question into an optimized, executable SQL query
    tailored to the target database dialect and dynamic schema.
    """
    if not schema_context or not schema_context.strip():
        raise ValueError("No database schema provided. Please connect a database first.")

    active_model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    active_schema = schema_context.strip()
    dialect_upper = dialect.upper()

    # Dialect-specific guidance
    dialect_notes = ""
    if "POSTGRES" in dialect_upper:
        dialect_notes = """
DIALECT RULES FOR POSTGRESQL:
- Use standard PostgreSQL syntax (NO MySQL backticks ``, use double quotes "" or plain names).
- IMPORTANT: If querying information_schema.tables or information_schema.columns to inspect metadata, ALWAYS filter with: table_schema = 'public' (e.g., WHERE table_schema = 'public' AND table_type = 'BASE TABLE'). Never query information_schema without filtering for 'public', otherwise PostgreSQL internal system catalog tables are included.
- For float division, cast integers using ::float (e.g., col::float / NULLIF(total, 0)).
- Use ILIKE for case-insensitive string matching.
- Use CURRENT_DATE for today's date.
- All non-aggregate columns in SELECT must appear in GROUP BY.
"""
    elif "SQLITE" in dialect_upper:
        dialect_notes = """
DIALECT RULES FOR SQLITE:
- Use standard SQLite syntax.
- Use date('now') or datetime('now') for current timestamps.
- Use 1.0 * col for floating point math.
"""
    else:  # MySQL
        dialect_notes = """
DIALECT RULES FOR MYSQL:
- Use valid MySQL syntax.
- NEVER use SUM(col WHERE cond). ALWAYS use SUM(CASE WHEN cond THEN col ELSE 0 END).
- Use NULLIF(col, 0) to prevent division by zero.
- Use CURDATE() for current date.
"""

    prompt = f"""{active_schema}
{dialect_notes}

USER QUESTION:
{user_query}

TASK:
Write a single, safe, read-only {dialect_upper} query to answer the user's question.
Return ONLY raw SQL. Do not include markdown code blocks, explanations, or notes.
"""

    resp = ollama.chat(
        model=active_model,
        messages=[
            {
                "role": "system",
                "content": f"You are a database expert. You output ONLY valid, executable {dialect_upper} SELECT queries with no markdown, backticks, or commentary."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={"temperature": 0.1}
    )

    sql = resp["message"]["content"].strip()

    # Clean markdown formatting if model wrapped in ```sql ... ```
    sql = re.sub(r"^```(?:sql|postgresql|mysql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```$", "", sql).strip()

    # MySQL-specific auto-fix for common LLM aggregation mistakes
    if "MYSQL" in dialect_upper:
        sql = re.sub(
            r"SUM\((\w+(?:\.\w+)?)\s+WHERE\s+([^)]+)\)",
            r"SUM(CASE WHEN \2 THEN \1 ELSE 0 END)",
            sql,
            flags=re.IGNORECASE
        )

    return sql.rstrip(";")
