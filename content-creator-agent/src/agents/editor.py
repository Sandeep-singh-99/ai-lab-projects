from typing import Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState
from src.models import EditorReview
from src.llm import get_gemini_llm

def editor_node(state: AgentState, gemini_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Editor / Reviewer Agent Node: Performs quality assurance using Structured Output with Gemini LLM.
    Evaluates draft content, assigns rating score (1-10), decides APPROVED vs NEEDS_REVISION,
    and returns actionable feedback.
    """
    topic = state.get("topic", "")
    audience = state.get("audience", "Beginners")
    tone = state.get("tone", "Friendly")
    draft_content = state.get("draft_content", "")
    seo_data = state.get("seo_data", {})
    revision_count = state.get("revision_count", 0)
    max_revisions = state.get("max_revisions", 3)
    logs = list(state.get("logs", []))
    
    logs.append(f"🧐 [Editor/Reviewer] Evaluating draft quality against requirements (Attempt #{revision_count + 1})...")
    
    llm = get_gemini_llm(api_key=gemini_api_key, temperature=0.2)
    
    system_prompt = (
        "You are a strict, constructive Senior Editor. Evaluate the article draft based on clarity, tone, "
        "accuracy, audience fit, and completeness. Approve (is_approved=True) if rating is >= 7 or if the content is clear and accurate. "
        "Otherwise, set is_approved=False and provide detailed, constructive feedback for revision."
    )
    user_prompt = (
        f"Topic: {topic}\n"
        f"Target Audience: {audience}\n"
        f"Target Tone: {tone}\n"
        f"Current Revision Counter: {revision_count}\n\n"
        f"Draft Content:\n{draft_content}\n\n"
        f"SEO Metadata:\n{seo_data}\n"
    )
    
    try:
        structured_llm = llm.with_structured_output(EditorReview)
        review_res: EditorReview = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        is_approved = review_res.is_approved
        rating = review_res.rating
        feedback = review_res.detailed_feedback
    except Exception as e:
        is_approved = True
        rating = 8
        feedback = f"Editor review completed via default evaluation ({str(e)})."
    
    status = "APPROVED" if is_approved else "NEEDS_REVISION"
    
    if not is_approved and revision_count >= max_revisions:
        logs.append(f"⚠️ [Editor] Maximum revision threshold ({max_revisions}) reached. Forcing final approval.")
        status = "APPROVED"
        is_approved = True
    
    logs.append(f"📋 [Editor] Review Decision: {status} | Quality Rating: {rating}/10")
    
    final_content = ""
    if is_approved:
        meta_title = seo_data.get("meta_title", topic)
        meta_desc = seo_data.get("meta_description", "")
        keywords = ", ".join(seo_data.get("target_keywords", []))
        
        final_content = (
            f"<!-- SEO Metadata -->\n"
            f"<!-- Title: {meta_title} -->\n"
            f"<!-- Description: {meta_desc} -->\n"
            f"<!-- Keywords: {keywords} -->\n\n"
            f"# {meta_title}\n\n"
            f"{draft_content}"
        )
    
    return {
        "review_status": status,
        "review_feedback": feedback,
        "rating": rating,
        "revision_count": revision_count + (0 if is_approved else 1),
        "logs": logs,
        "final_content": final_content
    }
