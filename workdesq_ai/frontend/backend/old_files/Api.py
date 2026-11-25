from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_sql import ask_agent_sql

app = FastAPI(title="WorkDesQ Local LLM Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend running"}

@app.post("/ask")
def ask(q: Question):
    answer, rows, sql = ask_agent_sql(q.query)
    return {"answer": answer, "rows": rows, "sql": sql}



# from fastapi import FastAPI
# from pydantic import BaseModel
# from sql_generator import generate_sql
# from db_executor import execute_sql

# app = FastAPI(title="AI SQL Engine")

# class QueryRequest(BaseModel):
#     schema: str
#     question: str

# @app.post("/query")
# def run_query(req: QueryRequest):
#     sql = generate_sql(req.schema, req.question)
#     result = execute_sql(sql)

#     return {
#         "generated_sql": sql,
#         "data": result
#     }