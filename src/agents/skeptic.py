import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import IdeaOSState, SkepticOutput

from src.prompts import SKEPTIC_SYSTEM_PROMPT

def run_skeptic(state: IdeaOSState) -> dict:
    """
    Agent 2: The Skeptic.
    Red-teams assumptions and stress-tests the statement.
    In Phase 1, we use Gemini Pro instead of Opus.
    """
    print("--- AGENT 2: SKEPTIC ---")
    
    # We use a higher temperature for divergent thinking
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    structured_llm = llm.with_structured_output(SkepticOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SKEPTIC_SYSTEM_PROMPT),
        ("human", "ROUTER TAGS:\nMode: {mode}\nDomain: {domain}\n\nLISTENER OUTPUT:\nCore Question: {core_question}\nAssumptions: {assumptions}\nHandoff Note: {handoff_note}")
    ])
    
    chain = prompt | structured_llm
    
    out: SkepticOutput = chain.invoke({
        "mode": state["router_tags"].mode,
        "domain": ", ".join(state["router_tags"].domain),
        "core_question": state["listener_output"].core_question,
        "assumptions": "\n".join(f"- {a}" for a in state["listener_output"].assumptions_in_play),
        "handoff_note": state["listener_output"].handoff_note
    })
    
    time.sleep(4)
    return {"skeptic_output": out}
