import streamlit as st
import os
from dotenv import load_dotenv

# Load local .env secrets if present
load_dotenv()

from src.llm_pipeline import (
    generate_sql_query,
    generate_result_summary,
    get_groq_model_name,
    get_openai_client,
)
from src.db_engine import execute_query

st.set_page_config(
    page_title="Cloud Asset NL Search Engine",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ Natural Language Cloud Asset Search Engine")
st.markdown("Search multi-cloud infrastructure assets, security posture, and misconfigurations using plain English.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    if "groq_api_key" not in st.session_state:
        st.session_state["groq_api_key"] = ""

    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state["groq_api_key"],
        key="groq_api_key_input",
        help="Enter your Groq API key for this session. It is not pre-filled to avoid exposing secrets in the UI.",
    )
    if api_key_input.strip():
        st.session_state["groq_api_key"] = api_key_input.strip()

    if "groq_model" not in st.session_state:
        st.session_state["groq_model"] = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    model_name = st.text_input(
        "Groq Model",
        value=st.session_state["groq_model"],
        key="groq_model_input",
        help="Use a model available to your Groq account. The default is openai/gpt-oss-120b.",
    )
    if model_name.strip():
        st.session_state["groq_model"] = model_name.strip()
    else:
        st.session_state["groq_model"] = "openai/gpt-oss-120b"

    os.environ["GROQ_MODEL"] = st.session_state["groq_model"]
    st.caption(f"Active model: {get_groq_model_name()}")

    st.markdown("---")
    st.markdown("### 💡 Example Queries")

    example_queries = [
        "Show me all unencrypted S3 buckets exposed to the public internet.",
        "Which EC2 instances in us-east-1 are currently stopped?",
        "Find security groups allowing global access on port 22.",
        "List public database instances that lack storage encryption.",
        "Which IAM roles have administrator privileges enabled?"
    ]

    selected_example = st.radio("Click an example to load:", example_queries)
    st.session_state["selected_example"] = selected_example

# Main Query Interface
user_query = st.text_area(
    "Enter your cloud inventory question:",
    value=st.session_state.get("selected_example", ""),
    placeholder="Example: Show me all unencrypted S3 buckets exposed to the public internet.",
    height=80,
)

col1, col2 = st.columns([1, 5])
with col1:
    search_clicked = st.button("🔍 Search Assets", type="primary", width="stretch")

if search_clicked:
    query_text = user_query.strip()
    if not query_text:
        st.warning("Please enter a question before searching.")
        st.stop()

    api_key = st.session_state.get("groq_api_key", "").strip()
    if not api_key:
        st.error("Please enter a valid Groq API Key in the sidebar to proceed.")
        st.stop()

    os.environ["GROQ_API_KEY"] = api_key

    with st.spinner("Translating intent into database query..."):
        try:
            client = get_openai_client()
            sql_query = generate_sql_query(query_text, client=client)
            df = execute_query(sql_query)

            col_left, col_right = st.columns([1, 1])

            with col_left:
                st.subheader("Generated SQL Statement")
                st.code(sql_query, language="sql")

            with col_right:
                st.subheader("Executive Summary")
                if not df.empty:
                    summary = generate_result_summary(query_text, df.to_markdown(), client=client)
                    st.info(summary)
                else:
                    st.warning("No resources matched the specified query conditions.")

            st.subheader("Matching Inventory Assets")
            st.dataframe(df, width="stretch")

        except Exception as e:
            st.error(f"Error executing search: {str(e)}")