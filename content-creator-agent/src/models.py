from typing import List
from pydantic import BaseModel, Field

class SEOOptimization(BaseModel):
    """Structured output schema for the SEO Agent node."""
    meta_title: str = Field(
        description="Catchy, SEO-optimized title within 60 characters"
    )
    meta_description: str = Field(
        description="Compelling meta description within 160 characters designed for search engine snippets"
    )
    target_keywords: List[str] = Field(
        description="Primary and secondary target keywords for search ranking"
    )
    heading_suggestions: List[str] = Field(
        description="Suggested H1, H2, and H3 headers to structure and optimize content"
    )
    content_improvements: List[str] = Field(
        description="Actionable tips and readability improvements incorporated into the article"
    )


class EditorReview(BaseModel):
    """Structured output schema for the Editor / Reviewer agent node."""
    is_approved: bool = Field(
        description="Set to True if content is ready for publication, False if revisions are required"
    )
    rating: int = Field(
        description="Overall content quality rating score from 1 to 10"
    )
    key_strengths: List[str] = Field(
        description="Key strengths and highlights of the current draft"
    )
    critical_issues: List[str] = Field(
        description="Specific gaps, inaccuracies, or issues that need fixing if not approved"
    )
    detailed_feedback: str = Field(
        description="Constructive, step-by-step feedback for the Content Writer if revision is required"
    )
