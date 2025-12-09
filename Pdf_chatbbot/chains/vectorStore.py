from langchain_chroma import Chroma
from chains.embeddings import get_embeddings


def get_vectorstore(persist_directory):
    return Chroma(
        persist_directory=persist_directory, embedding_function=get_embeddings()
    )
