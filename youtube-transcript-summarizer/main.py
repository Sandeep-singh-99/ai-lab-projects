import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import os

# Load .env variables
load_dotenv()

# Initialize model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# --- Helper functions ---

def extract_video_id(url: str):
    """Extract YouTube video ID from URL"""
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None

def get_youtube_transcript(video_id):
    """Fetch transcript text from YouTube"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def summarize_text(text: str):
    """Summarize text using Gemini through LangChain"""
    summarize_prompt = PromptTemplate.from_template(
        "Summarize the following YouTube transcript into concise bullet points:\n\n{text}"
    )
    summarize_chain = RunnableSequence(summarize_prompt | llm)
    summary = summarize_chain.invoke({"text": text})
    return summary.content.strip()

# --- Streamlit UI ---

st.set_page_config(page_title="🎬 YouTube Transcript Summarizer", layout="centered")

st.title("🎬 YouTube Transcript Summarizer")
st.write("Paste a YouTube video link to fetch and summarize its transcript using Gemini.")

youtube_url = st.text_input("Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=example")

if st.button("Summarize"):
    if not youtube_url:
        st.warning("Please enter a valid YouTube URL.")
    else:
        with st.spinner("Fetching and summarizing transcript..."):
            video_id = extract_video_id(youtube_url)
            if not video_id:
                st.error("Invalid YouTube URL format.")
            else:
                text = get_youtube_transcript(video_id)
                if text:
                    summary = summarize_text(text)
                    st.success("✅ Summary generated successfully!")
                    st.subheader("📘 Summary:")
                    st.write(summary)
