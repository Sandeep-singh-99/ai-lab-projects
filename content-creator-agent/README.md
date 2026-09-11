# 🚀 Content Creator Agent (LangChain + LangGraph Mini-Project)

An educational multi-agent content generation project built using **LangGraph**, **LangChain**, **Gemini LLMs** (`gemini-2.5-flash`), **Tavily Web Search**, and **Streamlit**.

This project demonstrates core agentic architecture patterns:
1. **Multi-Step Agent Collaboration**: Pipeline of specialized agents (Researcher ➔ Writer ➔ SEO Specialist ➔ Editor).
2. **State Management**: Centralized `AgentState` via TypedDict tracking topic, audience, intermediate outputs, quality rating, and logs.
3. **Tool Calling**: Researcher agent queries live web results using Tavily Search API.
4. **Structured Outputs**: SEO and Editor nodes utilize Pydantic schemas via `.with_structured_output()` for reliable JSON parsing.
5. **Iterative Feedback Loops**: Conditional edge routing (`should_continue`) from Editor back to Writer if revision is required (`NEEDS_REVISION`).
6. **Streamlit UI**: Full-featured interactive dashboard to trigger workflows, monitor real-time execution logs, view agent state, and export final markdown articles.

---

## 📐 Architecture & Workflow Diagram

```
                       ┌─────────────────────────┐
                       │       User Input        │
                       │ (Topic, Audience, Tone) │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │     Researcher Node     │ ◄── Tool Calling (Tavily Search)
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │   Content Writer Node   │ ◄── Initial Draft & Revisions
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │      SEO Agent Node     │ ◄── Structured Output (Keywords/Meta)
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │  Editor / Reviewer Node │ ◄── Structured Review & Decision
                       └────────────┬────────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                    [ APPROVED ]        [ NEEDS REVISION ]
                         │                     │
                         ▼                     └──────┐
                  ┌──────────────┐                    │ (Loop back with feedback)
                  │ Final Content│                    ▼
                  └──────────────┘           ┌─────────────────┐
                                             │ Content Writer  │
                                             └─────────────────┘
```

---

## 📂 Project Folder Structure

```
content-creator-agent/
├── app.py                      # Streamlit UI dashboard
├── requirements.txt            # Python dependencies
├── .env.example                # API key template
├── README.md                   # Complete architectural guide & documentation
└── src/
    ├── __init__.py
    ├── state.py                # LangGraph AgentState TypedDict definition
    ├── models.py               # Pydantic schemas for Structured Outputs
    ├── tools.py                # Tavily search tool wrapper & fallbacks
    ├── llm.py                  # Gemini LLM initializer (gemini-2.5-flash)
    ├── graph.py                # StateGraph compilation & conditional routing
    └── agents/
        ├── __init__.py
        ├── researcher.py       # Researcher node (Tavily search tool)
        ├── writer.py           # Content Writer node (Initial draft & revisions)
        ├── seo.py              # SEO Agent node (Pydantic structured output)
        └── editor.py           # Editor / Reviewer node (Quality evaluation & retry decision)
```

---

## ⚡ Key LangGraph Concepts Taught

### 1. Centralized State (`src/state.py`)
State is defined using `TypedDict`, making data shared across all nodes:
```python
class AgentState(TypedDict):
    topic: str
    audience: str
    tone: str
    platform: str
    research_data: str
    draft_content: str
    seo_data: Dict[str, Any]
    review_status: str       # "APPROVED" or "NEEDS_REVISION"
    review_feedback: str
    revision_count: int
    final_content: str
    logs: List[str]
```

### 2. Tool Calling (`src/agents/researcher.py`)
The Researcher queries Tavily web search to pull up-to-date data for the topic:
```python
search_results = search_web(f"{topic} tutorial best practices {audience}", api_key=tavily_api_key)
```

### 3. Structured Output (`src/agents/seo.py` & `src/agents/editor.py`)
Uses `.with_structured_output()` with Gemini to guarantee structured Pydantic objects:
```python
structured_llm = llm.with_structured_output(SEOOptimization)
seo_output: SEOOptimization = structured_llm.invoke(...)
```

### 4. Conditional Loops & Retry Workflows (`src/graph.py`)
The Editor node determines if the article needs revision. If status is `NEEDS_REVISION`, LangGraph loops back to `writer` with feedback attached:
```python
def should_continue(state: AgentState) -> Literal["writer", "__end__"]:
    if state.get("review_status") == "NEEDS_REVISION" and state.get("revision_count", 0) < state.get("max_revisions", 3):
        return "writer"
    return END
```

---

## 🛠️ Setup & Running

### 1. Environment Setup
Create a `.env` file in the `content-creator-agent` folder (or copy from `.env.example`):
```bash
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key # Optional for web search
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Web UI
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`. Enter your topic (e.g., *"How to learn FastAPI"*), target audience (*"Beginners"*), tone (*"Friendly"*), and platform (*"Blog"*), then click **Generate Content with Multi-Agent Workflow**.
