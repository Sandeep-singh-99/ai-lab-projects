import os
from typing import Optional
from langchain_tavily import TavilySearch

def get_tavily_search_tool(api_key: Optional[str] = None) -> Optional[TavilySearch]:
    """
    Instantiates TavilySearch tool using the provided API key or environment variable.
    """
    key = api_key or os.getenv("TAVILY_API_KEY")
    if not key or key.strip() == "":
        return None
    try:
        return TavilySearch(tavily_api_key=key, max_results=4)
    except Exception:
        return None

def search_web(query: str, api_key: Optional[str] = None) -> str:
    """
    Performs web research using Tavily Search API. Fallbacks gracefully if key is missing or fails.
    """
    tool = get_tavily_search_tool(api_key)
    if tool:
        try:
            results = tool.invoke({"query": query})
            items = results.get("results", []) if isinstance(results, dict) else (results if isinstance(results, list) else [])
            if items:
                formatted = []
                for idx, item in enumerate(items, 1):
                    title = item.get("title", f"Result {idx}")
                    content = item.get("content", "")
                    url = item.get("url", "")
                    formatted.append(f"[{idx}] {title}\nURL: {url}\nSummary: {content}")
                return "\n\n".join(formatted)
            return str(results)
        except Exception as e:
            return f"Note: Tavily Search API returned error ({str(e)}). Using domain knowledge for topic '{query}'."
    
    return (
        f"Fallback Web Search Data for '{query}':\n"
        "- Core Concepts: Prerequisites, Installation & Setup, Core Features, Interactive API Docs (Swagger/ReDoc), Code Examples.\n"
        "- Best Practices: Project structure, Async performance, Pydantic validation, Dependency Injection.\n"
        "- Common Pitfalls: Synchronous blocking functions, improper CORS setup, missing type annotations."
    )
