import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import ollama

load_dotenv()

from db_engine import create_database_engine, test_connection
from schema_extractor import SchemaExtractor
from query_router import get_sql_from_nlp
from sql_executor import run_sql
from llm_answer import generate_answer
from validators import SQLValidationError

st.set_page_config(
    page_title="Universal NLP-to-SQL Analytics",
    page_icon="🧠",
    layout="wide"
)

# Initialize Session State
if "engine" not in st.session_state:
    st.session_state.engine = None
if "schema_text" not in st.session_state:
    st.session_state.schema_text = None
if "schema_meta" not in st.session_state:
    st.session_state.schema_meta = None
if "db_name" not in st.session_state:
    st.session_state.db_name = None
if "dialect" not in st.session_state:
    st.session_state.dialect = "mysql"

# --- SIDEBAR: DATABASE & MODEL CONFIGURATION ---
st.sidebar.title("⚙️ Database Connection")

# Get list of local Ollama models
try:
    ollama_res = ollama.list()
    available_models = [m.get("model") or m.get("name") for m in ollama_res.get("models", [])]
    if not available_models:
        available_models = ["llama3.1:8b"]
except Exception:
    available_models = ["llama3.1:8b", "llama3:8b", "qwen3-coder:30b"]

# Default model index
default_idx = available_models.index("llama3.1:8b") if "llama3.1:8b" in available_models else 0
selected_model = st.sidebar.selectbox("🤖 Select LLM Model:", available_models, index=default_idx)

# Database Connection Form (Direct Universal Connection - Auto-loads from .env if present)
db_options = ["PostgreSQL", "MySQL", "SQLite"]
env_type = os.getenv("DB_TYPE", "postgresql").lower()
default_db_idx = 0 if "postgres" in env_type else (1 if "mysql" in env_type else (2 if "sqlite" in env_type else 0))
db_type = st.sidebar.selectbox("Database Type:", db_options, index=default_db_idx)

if db_type == "SQLite":
    sqlite_path = st.sidebar.text_input(
        "SQLite File Path:",
        value=os.getenv("SQLITE_PATH", ""),
        placeholder="e.g. sample_sales.db or C:/path/to/database.db",
        help="Enter path to your .db / .sqlite file"
    )
    custom_host, custom_port, custom_user, custom_pass, custom_db = "", 0, "", "", ""
else:
    default_port = int(os.getenv("DB_PORT", 5432 if db_type == "PostgreSQL" else 3306))
    col1, col2 = st.sidebar.columns([2, 1])
    custom_host = col1.text_input("Host:", value=os.getenv("DB_HOST", "localhost"), placeholder="e.g. localhost")
    custom_port = col2.number_input("Port:", value=default_port, step=1)
    custom_db = st.sidebar.text_input("Database Name:", value=os.getenv("DB_NAME", ""), placeholder="Enter database name")
    custom_user = st.sidebar.text_input("User:", value=os.getenv("DB_USER", ""), placeholder="Enter username")
    custom_pass = st.sidebar.text_input("Password:", type="password", value=os.getenv("DB_PASSWORD", ""), placeholder="Enter password")

if st.sidebar.button("🚀 Connect Database", use_container_width=True):
    try:
        with st.spinner(f"Connecting to {db_type}..."):
            if db_type == "SQLite":
                if not sqlite_path.strip():
                    st.sidebar.error("⚠️ Please enter SQLite file path.")
                else:
                    engine = create_database_engine(db_type="sqlite", sqlite_path=sqlite_path.strip())
                    db_label = sqlite_path.strip()
                    ok, msg = test_connection(engine)
                    if ok:
                        st.session_state.engine = engine
                        st.session_state.dialect = engine.dialect.name
                        st.session_state.db_name = db_label
                        with st.spinner("Extracting schema metadata..."):
                            st.session_state.schema_meta = SchemaExtractor.extract_schema_metadata(engine)
                            st.session_state.schema_text = SchemaExtractor.format_schema_for_prompt(engine)
                        st.sidebar.success(f"🟢 Connected to {db_label} ({engine.dialect.name.upper()})")
                    else:
                        st.sidebar.error(f"🔴 Connection Failed: {msg}")
            else:
                host_val = custom_host.strip() if custom_host.strip() else "localhost"
                if not custom_db.strip():
                    st.sidebar.error("⚠️ Please enter Database Name.")
                elif not custom_user.strip():
                    st.sidebar.error("⚠️ Please enter Username.")
                else:
                    engine = create_database_engine(
                        db_type=db_type.lower(),
                        host=host_val,
                        port=custom_port,
                        user=custom_user.strip(),
                        password=custom_pass,
                        db_name=custom_db.strip()
                    )
                    db_label = custom_db.strip()
                    ok, msg = test_connection(engine)
                    if ok:
                        st.session_state.engine = engine
                        st.session_state.dialect = engine.dialect.name
                        st.session_state.db_name = db_label
                        with st.spinner("Extracting schema metadata..."):
                            st.session_state.schema_meta = SchemaExtractor.extract_schema_metadata(engine)
                            st.session_state.schema_text = SchemaExtractor.format_schema_for_prompt(engine)
                        st.sidebar.success(f"🟢 Connected to {db_label} ({engine.dialect.name.upper()})")
                    else:
                        st.sidebar.error(f"🔴 Connection Failed: {msg}")
    except Exception as e:
        st.sidebar.error(f"🔴 Connection Error: {str(e)}")

