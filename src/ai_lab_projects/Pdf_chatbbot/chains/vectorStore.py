from langchain_chroma import Chroma
from ai_lab_projects.Pdf_chatbbot.chains.embeddings import get_embeddings


def get_vectorstore(persist_directory):
    return Chroma(
        persist_directory=persist_directory, embedding_function=get_embeddings()
    )
