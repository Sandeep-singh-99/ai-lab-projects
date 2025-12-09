from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from chains.rag_chain import get_rag_chain


class GraphState(TypedDict):
    """
    State for the RAG graph.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    question: str
    answer: str


def create_rag_graph(vectorstore):
    """
    Create a LangGraph workflow for RAG.

    Args:
        vectorstore: The vector store to use for retrieval

    Returns:
        graph: Compiled LangGraph workflow
    """
    rag_chain = get_rag_chain(vectorstore)

    def retrieve_and_generate(state: GraphState):
        """
        Retrieve relevant documents and generate an answer.
        """
        question = state["question"]

        # Invoke the RAG chain
        try:
            answer = rag_chain.invoke(question)
        except Exception as e:
            answer = f"Error generating response: {str(e)}"

        # Add AI message to messages
        ai_message = AIMessage(content=answer)

        return {"messages": [ai_message], "question": question, "answer": answer}

    # Create the graph
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("retrieve_and_generate", retrieve_and_generate)

    # Set entry point
    workflow.set_entry_point("retrieve_and_generate")

    # Add edge to END
    workflow.add_edge("retrieve_and_generate", END)

    # Compile the graph
    graph = workflow.compile()

    return graph
