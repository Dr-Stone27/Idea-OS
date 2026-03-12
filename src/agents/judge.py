import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import IdeaOSState, JudgeOutput

from src.prompts import JUDGE_SYSTEM_PROMPT

def run_judge(state: IdeaOSState) -> dict:
    """
    Agent 4: The Judge.
    Scores confidence and flags open risks.
    In Phase 1, we use Gemini Pro instead of Opus.
    """
    print("--- AGENT 4: JUDGE ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    structured_llm = llm.with_structured_output(JudgeOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", JUDGE_SYSTEM_PROMPT),
        ("human", """
ROUTER CLASSIFICATION:
Mode: {mode}

LISTENER (PROBLEM):
Core Question: {core_question}

SKEPTIC (CHALLENGES):
Critical Challenges:
{challenges}

ARCHITECT (STRUCTURE):
Frameworks Applied: {frameworks}
Skeptic Responses:
{skeptic_responses}
Open Risks:
{open_risks}
""")
    ])
    
    chain = prompt | structured_llm
    
    out: JudgeOutput = chain.invoke({
        "mode": state["router_tags"].mode,
        "core_question": state["listener_output"].core_question,
        "challenges": "\n".join(f"- {c}" for c in state["skeptic_output"].critical_challenges),
        "frameworks": ", ".join(state["architect_output"].frameworks_applied),
        "skeptic_responses": "\n".join(f"- {r}" for r in state["architect_output"].skeptic_responses),
        "open_risks": "\n".join(f"- {r}" for r in state["architect_output"].open_risks)
    })
    
    time.sleep(4)
    return {"judge_output": out}
