"""
LLM client factory.

All configuration via environment variables — switch providers by changing .env only.
Uses the OpenAI-compatible API format, which all major providers support.

Supported providers (set LLM_BASE_URL accordingly):
  - OpenRouter   → https://openrouter.ai/api/v1
  - Mistral      → https://api.mistral.ai/v1
  - Groq         → https://api.groq.com/openai/v1
  - Google (via OpenRouter, recommended over direct Gemini API)
  - OpenAI       → leave LLM_BASE_URL unset
  - Ollama       → http://localhost:11434/v1
"""

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model="openai/gpt-4o-mini",
        api_key="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",
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        streaming=False,
    )
