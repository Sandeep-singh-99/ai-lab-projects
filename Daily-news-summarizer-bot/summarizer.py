from dotenv import load_dotenv
import os
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# from langchain_community.prompts import PromptTemplate

load_dotenv()

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
llm = OllamaLLM(model="gemma3:1b", temperature=0)

# def summarize_news(news_items):
#     titles = "\n".join([f" -{n['title']}" for n in news_items])
#     prompt = PromptTemplate.from_template(
#         "Summarize the following news headlines in 3-5 points:\n\n{titles}"
#     )

#     final_prompt = prompt.format(titles=titles)
#     response = llm.invoke(final_prompt)
#     return response.content

def summarize_news(news_items):
    titles = "\n".join([f" - {n['title']}" for n in news_items])
    
    prompt_template = """
    Summarize the following news headlines in 3-5 points:

    {titles}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    final_prompt = prompt.format(titles=titles)
    
    # Use Ollama to generate response
    response = llm.invoke(final_prompt)
    return response