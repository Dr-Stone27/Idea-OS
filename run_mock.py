from langgraph.graph import StateGraph, END
from src.state import IdeaOSState
from src.graph import route_after_judge, increment_loop
from main import print_result

from src.agents.mock_agents import (
    mock_router, mock_listener, mock_skeptic, 
    mock_architect, mock_judge, mock_strategist
)

def build_mock_graph():
    workflow = StateGraph(IdeaOSState)
    
    workflow.add_node("router", mock_router)
    workflow.add_node("listener", mock_listener)
    workflow.add_node("skeptic", mock_skeptic)
    workflow.add_node("architect", mock_architect)
    workflow.add_node("judge", mock_judge)
    workflow.add_node("strategist", mock_strategist)
    workflow.add_node("increment_loop", increment_loop)

    workflow.set_entry_point("router")
    workflow.add_edge("router", "listener")
    workflow.add_edge("listener", "skeptic")
    workflow.add_edge("skeptic", "architect")
    workflow.add_edge("architect", "judge")
    
    workflow.add_conditional_edges(
        "judge",
        route_after_judge,
        {
            "listener": "increment_loop",
            "strategist": "strategist"
        }
    )
    
    workflow.add_edge("increment_loop", "listener")
    workflow.add_edge("strategist", END)
    
    return workflow.compile()

if __name__ == "__main__":
    app = build_mock_graph()
    
    initial_state = {
        "raw_input": "Should we build a custom time-tracking UX or integrate Toggl's API faster?",
        "loop_count": 0
    }
    
    print("Executing Mock IdeaOS Pipeline...")
    final_state = app.invoke(initial_state)
    print_result(final_state)
