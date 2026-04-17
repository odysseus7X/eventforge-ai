import os
from pathlib import Path

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load .env ONLY for local development
load_dotenv()


def _get_env(key: str) -> str:
    """
    Unified env loader:
    Priority:
    1. OS environment variables
    2. Streamlit secrets (if running in Streamlit)
    """

    # 1. Standard env (local + Streamlit runtime)
    val = os.getenv(key)
    if val:
        return val

    # 2. Streamlit secrets (only available in deployed app)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    # 3. Fail fast (important)
    raise ValueError(f"Missing required environment variable: {key}")


def get_llm() -> ChatOpenAI:
    """
    Returns configured ChatOpenAI client.
    Works both locally and on Streamlit Cloud.
    """

    return ChatOpenAI(
        model=_get_env("LLM_MODEL"),
        api_key=_get_env("LLM_API_KEY"),
        base_url=_get_env("LLM_BASE_URL"),
        temperature=0,
        streaming=False,
    )