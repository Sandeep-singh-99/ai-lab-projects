# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os

# load_dotenv()


# def get_llm(streaming: bool = True):
#     """
#     Get the LLM instance for chat.

#     Args:
#         streaming: Whether to enable streaming responses

#     Returns:
#         ChatGoogleGenerativeAI: The LLM instance
#     """
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         streaming=streaming,
#         temperature=0.7,
#     )


from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def get_llm(streaming: bool = True, temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """
    Get the LLM instance for chat.

    Args:
        streaming (bool): Whether to enable streaming responses. Defaults to True.
        temperature (float): Controls randomness (0.0 to 1.0). Defaults to 0.7.

    Returns:
        ChatGoogleGenerativeAI: The configured LLM instance.

    Raises:
        ValueError: If GOOGLE_API_KEY is not found.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    # Safety check to prevent confusing auth errors later
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. Please check your .env file."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        streaming=streaming,
        temperature=temperature,
    )
