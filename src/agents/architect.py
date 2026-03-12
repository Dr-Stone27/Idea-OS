import time
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import IdeaOSState, ArchitectOutput

from src.prompts import ARCHITECT_SYSTEM_PROMPT

def run_architect(state: IdeaOSState) -> dict:
    """
    Agent 3: The Architect.
    Applies hardcoded frameworks (Phase 1) to structure the idea and respond to the Skeptic.
    """
    print("--- AGENT 3: ARCHITECT ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.4)
    structured_llm = llm.with_structured_output(ArchitectOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", ARCHITECT_SYSTEM_PROMPT),
        ("human", """
ROUTER TAGS:
Mode: {mode}
Domain: {domain}

LISTENER (PROBLEM STATEMENT):
Core Question: {core_question}
Context: {context}

SKEPTIC (CHALLENGES):
Verdict: {skeptic_verdict}
Critical Challenges:
{challenges}

Questions You Must Answer:
{questions}

FRAMEWORK CONTEXT (Retrieved from Knowledge Base):
{framework_context}
""")
    ])
    
    chain = prompt | structured_llm
    
    out: ArchitectOutput = chain.invoke({
        "mode": state["router_tags"].mode,
        "domain": ", ".join(state["router_tags"].domain),
        "core_question": state["listener_output"].core_question,
        "context": state["listener_output"].context,
        "skeptic_verdict": state["skeptic_output"].skeptic_verdict,
        "challenges": "\n".join(f"- {c}" for c in state["skeptic_output"].critical_challenges),
        "questions": "\n".join(f"- {q}" for q in state["skeptic_output"].questions_for_architect),
        "framework_context": json.dumps(state.get("framework_context", []), indent=2)
    })
    
    time.sleep(4)
    return {"architect_output": out}
