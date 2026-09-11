from typing import List, Dict, Any, TypedDict

class AgentState(TypedDict):
    """
    State definition for the content creator agent graph.
    Maintains user parameters, intermediate agent outputs, review status, and execution logs.
    """
    topic: str
    audience: str
    tone: str
    platform: str
    
    # Intermediate Node Outputs
    research_data: str
    draft_content: str
    seo_data: Dict[str, Any]
    
    # Reviewer State & Retry Loop Control
    review_status: str       # "APPROVED" or "NEEDS_REVISION"
    review_feedback: str     # Actionable guidance from Editor to Writer
    rating: int              # Content quality score (1-10)
    revision_count: int      # Counter for revision loops
    max_revisions: int       # Maximum allowed revisions before forcing approval
    
    # Outputs & Execution Logs
    final_content: str
    logs: List[str]
