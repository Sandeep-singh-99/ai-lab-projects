from typing import Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState
from src.llm import get_gemini_llm
from src.tools import search_web

def researcher_node(state: AgentState, gemini_api_key: Optional[str] = None, tavily_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Researcher Node: Uses tool calling / web search via Tavily to collect facts, code samples, and outline details.
    Uses Gemini LLM to synthesize research findings into a technical brief.
    """
    topic = state.get("topic", "")
    audience = state.get("audience", "Beginners")
    platform = state.get("platform", "Blog")
    logs = list(state.get("logs", []))
    
    logs.append(f"🔍 [Researcher] Searching web for topic: '{topic}' targeting '{audience}' on '{platform}'...")
    
    search_query = f"{topic} tutorial guide best practices {audience} {platform}"
    raw_search_results = search_web(search_query, api_key=tavily_api_key)
    
    llm = get_gemini_llm(api_key=gemini_api_key, temperature=0.3)
    
    system_prompt = (
        "You are an expert technical content researcher. Synthesize web search findings into a structured, "
        "comprehensive research brief for a content writer. Focus on key takeaways, step-by-step learning progression, "
        "code examples, and practical tips."
    )
    user_prompt = (
        f"Topic: {topic}\n"
        f"Target Audience: {audience}\n"
        f"Platform: {platform}\n\n"
        f"Raw Web Search Results:\n{raw_search_results}\n\n"
        "Provide a clear, detailed research outline and technical brief."
    )
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
    research_summary = str(response.content)
    
    logs.append("✅ [Researcher] Technical research brief created successfully.")
    
    return {
        "research_data": research_summary,
        "logs": logs
    }
