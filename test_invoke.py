import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

print("Testing gemini-2.0-flash-lite...")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)
try:
    res = llm.invoke("Hi")
    print("gemini-2.0-flash-lite success:", res.content)
except Exception as e:
    print("gemini-2.0-flash-lite failed:", type(e).__name__, str(e))

print("Testing gemini-flash-lite-latest...")
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0)
try:
    res = llm.invoke("Hi")
    print("gemini-flash-lite-latest success:", res.content)
except Exception as e:
    print("gemini-flash-lite-latest failed:", type(e).__name__, str(e))
