# import os 
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# import streamlit as st
# from langchain_community.vectorstores import Chroma
# from langgraph.graph import StateGraph, START, END
# from langgraph.checkpoint.memory import InMemorySaver
# from langchain_core.messages import AIMessage, HumanMessage
# from langgraph.graph.message import add_messages
# from typing_extensions import TypedDict
# from typing import Annotated
# import uuid
# from langchain_community.embeddings import HuggingFaceEmbeddings

# load_dotenv()

# memory = InMemorySaver()


# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# class State(TypedDict):
#     email_topic: Annotated[list, add_messages]
#     email_category: Annotated[list, add_messages]
#     result: Annotated[list, add_messages]


# def create_email_graph(state: State):
#     input_topic = state["email_topic"][-1].content
#     input_category = state["email_category"][-1].content

#     Prompt = (
#         f"Draft a {input_category} email based on the following topic or key points:\n\n"
#         f"{input_topic}\n\n"
#         "Make sure the email is well-structured and professional."
#     )

#     response = llm.invoke(Prompt)

#     if not response or not response.content:
#         st.error("Failed to generate email draft. Please try again.")
    
#     raw_output = response.content.strip()

#     return {
#         "email_topic": state["email_topic"],
#         "email_category": state["email_category"],
#         "result": [AIMessage(content=raw_output)],
#     }

# workflow = StateGraph(State)
# workflow.add_node("create_email_graph", create_email_graph)
# workflow.add_edge(START, "create_email_graph")
# workflow.add_edge("create_email_graph", END)

# graph = workflow.compile(checkpointer=memory)

# # embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# st.set_page_config(page_title="Email Draft Generator", page_icon="✉️")
# st.title("✉️ Email Draft Generator")

# current_dir = os.path.dirname(os.path.abspath(__file__))
# data_dir = os.path.join(current_dir, "data")
# persistent_directory = os.path.join(data_dir, "chroma_db")

# # Ensure data folder exists
# os.makedirs(persistent_directory, exist_ok=True)

# if not os.path.exists(persistent_directory):
#     st.error("Persistent directory not found. Please ensure the Chroma database is set up correctly.")
# else:
#     vectorstore = Chroma(
#         persist_directory=persistent_directory,
#         embedding_function=embedding_model
#     )
#     # st.success("Chroma vector store loaded successfully.")

#     st.header("Generate Email Draft")
#     user_input = st.text_area("Enter the email topic or key points:", height=150)

#     category = st.selectbox("Select Email Category:", 
#                             ["Business", "Personal", "Marketing", "Follow-up", "Thank You", "Invitation"])

#     if st.button("Generate Draft"):
#         if user_input.strip() == "":
#             st.warning("Please enter some content to generate an email draft.")
#         else:
#             with st.spinner("Generating email draft..."):
#                 inputs = {
#                     "email_topic": [HumanMessage(content=user_input)],
#                     "email_category": [HumanMessage(content=category)]
#                 }

#                 thread_id = f"thread_{uuid.uuid4()}"

#                 output_state = graph.invoke(inputs, config={"configurable": {"thread_id": thread_id}})

#                 st.subheader("Generated Email Draft:")
#                 st.text_area("Email Draft:", value=output_state["result"][-1].content, height=300)

#                 vectorstore.add_texts([output_state["result"][-1].content], metadatas=[{"category": category, "topic": user_input}])
#                 st.success("Email draft generated and saved to vector store.")

    
# st.divider()
# st.subheader("🔍 Recall Previous Emails")
# search_query = st.text_input("Enter topic or phrase to find similar past emails:")
# if st.button("Search Memory"):
#     results = vectorstore.similarity_search(search_query, k=3)
#     if results:
#         for i, doc in enumerate(results, start=1):
#             st.markdown(f"**Result {i}:**\n\n{doc.page_content}\n---")
#     else:
#         st.info("No similar emails found in memory.")







import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
import uuid

load_dotenv()

# Memory for LangGraph workflow
memory = InMemorySaver()

# Gemini LLM for email drafting
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# State definition
class State(TypedDict):
    email_topic: Annotated[list, add_messages]
    email_category: Annotated[list, add_messages]
    result: Annotated[list, add_messages]

# Email generation logic
def create_email_graph(state: State):
    input_topic = state["email_topic"][-1].content
    input_category = state["email_category"][-1].content

    prompt = (
        f"Draft a {input_category} email based on the following topic or key points:\n\n"
        f"{input_topic}\n\n"
        "Make sure the email is well-structured and professional."
    )

    response = llm.invoke(prompt)

    if not response or not response.content:
        st.error("Failed to generate email draft. Please try again.")
        return state  # fallback

    raw_output = response.content.strip()

    return {
        "email_topic": state["email_topic"],
        "email_category": state["email_category"],
        "result": [AIMessage(content=raw_output)],
    }

# Workflow setup
workflow = StateGraph(State)
workflow.add_node("create_email_graph", create_email_graph)
workflow.add_edge(START, "create_email_graph")
workflow.add_edge("create_email_graph", END)

graph = workflow.compile(checkpointer=memory)

# Streamlit UI
st.set_page_config(page_title="Email Draft Generator", page_icon="✉️")
st.title("✉️ Email Draft Generator")

st.header("Generate Email Draft")
user_input = st.text_area("Enter the email topic or key points:", height=150)

category = st.selectbox("Select Email Category:", 
                        ["Business", "Personal", "Marketing", "Follow-up", "Thank You", "Invitation"])

if st.button("Generate Draft"):
    if user_input.strip() == "":
        st.warning("Please enter some content to generate an email draft.")
    else:
        with st.spinner("Generating email draft..."):
            inputs = {
                "email_topic": [HumanMessage(content=user_input)],
                "email_category": [HumanMessage(content=category)]
            }

            thread_id = f"thread_{uuid.uuid4()}"
            output_state = graph.invoke(inputs, config={"configurable": {"thread_id": thread_id}})

            st.subheader("Generated Email Draft:")
            st.text_area("Email Draft:", value=output_state["result"][-1].content, height=300)
