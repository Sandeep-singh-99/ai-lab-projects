import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Load environment variables from the .env next to this script
from pathlib import Path

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "ERROR: GOOGLE_API_KEY not found. Check your .env file or environment variables."
    )

# 2. Initialize the CHAT model (Crucial for MessageHistories)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,  # Explicitly passing the key fixes the 400 error
    temperature=0.7,
    max_output_tokens=1000,
)

# 3. Create a simple in-memory store for chat histories
store = {}


def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# 4. Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# 5. Combine the prompt and model into a runnable chain
chain = prompt | llm

# 6. Wrap the chain with message history
chain_with_history = RunnableWithMessageHistory(
    chain, get_chat_history, input_messages_key="input", history_messages_key="history"
)

session_id = "user_123"

# 7. First Interaction
print("--- Starting Conversation ---")
response1 = chain_with_history.invoke(
    {"input": "Hello! My name is Gemini User."},
    config={"configurable": {"session_id": session_id}},
)
print("AI:", response1.content)

# 8. Second Interaction (Testing Memory)
response2 = chain_with_history.invoke(
    {"input": "What is my name?"}, config={"configurable": {"session_id": session_id}}
)
print("AI:", response2.content)

print("\n--- Full Conversation History Object ---")
for message in store[session_id].messages:
    print(f"{message.type.upper()}: {message.content}")
