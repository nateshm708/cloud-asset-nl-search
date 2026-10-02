import os
from openai import OpenAI
from src.prompts import TEXT_TO_SQL_SYSTEM_PROMPT
from src.query_sanitizer import sanitize_and_validate_sql


def get_groq_model_name() -> str:
    """Returns the configured Groq model name or a safe default."""
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()
    return model_name or "openai/gpt-oss-120b"


def get_openai_client() -> OpenAI:
    """Initializes and returns the Groq-compatible OpenAI client using environment variables."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY. Please set it in your .env file or environment.")

    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )


def generate_sql_query(user_prompt: str, client: OpenAI = None) -> str:
    """Translates a natural language prompt into a safe SQLite SELECT query string."""
    if client is None:
        client = get_openai_client()

    response = client.chat.completions.create(
        model=get_groq_model_name(),
        temperature=0.0,
        messages=[
            {"role": "system", "content": TEXT_TO_SQL_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw_sql = response.choices[0].message.content.strip()
    is_valid, cleaned_sql = sanitize_and_validate_sql(raw_sql)
    if not is_valid:
        raise ValueError(f"Generated SQL is invalid or unsafe: {cleaned_sql}")

    return cleaned_sql


def generate_result_summary(user_prompt: str, df_markdown: str, client: OpenAI = None) -> str:
    """Generates a brief 1-2 sentence executive summary of the retrieved query findings."""
    if client is None:
        client = get_openai_client()

    summary_prompt = f"""User Asked: "{user_prompt}"
Query Result Data:
{df_markdown}

Provide a concise 1-2 sentence executive summary explaining what was found in the data above. Highlight high-risk security items or actionable findings if any exist."""

    response = client.chat.completions.create(
        model=get_groq_model_name(),
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a concise Cloud Security & IT Audit Analyst."},
            {"role": "user", "content": summary_prompt},
        ],
    )
    return response.choices[0].message.content.strip()