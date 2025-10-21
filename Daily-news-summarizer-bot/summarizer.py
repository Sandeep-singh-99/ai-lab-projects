from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def summarize_news(news_items):
    titles = "\n".join([f" -{n['title']}" for n in news_items])
    prompt = PromptTemplate.from_template(
        "Summarize the following news headlines in 3-5 points:\n\n{titles}"
    )

    final_prompt = prompt.format(titles=titles)
    response = llm.invoke(final_prompt)
    return response.content