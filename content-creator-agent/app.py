import os
import sys
import json
import streamlit as st
from dotenv import load_dotenv

# Ensure root package import capability
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

load_dotenv()

from src.graph import build_content_creator_graph

st.set_page_config(
    page_title="Content Creator Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 Multi-Agent Content Creator Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powered by LangGraph, LangChain, Gemini 2.5 Flash & Tavily Web Search</div>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    gemini_api_key_input = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", ""),
        type="password",
        help="Enter your Gemini API Key (or set GEMINI_API_KEY in .env file)."
    )
    
    tavily_api_key_input = st.text_input(
        "Tavily API Key (Optional)",
        value=os.getenv("TAVILY_API_KEY", ""),
        type="password",
        help="Optional: Enables real-time Tavily search for Researcher agent."
    )
    
    selected_model = st.selectbox(
        "Gemini LLM Model",
        options=["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"],
        index=0
    )
    
    max_revisions = st.slider(
        "Max Editor Revisions",
        min_value=1,
        max_value=5,
        value=3,
        help="Maximum loop iterations between Editor and Writer before finalizing."
    )
    
    st.divider()
    
    with st.expander("📌 Workflow Diagram", expanded=True):
        st.code("""
User Input
    ↓
Researcher (Tavily Search)
    ↓
Content Writer
    ↓
SEO Agent (Structured Output)
    ↓
Editor / Reviewer
    ↓
 ┌──┴──┐
 │     │
Good  Needs Revision
 │     │
 ↓     └──► Writer (Retry Loop)
Final Article
        """, language="text")

# Main Input Section
col1, col2 = st.columns([1, 1])

with col1:
    topic = st.text_input("Topic", value="How to learn FastAPI", help="Topic or title idea")
    audience = st.selectbox("Target Audience", options=["Beginners", "Intermediate Developers", "Tech Leads", "General Public"])

with col2:
    tone = st.selectbox("Tone & Voice", options=["Friendly", "Professional", "Technical & In-depth", "Conversational", "Educational"])
    platform = st.selectbox("Platform", options=["Blog", "LinkedIn Article", "Newsletter", "Documentation Guide"])

st.divider()

if st.button("🚀 Generate Content with Multi-Agent Workflow", type="primary", use_container_width=True):
    if not gemini_api_key_input:
        st.error("⚠️ Please provide a Gemini API Key in the sidebar to run the workflow.")
    else:
        # Initialize initial graph state
        initial_state = {
            "topic": topic,
            "audience": audience,
            "tone": tone,
            "platform": platform,
            "research_data": "",
            "draft_content": "",
            "seo_data": {},
            "review_status": "",
            "review_feedback": "",
            "rating": 0,
            "revision_count": 0,
            "max_revisions": max_revisions,
            "logs": [f"🚀 Workflow initiated for topic: '{topic}' using model {selected_model}"],
            "final_content": ""
        }
        
        progress_bar = st.progress(0, text="Initializing LangGraph Agents...")
        status_box = st.empty()
        
        try:
            # Build and execute graph
            graph = build_content_creator_graph(
                gemini_api_key=gemini_api_key_input,
                tavily_api_key=tavily_api_key_input
            )
            
            os.environ["GEMINI_MODEL"] = selected_model
            
            progress_bar.progress(25, text="Running Researcher Agent (Tavily Search)...")
            final_state = graph.invoke(initial_state)
            progress_bar.progress(100, text="Workflow Completed Successfully!")
            
            st.session_state["final_state"] = final_state
            st.success("🎉 Multi-agent workflow execution completed!")
            
        except Exception as e:
            st.error(f"❌ Error during workflow execution: {str(e)}")

# Display Results if state exists
if "final_state" in st.session_state:
    state = st.session_state["final_state"]
    
    st.subheader("📊 Output Dashboard")
    
    tab_final, tab_research, tab_draft, tab_seo, tab_editor, tab_logs = st.tabs([
        "📄 Final Article",
        "🔍 Research Brief",
        "✍️ Writer Draft",
        "📈 SEO Metadata",
        "📋 Editor Review",
        "🛠️ Execution Logs"
    ])
    
    with tab_final:
        st.markdown(state.get("final_content", "No content generated."))
        st.divider()
        st.download_button(
            label="📥 Download Markdown Article",
            data=state.get("final_content", ""),
            file_name=f"{topic.lower().replace(' ', '_')}_article.md",
            mime="text/markdown"
        )
        
    with tab_research:
        st.markdown("### Technical Research Brief (Researcher Node)")
        st.markdown(state.get("research_data", "No research notes."))
        
    with tab_draft:
        st.markdown("### Written Draft (Content Writer Node)")
        st.markdown(state.get("draft_content", "No draft generated."))
        
    with tab_seo:
        st.markdown("### Structured SEO Optimization (SEO Node)")
        seo_data = state.get("seo_data", {})
        st.write(f"**Meta Title:** {seo_data.get('meta_title', 'N/A')}")
        st.write(f"**Meta Description:** {seo_data.get('meta_description', 'N/A')}")
        
        keywords = seo_data.get("target_keywords", [])
        if keywords:
            st.write("**Target Keywords:** " + ", ".join([f"`{k}`" for k in keywords]))
            
        headings = seo_data.get("heading_suggestions", [])
        if headings:
            st.markdown("**Heading Structure Suggestions:**")
            for h in headings:
                st.markdown(f"- {h}")
                
    with tab_editor:
        st.markdown("### Editor Quality Review (Editor Node)")
        status = state.get("review_status", "APPROVED")
        rating = state.get("rating", 0)
        revisions = state.get("revision_count", 0)
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Review Decision", status)
        with m_col2:
            st.metric("Quality Rating", f"{rating} / 10")
        with m_col3:
            st.metric("Revision Loops Run", revisions)
            
        feedback = state.get("review_feedback", "")
        if feedback:
            st.markdown("**Editor Feedback:**")
            st.info(feedback)
            
    with tab_logs:
        st.markdown("### Step-by-Step Graph Execution Logs")
        logs = state.get("logs", [])
        for log in logs:
            st.text(log)
        
        st.divider()
        with st.expander("🔍 Complete State Inspection (JSON)", expanded=False):
            st.json(state)
