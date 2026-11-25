# Universal NLP-to-SQL — FastAPI & React Stack

This directory contains the **Two-Tier (Client-Server)** version of the Universal NLP-to-SQL platform:
- **Backend**: Python **FastAPI** REST API powered by **Ollama** and universal multi-database engine (PostgreSQL, MySQL, SQLite).
- **Frontend**: **React.js + Vite** single-page application with real-time query execution, SQL inspector, and dynamic data tables.

---

## 🚀 Key Upgrades

- **Powered by Ollama**: Fully replaced legacy GGUF/llama-cpp with local Ollama models (`llama3.1:8b`, `llama3.2:3b`, etc.).
- **Universal Multi-DB Support**: Supports PostgreSQL (including your Docker container), MySQL, and SQLite.
- **Dynamic Real-Time Schema Extraction**: Automatically extracts tables, columns, and foreign keys on the fly.
- **Interactive React UI**: Tabbed interface for AI Insights, generated SQL query, and data table viewer.

---

## ⚡ Quick Start

### 1. Start the FastAPI Backend
Open a terminal:
```bash
cd workdesq_ai/frontend/backend
python start.py
```
- API Server runs at: **`http://localhost:8032`**
- Interactive Swagger API Docs: **`http://localhost:8032/docs`**

---

### 2. Start the React Frontend
Open a second terminal:
```bash
cd workdesq_ai/frontend/frontend
npm install
npm run dev
```
- React Web App runs at: **`http://localhost:5173`**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Check backend & database connection health |
| `GET` | `/schema` | Dynamically extract connected database schema & tables |
| `POST` | `/ask` | Convert English question to SQL via Ollama, execute, and return insights |
| `POST` | `/connect` | Dynamically switch database (PostgreSQL / MySQL / SQLite) |

### Example Request (`POST /ask`):
```json
{
  "query": "Show all employees with their department name and location"
}
```

### Example Response:
```json
{
  "answer": "There are 5 employees in total across Engineering, Sales, and Marketing...",
  "sql": "SELECT e.name, d.dept_name, d.location FROM employees e JOIN departments d ON e.dept_id = d.dept_id",
  "rows": [
    { "name": "Rahul Sharma", "dept_name": "Engineering", "location": "Bengaluru" },
    { "name": "Pooja Verma", "dept_name": "Engineering", "location": "Bengaluru" }
  ],
  "row_count": 2
}
```
