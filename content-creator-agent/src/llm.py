import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI

DEFAULT_MODEL = "gemini-2.5-flash"

def get_gemini_llm(
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.7
) -> ChatGoogleGenerativeAI:
    """
    Utility helper to instantiate ChatGoogleGenerativeAI LLM with Gemini models.
    Checks GEMINI_API_KEY or GOOGLE_API_KEY environment variables.
    """
    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key or key.strip() == "":
        raise ValueError(
            "Gemini API Key is required. Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable or enter it in the sidebar."
        )
    
    selected_model = model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    return ChatGoogleGenerativeAI(
        model=selected_model,
        google_api_key=key,
        temperature=temperature
    )
