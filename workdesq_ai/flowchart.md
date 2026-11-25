# Universal NLP-to-SQL Analytics Architecture & Workflow

This document illustrates the complete end-to-end data and execution pipeline of the system.

```
┌─────────────────────────────────────────────────────────────┐
│                           START                             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               1. CONNECT ANY SQL DATABASE                   │
│   - Multi-DB Engine: MySQL | PostgreSQL | SQLite            │
│   - Test connection & manage connection pooling             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             2. DYNAMIC SCHEMA EXTRACTION                    │
│   - Auto-inspect tables, column names, and data types       │
│   - Identify primary keys & foreign key relationships       │
│   - Fetch 2 sample rows per table for categorical context   │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 3. USER ENTERS NLP QUESTION                 │
│   Example: "Who are the top 5 most productive employees?"   │
│   (or select from auto-generated quick example chips)       │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           4. DIALECT-AWARE TEXT → SQL GENERATION            │
│   - Model: Local Ollama (Llama 3.1 8B / Qwen 3 Coder)       │
│   - Injects auto-extracted schema + target dialect rules:   │
│       * MySQL:      SUM(CASE WHEN ...), CURDATE()           │
│       * PostgreSQL: ILIKE, ::float division, CURRENT_DATE   │
│       * SQLite:     1.0 * col float math, date('now')       │
│   - Output: Dialect-specific SQL query                      │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               5. SQL SAFETY VALIDATION LAYER                │
│   - Strictly allow only read-only queries (SELECT / WITH)   │
│   - Block destructive commands (DROP, DELETE, UPDATE, etc.) │
│   - Block multi-statement queries (chained semicolons)      │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│        6. EXECUTE SQL QUERY IN CONNECTED DATABASE           │
│   - Run query safely using SQLAlchemy thread-safe session   │
│   - Database: MySQL (3306) | PostgreSQL (5432) | SQLite     │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   7. FETCH QUERY RESULTS                    │
│   - Load results into Pandas DataFrame                      │
│   - Track row counts and execution metrics                  │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                8. FORMAT DATA FOR LLM INPUT                 │
│   - Extract sample rows (top 20 rows)                       │
│   - Compute statistical summary (Min, Max, Avg, Median)     │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              9. AI INSIGHT & SUMMARY GENERATION             │
│   - Input: User question + DataFrame stats + Top rows       │
│   - Model: Ollama LLM                                       │
│   - Output: Executive summary with key findings & trends    │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   10. DASHBOARD DISPLAY                     │
│   - Show:                                                   │
│       * AI Insights & Summary card                          │
│       * Expandable SQL query viewer with syntax highlight   │
│       * Interactive query results data table                │
│       * One-click "Download as CSV" export button           │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                            END                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Component Mapping

| Stage | Responsible Module / File | Description |
| :--- | :--- | :--- |
| **Database Connection** | [`db_engine.py`](db_engine.py) | Multi-database factory for MySQL, PostgreSQL, and SQLite. |
| **Schema Discovery** | [`schema_extractor.py`](schema_extractor.py) | Dynamic schema, key relationships, and data reflection. |
| **User Interface** | [`app.py`](app.py) | Streamlit web interface with DB switcher and model selector. |
| **NLP to SQL** | [`query_router.py`](query_router.py) | Dynamic prompt construction and dialect-specific SQL synthesis. |
| **Security Firewall** | [`validators.py`](validators.py) | Rejects non-SELECT queries and prevents SQL injection chaining. |
| **Query Execution** | [`sql_executor.py`](sql_executor.py) | Runs validated queries and returns Pandas DataFrames. |
| **AI Insights** | [`llm_answer.py`](llm_answer.py) | Synthesizes statistical insights and executive bullet points. |
