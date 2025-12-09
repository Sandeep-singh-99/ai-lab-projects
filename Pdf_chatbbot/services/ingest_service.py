from chains.vectorStore import get_vectorstore
from chains.pdf_loader import load_pdf
from chains.splitters import get_splitter
import os


def ingest_pdf(file_path: str, persist_directory: str = "./storage/chroma_db"):
    """
    Ingest a PDF file into the vector store.

    Args:
        file_path: Path to the PDF file
        persist_directory: Directory to persist the vector store

    Returns:
        vectorstore: The created vector store
    """
    # Load PDF documents
    documents = load_pdf(file_path)

    # Split documents into chunks
    splitter = get_splitter()
    chunks = splitter.split_documents(documents)

    # Create vector store
    vectorstore = get_vectorstore(persist_directory)
    vectorstore.add_documents(chunks)

    return vectorstore


def get_existing_vectorstore(persist_directory: str = "./storage/chroma_db"):
    """
    Get an existing vector store.

    Args:
        persist_directory: Directory where the vector store is persisted

    Returns:
        vectorstore: The existing vector store or None if it doesn't exist
    """
    if os.path.exists(persist_directory):
        return get_vectorstore(persist_directory)
    return None
