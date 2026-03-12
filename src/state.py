from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

# --- Sub-Schemas for Agent Outputs ---

class RouterTags(BaseModel):
    mode: Literal["ideation", "decision", "learning", "diagnosis", "execution", "optimization"] = Field(
        description="The mode of thinking"
    )
    domain: list[Literal["product", "personal", "strategic", "operational", "creative", "technical"]] = Field(
        description="The domain(s) of the input"
    )
    depth: Literal["quick-take", "standard", "deep-dive"] = Field(
        description="The depth of thinking required"
    )
    framework_bucket: str = Field(
        description="The RAG knowledge bucket to pull from"
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="Confidence in classification"
    )
    ambiguity_note: Optional[str] = Field(
        default=None, description="Note on what is unclear (if confidence is medium/low)"
    )

class ListenerOutput(BaseModel):
    core_question: str = Field(description="The single sharpest version of what the person is trying to solve")
    context: str = Field(description="Constraints, background, relevant facts")
    assumptions_in_play: list[str] = Field(description="Beliefs the idea depends on but hasn't been verified")
    mode_domain_context: str = Field(description="How the mode/domain shapes this framing")
    handoff_note: str = Field(description="What should be challenged hardest by the Skeptic")

class SkepticOutput(BaseModel):
    strongest_aspect: str = Field(description="What genuinely holds up")
    critical_challenges: list[str] = Field(description="Most dangerous assumptions or gaps")
    questions_for_architect: list[str] = Field(description="Unresolved questions that must be addressed before structuring")
    pattern_flag: Optional[str] = Field(default=None, description="Note if this echoes a past session")
    skeptic_verdict: str = Field(description="Skeptic's bottom line verdict")

class ArchitectOutput(BaseModel):
    frameworks_applied: list[str] = Field(description="Framework names and why they fit")
    structured_breakdown: str = Field(description="The actual filled-in framework application")
    skeptic_responses: list[str] = Field(description="How challenges were addressed or if they remain open")
    open_risks: list[str] = Field(description="Challenges that cannot be structurally resolved")
    what_would_change_everything: str = Field(description="The single assumption that invalidates the structure")

class JudgeScores(BaseModel):
    clarity: int = Field(ge=0, le=10, description="Is the problem well-defined?")
    defensibility: int = Field(ge=0, le=10, description="How well were challenges addressed?")
    assumption_risk: int = Field(ge=0, le=10, description="How dangerous are remaining open assumptions? (Inverted)")
    readiness: int = Field(ge=0, le=10, description="Is this ready to act on?")
    clarity_justification: str
    defensibility_justification: str
    assumption_risk_justification: str
    readiness_justification: str

class JudgeOutput(BaseModel):
    scores: JudgeScores
    overall_verdict: Literal["Proceed", "Proceed with conditions", "Loop back"]
    the_swing_factor: str = Field(description="The specific thing that would most change this score")
    conditions: Optional[list[str]] = Field(default=None, description="What must be resolved before this is ready")
    loop_back_brief: Optional[str] = Field(default=None, description="Brief for Listener if verdict is Loop back")

class StrategistOutput(BaseModel):
    the_bottom_line: str = Field(description="3-5 sentences. What actually matters here")
    what_to_do_next: list[str] = Field(description="Specific, actionable next steps")
    what_to_watch: str = Field(description="The one thing that could change the entire picture")
    pattern_insight: Optional[str] = Field(default=None, description="Observation about broader thinking patterns")
    one_question_back: str = Field(description="The single most useful question for the person to sit with")

# --- LangGraph State ---

class IdeaOSState(TypedDict):
    """
    The state dictionary that is passed between nodes in the LangGraph.
    Data is accumulated as it flows through the pipeline.
    """
    raw_input: str
    router_tags: Optional[RouterTags]
    
    # We store the output of each agent. In P1, we only run once (mostly), 
    # but the loop-back might overwrite listener_output and skeptic_output.
    listener_output: Optional[ListenerOutput]
    skeptic_output: Optional[SkepticOutput]
    architect_output: Optional[ArchitectOutput]
    judge_output: Optional[JudgeOutput]
    strategist_output: Optional[StrategistOutput]
    
    loop_count: int
