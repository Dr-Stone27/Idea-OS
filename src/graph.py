from langgraph.graph import StateGraph, END

from src.state import IdeaOSState
from src.agents.router import run_router
from src.agents.listener import run_listener
from src.agents.skeptic import run_skeptic
from src.agents.architect import run_architect
from src.agents.judge import run_judge
from src.agents.strategist import run_strategist

def route_after_judge(state: IdeaOSState) -> str:
    """
    Conditional routing logic after the Judge scores the idea.
    If Readiness < 5 and we haven't looped too many times, go back to Listener.
    Otherwise, proceed to Strategist.
    """
    if state["judge_output"].scores.readiness < 5 and state.get("loop_count", 0) < 2:
        print("[ORCHESTRATOR] Judge readiness < 5. Looping back to Listener...")
        # Increment loop count (LangGraph states update by returning dicts)
        # We need a small node to increment it safely, or handle it in the Judge.
        # For simplicity, we just do it here statically though LangGraph prefers node updates.
        return "listener"
    
    return "strategist"

def increment_loop(state: IdeaOSState) -> dict:
    """Helper node to safely increment the loop count when a loop occurs."""
    current = state.get("loop_count", 0)
    return {"loop_count": current + 1}

def build_graph():
    # Initialize the graph with our state schema
    workflow = StateGraph(IdeaOSState)
    
    # Add all 6 agents as nodes
    workflow.add_node("router", run_router)
    workflow.add_node("listener", run_listener)
    workflow.add_node("skeptic", run_skeptic)
    workflow.add_node("architect", run_architect)
    workflow.add_node("judge", run_judge)
    workflow.add_node("strategist", run_strategist)
    
    # Add a helper node to increment loop counter before hitting the listener again
    workflow.add_node("increment_loop", increment_loop)

    # Define the sequential pipeline flow
    workflow.set_entry_point("router")
    workflow.add_edge("router", "listener")
    workflow.add_edge("listener", "skeptic")
    workflow.add_edge("skeptic", "architect")
    workflow.add_edge("architect", "judge")
    
    # Define conditional routing from the judge
    workflow.add_conditional_edges(
        "judge",
        route_after_judge,
        {
            "listener": "increment_loop",
            "strategist": "strategist"
        }
    )
    
    # Connect the increment helper back to the listener
    workflow.add_edge("increment_loop", "listener")
    
    # Strategist goes to END
    workflow.add_edge("strategist", END)
    
    return workflow.compile()
