import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import IdeaOSState, ListenerOutput

from src.prompts import LISTENER_SYSTEM_PROMPT

def run_listener(state: IdeaOSState) -> dict:
    """
    Agent 1: The Listener.
    Crystallizes raw input into a clean problem statement.
    """
    print("--- AGENT 1: LISTENER ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    structured_llm = llm.with_structured_output(ListenerOutput)
    
    # If the system looped back from the Judge, we inject the Skeptic flags
    loop_context = ""
    if state.get("loop_count", 0) > 0 and state.get("judge_output"):
        loop_context = f"\n\n[SYSTEM NOTE: This input was rejected by the Judge. Please re-crystallize incorporating this feedback:\n{state['judge_output'].loop_back_brief}]"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", LISTENER_SYSTEM_PROMPT),
        ("human", "ROUTER CLASSIFICATION:\nMode: {mode}\nDomain: {domain}\n\nRAW INPUT:\n{raw_input}{loop_context}")
    ])
    
    chain = prompt | structured_llm
    
    tags = state["router_tags"]
    
    result: ListenerOutput = chain.invoke({
        "mode": tags.mode,
        "domain": ", ".join(tags.domain),
        "raw_input": state["raw_input"],
        "loop_context": loop_context
    })
    
    time.sleep(4)
    return {"listener_output": result}
