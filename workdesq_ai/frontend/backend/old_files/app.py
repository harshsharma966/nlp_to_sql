import streamlit as st
import pandas as pd
from agent_sql import ask_agent_sql

st.set_page_config(page_title="WorkDesQ AI (SQL Agent)", layout="wide")
st.title("🤖 WorkDesQ AI")

user_q = st.text_input("Ask your question:", placeholder="Who has the best work habits?")

# if st.button("Submit"):
#     if not user_q.strip():
#         st.warning("Please type a question.")
#         st.stop()

#     try:
#         with st.spinner("Thinking..."):
#             answer, rows, sql_query = ask_agent_sql(user_q)

#         st.subheader("✅ Final Answer")
#         st.success(answer)

#         with st.expander("🧾 SQL Generated"):
#             st.code(sql_query, language="sql")

#         if rows:
#             st.subheader("📋 Result Table")
#             st.dataframe(pd.DataFrame(rows), use_container_width=True)
#         else:
#             st.info("No rows returned.")

#     except Exception as e:
#         st.error("❌ Backend crashed due to error (SQL/API/DB issue).")
#         st.code(str(e))

if st.button("Submit"):
    try:
        with st.spinner("Thinking..."):
            st.write("Submitting query...")

            answer, rows, sql_query = ask_agent_sql(user_q)

        st.success(answer)
    except Exception as e:
        st.error("❌ Error occurred")
        st.code(str(e))

