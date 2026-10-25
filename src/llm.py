import os

from .config import LLM_PROVIDER, LLM_MODEL


def get_llm():
    if LLM_PROVIDER == "openrouter":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=LLM_MODEL,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )
    if LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0)
    if LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model=LLM_MODEL, temperature=0)
    raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")