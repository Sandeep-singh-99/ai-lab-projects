from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from chains.llm import get_llm


def format_docs(docs):
    """Format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)


def get_rag_chain(vectorstore):
    """
    Create a RAG (Retrieval Augmented Generation) chain.

    Args:
        vectorstore: The vector store to use for retrieval

    Returns:
        chain: The RAG chain
    """
    llm = get_llm(streaming=True)

    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    )

    # Create prompt template
    system_prompt = """You are a helpful assistant that answers questions based on the provided context from PDF documents.
Use the following pieces of context to answer the question. If you don't know the answer based on the context, just say that you don't know.
Don't try to make up an answer. Keep your answers concise and relevant.

Context:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(system_prompt)

    # Create the chain using LCEL (LangChain Expression Language)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
