from typing import Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState
from src.llm import get_gemini_llm

def writer_node(state: AgentState, gemini_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Content Writer Node: Crafts initial draft or revises content based on research notes and Editor review feedback.
    Uses Gemini LLM to generate clear, high-quality Markdown content.
    """
    topic = state.get("topic", "")
    audience = state.get("audience", "Beginners")
    tone = state.get("tone", "Friendly")
    platform = state.get("platform", "Blog")
    research_data = state.get("research_data", "")
    review_feedback = state.get("review_feedback", "")
    revision_count = state.get("revision_count", 0)
    logs = list(state.get("logs", []))
    
    if revision_count > 0 and review_feedback:
        logs.append(f"✍️ [Content Writer] Revising draft (Revision #{revision_count}) incorporating Editor feedback...")
    else:
        logs.append(f"✍️ [Content Writer] Generating initial article draft for '{topic}'...")
    
    llm = get_gemini_llm(api_key=gemini_api_key, temperature=0.7)
    
    system_prompt = (
        f"You are a skilled Content Writer specializing in {platform} content. "
        f"Write engaging, well-structured, clear content tailored specifically for {audience}. "
        f"Maintain a {tone} tone. Use clean Markdown formatting with clear section headers, bullet points, and code blocks."
    )
    
    user_prompt = (
        f"Topic: {topic}\n"
        f"Target Audience: {audience}\n"
        f"Tone: {tone}\n"
        f"Platform: {platform}\n\n"
        f"Research Brief:\n{research_data}\n"
    )
    
    if revision_count > 0 and review_feedback:
        user_prompt += (
            f"\nCRITICAL - Editor Feedback to Address:\n"
            f"{review_feedback}\n\n"
            "Please revise the complete article draft to address every issue raised by the Editor."
        )
    else:
        user_prompt += "\nWrite the complete article draft with an introduction, key concepts, practical code/examples, best practices, and conclusion."
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
    draft_content = str(response.content)
    
    logs.append(f"✅ [Content Writer] Draft generated/updated ({len(draft_content)} characters).")
    
    return {
        "draft_content": draft_content,
        "logs": logs
    }
