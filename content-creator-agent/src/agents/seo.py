from typing import Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState
from src.models import SEOOptimization
from src.llm import get_gemini_llm

def seo_node(state: AgentState, gemini_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    SEO Agent Node: Leverages Structured Output (Pydantic schema) with Gemini LLM to evaluate draft and return
    target keywords, meta title, meta description, heading structure, and readability enhancements.
    """
    topic = state.get("topic", "")
    audience = state.get("audience", "")
    platform = state.get("platform", "")
    draft_content = state.get("draft_content", "")
    logs = list(state.get("logs", []))
    
    logs.append("📈 [SEO Agent] Analyzing content draft and extracting structured SEO metadata...")
    
    llm = get_gemini_llm(api_key=gemini_api_key, temperature=0.3)
    
    system_prompt = (
        "You are an expert SEO Specialist. Analyze the provided draft article and generate structured "
        "SEO metadata including meta title, meta description, target keywords, heading suggestions, and readability improvements."
    )
    user_prompt = (
        f"Topic: {topic}\n"
        f"Target Audience: {audience}\n"
        f"Platform: {platform}\n\n"
        f"Draft Article (Snippet):\n{draft_content[:3500]}\n"
    )
    
    try:
        structured_llm = llm.with_structured_output(SEOOptimization)
        seo_res: SEOOptimization = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        seo_dict = seo_res.model_dump()
    except Exception as e:
        seo_dict = {
            "meta_title": f"{topic}: The Complete Guide for {audience}",
            "meta_description": f"Master {topic} step-by-step with this beginner-friendly guide covering setup, features, and best practices.",
            "target_keywords": [topic.lower(), f"learn {topic.lower()}", f"{topic.lower()} tutorial", f"{topic.lower()} guide"],
            "heading_suggestions": ["H1: Main Title", "H2: Getting Started", "H2: Key Concepts", "H2: Summary"],
            "content_improvements": [f"SEO extraction completed (fallback mode: {str(e)})"]
        }
    
    logs.append(f"✅ [SEO Agent] Keywords: {', '.join(seo_dict.get('target_keywords', [])[:4])} | Meta Title: '{seo_dict.get('meta_title')}'")
    
    return {
        "seo_data": seo_dict,
        "logs": logs
    }
