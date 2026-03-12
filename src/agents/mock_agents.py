from src.state import IdeaOSState, RouterTags, ListenerOutput, SkepticOutput, ArchitectOutput, JudgeOutput, JudgeScores, StrategistOutput

def mock_router(state: IdeaOSState) -> dict:
    print("--- AGENT 0: ROUTER (MOCK) ---")
    return {"router_tags": RouterTags(
        mode="decision",
        domain=["product", "technical"],
        depth="standard",
        framework_bucket="product",
        confidence="high",
        ambiguity_note=None
    )}

def mock_retrieve_context(state: IdeaOSState) -> dict:
    print("--- PRE-PIPELINE: RETRIEVING CONTEXT (MOCK) ---")
    return {"framework_context": [{"name": "Mock Framework", "bucket": ["product"], "structure": "Mock structure"}]}

def mock_listener(state: IdeaOSState) -> dict:
    print("--- AGENT 1: LISTENER (MOCK) ---")
    return {"listener_output": ListenerOutput(
        core_question="Should we build a custom time-tracking UX or integrate Toggl's API faster?",
        context="Engineering prefers integration for speed, Product prefers custom for UX control.",
        assumptions_in_play=["Custom UX will yield better retention", "Toggl integration is genuinely faster"],
        mode_domain_context="Decision between technical speed and product UX.",
        handoff_note="Challenge the assumption that Toggl integration means bad UX."
    )}

def mock_skeptic(state: IdeaOSState) -> dict:
    print("--- AGENT 2: SKEPTIC (MOCK) ---")
    return {"skeptic_output": SkepticOutput(
        strongest_aspect="The tradeoff between speed and control is clearly identified.",
        critical_challenges=[
            "Assumption that Toggl's UX is poor has not been validated.",
            "You are assuming building custom won't take 3x the estimated time."
        ],
        questions_for_architect=["What specific UX flow cannot be achieved with Toggl's API?"],
        pattern_flag=None,
        skeptic_verdict="Needs validation on the actual UX limitations of the Toggl API before committing to a custom build."
    )}

def mock_architect(state: IdeaOSState) -> dict:
    print("--- AGENT 3: ARCHITECT (MOCK) ---")
    return {"architect_output": ArchitectOutput(
        frameworks_applied=["Weighted Criteria Matrix", "Pre-Mortem"],
        structured_breakdown="Criteria: Time to Market (Toggl wins), UX Control (Custom wins), Maintenance Cost (Toggl wins).",
        skeptic_responses=["We must spike the Toggl API to see if it supports our exact UX requirement."],
        open_risks=["Without an API spike, we are guessing at Toggl's limitations."],
        what_would_change_everything="If Toggl's API supports custom headless UI, the custom build argument vanishes."
    )}

def mock_judge(state: IdeaOSState) -> dict:
    print("--- AGENT 4: JUDGE (MOCK) ---")
    # Simulate a loop once to prove the graph works
    if state.get("loop_count", 0) == 0:
        return {"judge_output": JudgeOutput(
            scores=JudgeScores(
                clarity=8, defensibility=4, assumption_risk=8, readiness=4,
                clarity_justification="Clear question.", defensibility_justification="Spike isn't done.",
                assumption_risk_justification="High risk of wasted Eng time.", readiness_justification="Not ready to act."
            ),
            overall_verdict="Loop back",
            the_swing_factor="The API Spike.",
            conditions=None,
            loop_back_brief="The Architect realized we are guessing about Toggl's API. Please re-frame the core question as an exploration/learning goal about Toggl's capabilities first."
        )}
    else:
        return {"judge_output": JudgeOutput(
            scores=JudgeScores(
                clarity=9, defensibility=8, assumption_risk=3, readiness=8,
                clarity_justification="Clear question.", defensibility_justification="Risk acknowledged.",
                assumption_risk_justification="Lowered by the spike condition.", readiness_justification="Ready to execute spike."
            ),
            overall_verdict="Proceed with conditions",
            the_swing_factor="The outcome of the Toggl API Spike.",
            conditions=["Complete a 2-day technical spike on Toggl headless UI."],
            loop_back_brief=None
        )}

def mock_strategist(state: IdeaOSState) -> dict:
    print("--- AGENT 5: STRATEGIST (MOCK) ---")
    return {"strategist_output": StrategistOutput(
        the_bottom_line="You are debating a build vs buy without knowing the actual limits of the buy option.",
        what_to_do_next=["Task engineering to do a 2-day API spike on Toggl.", "Have Product list the 3 absolute dealbreaker UX requirements."],
        what_to_watch="If the spike takes longer than 2 days, Toggl might not be as fast as assumed.",
        pattern_insight=None,
        one_question_back="If building custom takes 3 months instead of 3 weeks, would Product still demand it?"
    )}
