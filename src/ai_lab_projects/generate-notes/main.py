import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAI

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Google API key not found! Please check your .env file.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="📝 AI Notes Generator", layout="wide")
st.title("🧠 AI Notes Generator")

# --- Initialize Gemini LLM ---
# Try switching to gemini-1.5-flash if 2.5 isn't available to your key
try:
    llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
except Exception as e:
    st.error(f"⚠️ Failed to initialize Gemini: {e}")
    st.stop()

# --- User Input ---
topic = st.text_input("Enter key points or topic for notes generation:")

# --- Generate Notes Button ---
if st.button("✨ Generate Notes", use_container_width=True, type="primary"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic or key points.")
    else:
        # --- Prompt Template ---
        prompt = f"""
        Generate detailed, well-structured notes based on the following topic:

        **Topic:** {topic}

        Requirements:
        - Use clear markdown formatting (headings, bullet points, bold, etc.).
        - Include examples where applicable.
        - Add image references if necessary (use markdown image syntax `![alt](url)`).
        - Keep explanations educational and concise.
        """

        # --- Loading Spinner ---
        with st.spinner("🧩 Generating your notes... please wait..."):
            try:
                response = llm.invoke(prompt)

                # --- Handle Different Response Types ---
                if not response:
                    st.error("❌ No response received from Gemini.")
                    st.stop()

                if hasattr(response, "content"):
                    raw_output = response.content.strip()
                elif isinstance(response, str):
                    raw_output = response.strip()
                else:
                    st.error("⚠️ Unexpected response format.")
                    st.stop()

                # --- Display Notes ---
                if raw_output:
                    st.success("✅ Notes generated successfully!")
                    st.markdown("### 📝 Generated Notes:")
                    st.markdown(raw_output, unsafe_allow_html=True)

                    # Optional: Download button
                    st.download_button(
                        label="💾 Download Notes (Markdown)",
                        data=raw_output,
                        file_name=f"{topic}_notes.md",
                        mime="text/markdown",
                    )
                else:
                    st.error("❌ Empty output received. Please try again.")

            except Exception as e:
                st.error(f"⚠️ Error while generating notes: {e}")
