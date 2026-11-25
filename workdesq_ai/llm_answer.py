from typing import Optional
import os
import ollama
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def generate_answer(
    user_question: str,
    df: pd.DataFrame,
    model: Optional[str] = None
) -> str:
    """
    Generate natural language answer from SQL query results using LLM.
    Works for any database table and dataset.
    """
    if df.empty:
        return "📊 No records found matching your criteria. Try modifying your question or adjusting the filters."

    # Analyze the dataframe structure
    num_rows = len(df)
    columns = df.columns.tolist()

    # Convert to structured format for LLM (sample top 20 rows)
    data_summary = df.head(20).to_dict(orient="records")

    # Calculate summary statistics for numeric columns
    stats = {}
    for col in df.select_dtypes(include=['number']).columns:
        stats[col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "avg": round(float(df[col].mean()), 2),
            "median": round(float(df[col].median()), 2)
        }

    try:
        active_model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")

        prompt = f"""You are an expert AI data analyst assistant.

USER QUESTION:
{user_question}

QUERY RESULTS OVERVIEW:
- Total Records Returned: {num_rows}
- Columns: {', '.join(columns)}

DATA SAMPLE (top rows):
{data_summary}

STATISTICAL SUMMARY:
{stats if stats else 'No numeric columns'}

TASK:
Provide a clear, concise, data-driven answer to the user's question based strictly on the query results.

GUIDELINES:
1. Start with a direct answer to the question.
2. Highlight key findings, top/bottom values, and outliers.
3. Use bullet points for readability.
4. Keep conclusions professional, accurate, and actionable.
5. Limit response to 4-6 concise bullet points.
"""

        resp = ollama.chat(
            model=active_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert data analyst assistant. "
                        "Analyze query results and provide clear, concise, "
                        "and data-driven natural language insights answering the user's question."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.3,
                "top_p": 0.9
            }
        )

        return resp["message"]["content"].strip()

    except Exception as e:
        return f"""⚠️ Found {num_rows} records. Could not generate AI summary ({str(e)}).
Columns available: {', '.join(columns)}
Please inspect the results table below."""
