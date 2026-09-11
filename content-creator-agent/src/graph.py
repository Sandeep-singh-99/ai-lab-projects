from typing import Literal, Optional, Dict, Any
from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.agents.researcher import researcher_node
from src.agents.writer import writer_node
from src.agents.seo import seo_node
from src.agents.editor import editor_node

def should_continue(state: AgentState) -> Literal["writer", "__end__"]:
    """
    Conditional routing function for the Editor node:
    - Returns 'writer' if content review status is 'NEEDS_REVISION' and revision count < max_revisions
    - Returns END if content review status is 'APPROVED' or revision limit is exceeded
    """
    status = state.get("review_status", "APPROVED")
    revision_count = state.get("revision_count", 0)
    max_revisions = state.get("max_revisions", 3)
    
    if status == "NEEDS_REVISION" and revision_count < max_revisions:
        return "writer"
    return END

def build_content_creator_graph(gemini_api_key: Optional[str] = None, tavily_api_key: Optional[str] = None):
    """
    Builds and compiles the StateGraph workflow for multi-agent content creation using Gemini LLM.
    Flow: START -> Researcher -> Content Writer -> SEO Agent -> Editor/Reviewer -> [Conditional: Writer / END]
    """
    builder = StateGraph(AgentState)
    
    # Node functions with API key injection
    def _researcher(state: AgentState) -> Dict[str, Any]:
        return researcher_node(state, gemini_api_key=gemini_api_key, tavily_api_key=tavily_api_key)
    
    def _writer(state: AgentState) -> Dict[str, Any]:
        return writer_node(state, gemini_api_key=gemini_api_key)
    
    def _seo(state: AgentState) -> Dict[str, Any]:
        return seo_node(state, gemini_api_key=gemini_api_key)
    
    def _editor(state: AgentState) -> Dict[str, Any]:
        return editor_node(state, gemini_api_key=gemini_api_key)
    
    # Register Nodes
    builder.add_node("researcher", _researcher)
    builder.add_node("writer", _writer)
    builder.add_node("seo", _seo)
    builder.add_node("editor", _editor)
    
    # Connect Sequential Edges
    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "seo")
    builder.add_edge("seo", "editor")
    
    # Connect Conditional Loop Edge from Editor
    builder.add_conditional_edges("editor", should_continue, {
        "writer": "writer",
        END: END
    })
    
    return builder.compile()
