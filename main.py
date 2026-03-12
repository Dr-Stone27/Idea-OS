import os
from dotenv import load_dotenv, find_dotenv

from src.graph import build_graph

# Load Google API Key
load_dotenv(find_dotenv())

def print_result(state):
    print("\n" + "="*50)
    print("                 IDEAOS OUTPUT                 ")
    print("="*50 + "\n")
    
    print(f"ROUTER CLASSIFICATION: [MODE: {state['router_tags'].mode.upper()}] | [DOMAIN: {', '.join(state['router_tags'].domain).upper()}]")
    print("-" * 50)
    
    print(f"1. CORE QUESTION (Listener):\n   {state['listener_output'].core_question}\n")
    
    print(f"2. THE SKEPTIC'S VERDICT:\n   {state['skeptic_output'].skeptic_verdict}\n")
    
    print(f"3. APPLIED FRAMEWORK(S) (Architect):")
    for f in state['architect_output'].frameworks_applied:
        print(f"   - {f}")
    print()
    
    print(f"4. THE JUDGE'S VERDICT: {state['judge_output'].overall_verdict.upper()}")
    print(f"   Clarity: {state['judge_output'].scores.clarity}/10")
    print(f"   Defensibility: {state['judge_output'].scores.defensibility}/10")
    print(f"   Risk: {state['judge_output'].scores.assumption_risk}/10 (higher is worse)")
    print(f"   Readiness: {state['judge_output'].scores.readiness}/10")
    if state['judge_output'].conditions:
        print("   Conditions to Proceed:")
        for c in state['judge_output'].conditions:
            print(f"     - {c}")
    print("-" * 50)
    
    s_out = state['strategist_output']
    print(f"5. THE STRATEGIST (Synthesis):\n")
    print(f"THE BOTTOM LINE:\n{s_out.the_bottom_line}\n")
    
    print("WHAT TO DO NEXT:")
    for a in s_out.what_to_do_next:
        print(f"- {a}")
    print()
    
    print(f"ONE QUESTION BACK:\n{s_out.one_question_back}\n")
    print("="*50)

if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY") == "your_api_key_here":
        print("ERROR: Please set GOOGLE_API_KEY in the .env file.")
        exit(1)

    # Test Input 1: An ambiguously broad starting point
    input_text = """
    I want to build a new feature into our web app where users can track how much time 
    they spend on different projects. But I don't know if we should build it internally 
    or just integrate with Toggl's API. Engineering says integration is faster but 
    product thinks we lose control over the UX. What should we do?
    """
    
    print(f"RAW INPUT:\n{input_text.strip()}\n")
    
    app = build_graph()
    
    initial_state = {
        "raw_input": input_text.strip(),
        "loop_count": 0
    }
    
    try:
        final_state = app.invoke(initial_state)
        print_result(final_state)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
