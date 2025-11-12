from typing import TypedDict, Annotated, Optional
from langgraph.graph import add_messages, StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv
import json
from uuid import uuid4
from langgraph.checkpoint.memory import MemorySaver
from langchain_tavily import TavilySearch
import streamlit as st

load_dotenv()

memory = MemorySaver()

search_tool = TavilySearch(max_results=3)