# --- SCHEMA EXPLORER IN SIDEBAR ---
if st.session_state.schema_meta and st.session_state.schema_meta.get("tables"):
    with st.sidebar.expander("📚 Discovered Tables & Columns", expanded=False):
        for tbl_name, tbl_info in st.session_state.schema_meta["tables"].items():
            st.markdown(f"**📄 `{tbl_name}`**")
            cols_summary = [f"{c['name']} ({c['type']})" for c in tbl_info["columns"]]
            st.caption(", ".join(cols_summary))


# --- MAIN APPLICATION AREA ---
st.title("🧠 Universal NLP-to-SQL Analytics")
st.markdown("Ask natural language questions in plain English to automatically query **any** connected SQL database.")

# Connection status banner
if st.session_state.engine is not None:
    tables_count = len(st.session_state.schema_meta["tables"]) if st.session_state.schema_meta else 0
    st.success(
        f"🟢 **Connected Database:** `{st.session_state.db_name}` | "
        f"**Dialect:** `{st.session_state.dialect.upper()}` | "
        f"**Discovered Tables:** `{tables_count}` | "
        f"**Model:** `{selected_model}`"
    )
else:
    st.warning("⚠️ No active database connection. Please click **'Connect'** in the sidebar to get started.")

# Quick Example suggestions
selected_example = None
if st.session_state.schema_meta and st.session_state.schema_meta.get("tables"):
    available_tbls = list(st.session_state.schema_meta["tables"].keys())
    
    # Generate dynamic suggestions based on detected tables
    first_tbl = available_tbls[0]
    second_tbl = available_tbls[1] if len(available_tbls) > 1 else first_tbl
    example_queries = [
        f"Show top 10 records from {first_tbl}",
        f"How many total records are in {first_tbl}?",
        f"Summarize data in {second_tbl}"
    ]

    st.markdown("**Quick Examples:**")
    cols = st.columns(len(example_queries))
    for i, ex in enumerate(example_queries):
        if cols[i].button(ex, key=f"ex_{i}", use_container_width=True):
            selected_example = ex

# Question Input
user_query = st.text_input(
    "Ask your question in natural language (NLP):",
    value=selected_example or "",
    placeholder="e.g. Show top 10 most productive employees"
)

run_button = st.button("🚀 Analyze & Query Database", type="primary")

if run_button or selected_example:
    if not st.session_state.engine:
        st.error("Please connect to a database in the sidebar first.")
    elif not user_query.strip():
        st.warning("Please enter a question to analyze.")
    else:
        try:
            # Step 1: Generate SQL query with LLM
            with st.spinner(f"🤖 Generating {st.session_state.dialect.upper()} query with {selected_model}..."):
                sql = get_sql_from_nlp(
                    user_query=user_query,
                    schema_context=st.session_state.schema_text,
                    dialect=st.session_state.dialect,
                    model=selected_model
                )

            # Step 2: Show Generated SQL in code block
            with st.expander("🔍 View Generated SQL Query", expanded=True):
                st.code(sql, language="sql")

            # Step 3: Execute SQL query safely
            with st.spinner("⚡ Executing query against database..."):
                df = run_sql(sql, engine=st.session_state.engine)

            # Step 4: Generate AI insights
            with st.spinner("💡 Synthesizing insights with AI..."):
                answer = generate_answer(user_query, df, model=selected_model)

            # Display Insights
            st.subheader("💡 AI Insights & Summary")
            st.info(answer)

            # Display Data Table & Metrics
            st.subheader(f"📋 Query Results ({len(df)} rows)")
            st.dataframe(df, use_container_width=True)

            # CSV Download button
            if not df.empty:
                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_data,
                    file_name="query_results.csv",
                    mime="text/csv"
                )

        except SQLValidationError as sve:
            st.error(f"🛑 Security Block: {sve}")
        except Exception as e:
            st.error(f"⚠️ Query Execution Error: {str(e)}")
