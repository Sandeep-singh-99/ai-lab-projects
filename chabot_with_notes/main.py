import os
from langchain_ollama import OllamaLLM  # Use Ollama local model
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Chroma
# from langchain.embeddings import OllamaEmbeddings
# from langchain.embeddings import LLMEmbeddings
from langchain_ollama import OllamaEmbeddings
# from langchain.chains import RetrievalQA



llm = OllamaLLM(model="llama3:8b", temperature=0)

st.set_page_config(page_title="Chatbot with Notes", page_icon="🤖")
st.title("🤖 Chatbot with Notes")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "store", "DSA CheatSheet.pdf")
persistent_dir = os.path.join(current_dir, "data", "chroma_db")


if not os.path.exists(persistent_dir):
    st.write("persistent directory does not exists. Please create it first.")

    if not os.path.exists(file_path):
        st.write("file does not exists. Please add the file first.")
    
    loader = PyMuPDFLoader(file_path=file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    st.write("----Document Chunks Information----")
    st.write(f"Total number of chunks: {len(docs)}")
    st.write(f"First chunk {docs[0].page_content}...")

    st.write("----Creating Embeddings and Vector Store----")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    st.write("Embeddings created.")

    st.write("Creating Chroma Vector Store...")
    vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persistent_dir)
    st.write("Chroma Vector Store created and persisted.")
else:
    st.write("Persistent directory exists. Loading existing Chroma Vector Store...")
    vectordb = Chroma(persist_directory=persistent_dir, embedding_function=OllamaEmbeddings(model="nomic-embed-text"))
    st.write("Chroma Vector Store loaded.")


text_input = st.text_input("You: ", placeholder="Ask me anything about DSA CheatSheet PDF")
if text_input:
    st.write(f"You: {text_input}")

    docs = vectordb.similarity_search(text_input, k=2)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a helpful AI assistant. Use the following context to answer the question.
{context}

Question: {text_input}
Answer:"""

    response = llm.invoke(prompt)
    st.write(f"AI: {response}")