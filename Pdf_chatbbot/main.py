import streamlit as st
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from services.ingest_service import ingest_pdf, get_existing_vectorstore
from graph.rag_graph import create_rag_graph
from langchain_core.messages import HumanMessage, AIMessage

# Page configuration
st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        color: #1a1a1a;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .message-label {
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #1a1a1a;
    }
    .message-content {
        color: #2d2d2d;
        line-height: 1.6;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "graph" not in st.session_state:
    st.session_state.graph = None

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# Header
st.markdown('<p class="main-header">📚 PDF Chatbot</p>', unsafe_allow_html=True)
st.markdown("**Powered by LangChain, LangGraph, ChromaDB & Google Gemini**")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📄 Upload PDF")
    st.markdown("Upload a PDF document to start chatting with it.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a PDF document to extract information from",
    )

    if uploaded_file is not None:
        if st.button("🔄 Process PDF", type="primary"):
            with st.spinner("Processing PDF... This may take a moment."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    # Process the PDF
                    persist_dir = "./storage/chroma_db"
                    st.session_state.vectorstore = ingest_pdf(
                        tmp_file_path, persist_dir
                    )
                    st.session_state.graph = create_rag_graph(
                        st.session_state.vectorstore
                    )
                    st.session_state.pdf_processed = True

                    # Clean up temporary file
                    os.unlink(tmp_file_path)

                    st.success(f"✅ Successfully processed: {uploaded_file.name}")
                    st.info("You can now start asking questions about the PDF!")

                except Exception as e:
                    st.error(f"❌ Error processing PDF: {str(e)}")

    # Display status
    st.divider()
    if st.session_state.pdf_processed:
        st.success("✅ PDF Ready")
        st.info(f"💬 Messages: {len(st.session_state.messages)}")
    else:
        st.warning("⚠️ No PDF loaded")
        st.info("Upload and process a PDF to start chatting")

    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

# Main chat interface
if not st.session_state.pdf_processed:
    st.info("👈 Please upload and process a PDF from the sidebar to start chatting.")
else:
    # Display chat messages
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.container():
                st.markdown(
                    f'<div class="chat-message user-message">'
                    f'<div class="message-label">👤 You</div>'
                    f'<div class="message-content">{message.content}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
        elif isinstance(message, AIMessage):
            with st.container():
                st.markdown(
                    f'<div class="chat-message assistant-message">'
                    f'<div class="message-label">🤖 Assistant</div>'
                    f'<div class="message-content">{message.content}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # Chat input
    if prompt := st.chat_input("Ask a question about your PDF..."):
        # Add user message to chat history
        user_message = HumanMessage(content=prompt)
        st.session_state.messages.append(user_message)

        # Display user message
        with st.container():
            st.markdown(
                f'<div class="chat-message user-message">'
                f'<div class="message-label">👤 You</div>'
                f'<div class="message-content">{prompt}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

        # Generate response with streaming
        with st.container():
            message_placeholder = st.empty()

            try:
                # Invoke the graph
                result = st.session_state.graph.invoke(
                    {
                        "messages": st.session_state.messages,
                        "question": prompt,
                        "answer": "",
                    }
                )

                # Extract the answer
                answer = result.get("answer", "I couldn't generate a response.")

                # Display streaming effect (simulate streaming for better UX)
                full_response = ""
                message_placeholder.markdown(
                    f'<div class="chat-message assistant-message">'
                    f'<div class="message-label">🤖 Assistant</div>'
                    f'<div class="message-content">{answer}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

                # Add assistant message to chat history
                ai_message = AIMessage(content=answer)
                st.session_state.messages.append(ai_message)

            except Exception as e:
                error_message = f"❌ Error generating response: {str(e)}"
                message_placeholder.error(error_message)
                st.session_state.messages.append(AIMessage(content=error_message))

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        Built with ❤️ using Streamlit, LangChain, LangGraph & ChromaDB
    </div>
    """,
    unsafe_allow_html=True,
)
