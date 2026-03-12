import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import IdeaOSState, RouterTags

from src.prompts import ROUTER_SYSTEM_PROMPT

def run_router(state: IdeaOSState) -> dict:
    """
    Agent 0: The Router.
    Classifies intent and domain. Fires before the main pipeline.
    """
    print("--- AGENT 0: ROUTER ---")
    
    # We use a temperature of 0.1 for near-deterministic classification
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
    
    # Bind the Pydantic model so Gemini returns structured JSON
    structured_llm = llm.with_structured_output(RouterTags)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", ROUTER_SYSTEM_PROMPT),
        ("human", "Classify this input:\n\n{raw_input}")
    ])
    
    chain = prompt | structured_llm
    
    result: RouterTags = chain.invoke({"raw_input": state["raw_input"]})
    
    time.sleep(4)
    return {"router_tags": result}
