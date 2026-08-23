# 📚 PDF Chatbot

A powerful PDF chatbot built with **LangChain**, **LangGraph**, **ChromaDB**, and **Google Gemini**. Upload any PDF document and chat with it using natural language queries with streaming responses.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1.10-green.svg)

## ✨ Features

- 📄 **PDF Upload & Processing**: Upload PDF documents and automatically extract and index content
- 💬 **Interactive Chat Interface**: Ask questions about your PDF in natural language
- 🔄 **Streaming Responses**: Real-time streaming responses for better user experience
- 🧠 **RAG (Retrieval Augmented Generation)**: Accurate answers based on PDF content
- 📝 **Chat History**: Maintains conversation context for follow-up questions
- 🎨 **Beautiful UI**: Modern, gradient-styled interface with custom CSS
- 🗄️ **Vector Storage**: Persistent storage using ChromaDB for efficient retrieval

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Google Gemini 2.5 Flash
- **Framework**: LangChain, LangGraph
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **PDF Processing**: PyPDF

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Pdf_chatbbot
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```bash
   cp .env.example .env
   ```

   Add your Google API key to `.env`:

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🎯 Usage

1. **Start the application**

   ```bash
   streamlit run main.py
   ```

2. **Upload a PDF**

   - Click on "Choose a PDF file" in the sidebar
   - Select your PDF document
   - Click "🔄 Process PDF" to index the document

3. **Start chatting**
   - Once the PDF is processed, type your question in the chat input
   - The chatbot will provide answers based on the PDF content
   - Ask follow-up questions to dive deeper into the content

## 📁 Project Structure

```
Pdf_chatbbot/
├── chains/
│   ├── __init__.py
│   ├── embeddings.py      # HuggingFace embeddings configuration
│   ├── llm.py             # Google Gemini LLM setup
│   ├── pdf_loader.py      # PDF loading functionality
│   ├── rag_chain.py       # RAG chain implementation
│   ├── splitters.py       # Text splitting configuration
│   └── vectorStore.py     # ChromaDB vector store setup
├── graph/
│   ├── __init__.py
│   └── rag_graph.py       # LangGraph workflow
├── services/
│   ├── __init__.py
│   └── ingest_service.py  # PDF ingestion service
├── storage/
│   └── chroma_db/         # Vector database storage (auto-created)
├── utils/
│   └── __init__.py
├── main.py                # Streamlit application
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## 🔧 Configuration

### Embedding Model

The default embedding model is `sentence-transformers/all-MiniLM-L6-v2`. You can change this in `chains/embeddings.py`.

### LLM Model

The default LLM is `gemini-2.5-flash`. You can modify this in `chains/llm.py`.

### Chunk Size

Text splitting uses a chunk size of 1000 with 200 character overlap. Adjust these in `chains/splitters.py`.

## 🎨 Features in Detail

### PDF Processing

- Uploads are saved temporarily and processed immediately
- Documents are split into chunks for efficient retrieval
- Embeddings are generated and stored in ChromaDB
- Vector store persists across sessions

### Chat Interface

- Clean, modern UI with gradient styling
- Distinct styling for user and assistant messages
- Real-time message display
- Clear chat history option
- Status indicators in sidebar

### RAG Pipeline

1. User query is received
2. Relevant document chunks are retrieved from vector store
3. Context is passed to LLM along with chat history
4. LLM generates response based on context
5. Response is streamed back to user

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- UI created with [Streamlit](https://streamlit.io/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)

---

**Note**: Make sure to keep your API keys secure and never commit them to version control.
