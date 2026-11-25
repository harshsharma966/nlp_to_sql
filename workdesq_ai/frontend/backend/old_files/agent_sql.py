from llama_cpp import Llama
import re
from schema import extract_schema

# Load model ONCE (important for FastAPI)
llm = Llama(
    model_path="models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf",
    n_ctx=3072,
    n_threads=8,
    n_gpu_layers=35,
    verbose=False,
)

def generate_sql(question: str) -> str:
    """
    Takes a natural language question
    Returns a single executable SQL query
    """

    schema = extract_schema()

    prompt = f"""
You are WorkDesQ AI: an expert MySQL SQL generator for an employee productivity monitoring database.

You must output ONLY ONE executable SQL query and NOTHING ELSE.
No explanation. No markdown. No comments. No extra text.
Always end query with semicolon.

-----------------------
DATABASE SEMANTICS
-----------------------
Core tables used in questions:
- userdetails (employee master): userid, username, depid, location, connected, active, starttime, endtime, os, devicename
- userdata11 (employee activity sessions): userid, startdatetime, enddatetime, duration, status, appname
- department: id, name
- userdata12 (screenshots): userid, time, path, id

MEANING of productivity in this system:
- "Working" status = productive time
- "Distracted" status = distracted time
- "Idle" status = idle time
Productivity percentage:
  SUM(CASE WHEN status='Working' THEN duration ELSE 0 END) / NULLIF(SUM(duration),0) * 100

NEVER define productivity as COUNT(userid) or COUNT(*).
COUNT(*) is for sessions only (like "how many sessions", "how many records").

-----------------------
QUESTION TYPES (STRICT RULES)
-----------------------

1) "Most productive / most disciplined / most efficient employee"
Return TOP 1 employee by:
- productivity_percentage DESC
then total_productive_hours DESC
Use:
- userdetails ud JOIN userdata11 u11 ON ud.userid=u11.userid
- LEFT JOIN department d ON ud.depid=d.id
- WHERE ud.connected=1 (only if question implies current employees)
- GROUP BY ud.userid, ud.username, ud.depid, d.name
- LIMIT 1

2) "Least productive employees"
Return list of employees where productivity_percentage < 60
ORDER BY productivity_percentage ASC
LIMIT 10

3) "Show employees using YouTube"
Filter:
WHERE u11.appname LIKE '%YouTube%'
Return username, department, location, youtube_sessions (COUNT(*)), total_youtube_hours (SUM(duration))
GROUP BY ud.userid, ud.username, d.name, ud.location
ORDER BY total_youtube_hours DESC

4) "Which department has highest productivity" / "Rank departments by productivity"
Compute department_productivity_percentage using same productivity formula but grouped by department
ORDER BY department_productivity_percentage DESC

5) "Today's employee activity"
Filter:
WHERE DATE(u11.startdatetime) = CURDATE()
Return username, department, status, appname, duration, startdatetime, enddatetime
ORDER BY username, startdatetime

6) "Compare Engineering vs Sales productivity"
WHERE d.name IN ('Engineering','Sales')
Return productivity_rate per department

7) "Who is currently online?"
Use userdetails only (optionally join department):
WHERE ud.connected=1 AND TIMESTAMPDIFF(HOUR, ud.active, NOW()) < 1
ORDER BY ud.active DESC

8) "Most used applications"
Use userdata11:
Return application usage stats:
COUNT(*) usage_count, COUNT(DISTINCT userid) unique_users, SUM(duration) total_hours
ORDER BY usage_count DESC LIMIT 20

-----------------------
GENERAL SQL RULES
-----------------------
- Use only columns present in SCHEMA below.
- Do not hallucinate tables/columns.
- Use JOIN patterns exactly like the system expects:
  userdetails ud
  userdata11 u11
  department d
- Use u11 for activity/session data.
- Use ud for employee info.
- When selecting username: use ud.username
- Always use proper GROUP BY when aggregate is used.
- Use NULLIF to avoid divide-by-zero.
- Do NOT filter by CURDATE unless question mentions today/this week/this month.
- For time periods:
  - today: DATE(col)=CURDATE()
  - last 7 days: col >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
  - last 30 days: col >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)

-----------------------
SCHEMA
-----------------------
{schema}

-----------------------
QUESTION
-----------------------
{question}

Return ONLY the SQL query:
"""

    output = llm(
        prompt,
        max_tokens=350,
        temperature=0.0,
        stop=["Explanation", "Reason", "Note", "Answer", "```"]
    )

    raw = output["choices"][0]["text"]

    match = re.search(r"(SELECT[\s\S]+?;)", raw, re.IGNORECASE)
    sql = match.group(1).strip() if match else raw.strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql
