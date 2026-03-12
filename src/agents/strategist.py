import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import IdeaOSState, StrategistOutput

from src.prompts import STRATEGIST_SYSTEM_PROMPT

def run_strategist(state: IdeaOSState) -> dict:
    """
    Agent 5: The Strategist.
    Synthesizes the entire pipeline into clear, actionable output.
    """
    print("--- AGENT 5: STRATEGIST ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
    structured_llm = llm.with_structured_output(StrategistOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", STRATEGIST_SYSTEM_PROMPT),
        ("human", """
ROUTER CLASSIFICATION:
Mode: {mode}

LISTENER:
{core_question}

SKEPTIC VERDICT:
{skeptic_verdict}

ARCHITECT SUMMARY:
{frameworks}

JUDGE VERDICT:
{judge_verdict} (Clarity: {clarity}, Defensibility: {defens}, Risk: {risk}, Readiness: {readiness})
Swing Factor: {swing_factor}
Conditions: {conditions}
""")
    ])
    
    chain = prompt | structured_llm
    
    out: StrategistOutput = chain.invoke({
        "mode": state["router_tags"].mode,
        "core_question": state["listener_output"].core_question,
        "skeptic_verdict": state["skeptic_output"].skeptic_verdict,
        "frameworks": ", ".join(state["architect_output"].frameworks_applied),
        "judge_verdict": state["judge_output"].overall_verdict,
        "clarity": state["judge_output"].scores.clarity,
        "defens": state["judge_output"].scores.defensibility,
        "risk": state["judge_output"].scores.assumption_risk,
        "readiness": state["judge_output"].scores.readiness,
        "swing_factor": state["judge_output"].the_swing_factor,
        "conditions": "\n".join(f"- {c}" for c in state["judge_output"].conditions) if state["judge_output"].conditions else "None"
    })
    
    time.sleep(4)
    return {"strategist_output": out}
