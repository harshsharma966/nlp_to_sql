# Universal NLP-to-SQL Analytics AI

An intelligent, multi-dialect AI analytics platform that converts natural language business questions into safe, optimized SQL queries and generates executive summaries and actionable data insights using local Large Language Models (LLMs).

---

## 🚀 Key Features

- **🌐 Multi-Database Support**: Connect seamlessly to **PostgreSQL**, **MySQL**, and **SQLite**.
- **🔍 Dynamic Real-Time Schema Extraction**: Auto-discovers tables, columns, primary/foreign keys, and inspects sample records on the fly—no hardcoded schemas.
- **🤖 Dialect-Aware SQL Generation**: Generates precise syntax tailored to the connected database engine using local Ollama models (`llama3.1:8b`, `llama3.2:3b`, `qwen2.5-coder`, etc.).
- **🛡️ Multi-Layer Security & Validation**: Enforces strictly read-only execution (`SELECT` / `WITH`); prevents destructive statements (`DROP`, `DELETE`, `UPDATE`, `ALTER`, etc.) and injection attacks.
- **💡 Actionable AI Insights**: Beyond tabular results, generates human-readable executive findings, statistical distributions, and actionable business insights.
- **📊 Modern Web UI**: Built with Streamlit, featuring real-time connection status, interactive table viewers, query inspection, and one-click CSV export.

---

## 🏗️ System Architecture

```
User Query (English)
       │
       ▼
1. Dynamic Schema Extractor (schema_extractor.py)
   ├── Discovers Tables & Column Data Types
   ├── Maps Primary & Foreign Key Relationships
   └── Extracts Sample Rows for Categorical Context
       │
       ▼
2. Query Router & LLM Engine (query_router.py + Ollama)
   ├── Injects Target Dialect Rules (PostgreSQL / MySQL / SQLite)
   └── Generates Read-Only SQL Query
       │
       ▼
3. SQL Safety Validator (validators.py)
   └── Blocks destructive keywords (DROP, DELETE, UPDATE, injection)
       │
       ▼
4. Database Engine (db_engine.py / SQLAlchemy)
   └── Executes query on PostgreSQL / MySQL / SQLite
       │
       ▼
5. Insights Generator (llm_answer.py)
   └── Generates Executive Business Summary & Key Metrics
       │
       ▼
6. Interactive Dashboard (app.py - Streamlit)
   └── Visualizes Results Table, Metrics & Download Options
```

---

## 📂 Project Structure

```
workdesq_ai/
│
├── app.py                  # Main Streamlit web application
├── db_engine.py            # Universal SQLAlchemy connection factory & pooling
├── schema_extractor.py     # Real-time schema inspector & sample data extractor
├── query_router.py         # NLP-to-SQL translation with dialect-specific prompts
├── validators.py           # SQL safety and read-only validation layer
├── sql_executor.py         # Database query execution & pandas dataframe converter
├── llm_answer.py           # Natural language business summary generator
│
├── .env                    # Active environment & database credentials
├── .env.example            # Template for environment variables
├── requirements.txt        # Python package dependencies
└── sample_sales.db         # Sample SQLite database for instant zero-setup testing
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- **Python**: 3.8+ installed
- **Ollama**: Installed and running locally ([ollama.com](https://ollama.com))

### 2. Install Dependencies
```bash
cd workdesq_ai
pip install -r requirements.txt
```

*(Or install core dependencies manually:)*
```bash
pip install streamlit pandas sqlalchemy pymysql mysql-connector-python psycopg2-binary ollama python-dotenv
```

### 3. Pull LLM Model in Ollama
Make sure your Ollama instance is active, then pull the model:
```bash
ollama pull llama3.1:8b
```
*(For low-resource GPUs or 4GB VRAM laptops, you can also use `llama3.2:3b`)*

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser at: **`http://localhost:8501`**

---

## 🔌 Database Connection Options

### Option A: PostgreSQL (Docker Container or Local)
Configure your `.env` file:
```ini
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5433             # Or 5432 depending on your container port mapping
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=nlptosql

OLLAMA_MODEL=llama3.1:8b
OLLAMA_HOST=http://localhost:11434
```
*(The Streamlit UI will auto-fill these values upon loading!)*

### Option B: MySQL
```ini
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

### Option C: SQLite (Instant Zero-Setup Testing)
In the Streamlit sidebar:
1. Select **Database Type**: `SQLite`
2. **File Path**: `sample_sales.db`
3. Click **"🚀 Connect Database"**

---

## 🧪 Verified Example Queries

### 1. Basic Single-Table Queries
- *"Show all employees and their roles"*
- *"List all departments and their locations"*
- *"Show employees with salary greater than 70000"*
- *"List all products sold in sales"*

### 2. Aggregations & Math Calculations
- *"What is the total sales revenue generated so far?"*
- *"What is the average salary of all employees?"*
- *"Who is the highest paid employee and what is their salary?"*

### 3. Multi-Table JOINs
- *"Show all employees with their department name and location"*
- *"Show department-wise total salary expense"*
- *"How many employees are there in each department?"*

### 4. Advanced 3-Table Analytics (Sales + Employees + Departments)
- *"Which employee generated the highest total sales amount?"*
- *"Show each sales record with employee name, department name, product, and amount"*
- *"Show total sales revenue for each product ordered from highest to lowest"*

---

## 🛡️ Security & Read-Only Guarantee

All generated SQL queries pass through `validators.py` before touching the database engine:
- Queries must begin with `SELECT` or `WITH`.
- Destructive commands (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `GRANT`, `SHUTDOWN`) are strictly rejected.
- Multi-statement execution via chained semicolons (`;`) is blocked.

---

## 📜 License
MIT License.
