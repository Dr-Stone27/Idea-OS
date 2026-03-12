# Idea-OS
IdeaOS is a cognitive infrastructure designed to be a "domain-agnostic thinking OS." It forces ideas through a rigorous, multi-agent stress-testing pipeline to produce highly structured and actionable outputs.

## Phase 1 Pipeline

This repository contains **Phase 1** of the IdeaOS architecture. IdeaOS is a multi-agent system designed to take raw, unstructured problem statements, critically analyze the context, apply strategic operational frameworks, and synthesize a polished, ready-to-execute strategy.

This Phase 1 pipeline represents the core LangGraph orchestrator connecting 6 specialized agents, implemented using structured type-safe JSON outputs and programmatic routing.

## 🏗 System Architecture

The pipeline consists of the following 6 sequential agents. Each plays a distinct role, executed in order using `LangGraph`:

1. **Agent 0: The Router (`src/agents/router.py`)** 
   - **Role:** Intent & tag classification.
   - **Mechanism:** Looks at the raw input and determines the core mode (e.g., Execution, Decision) and operational domain (e.g., Product, Technical). It assigns strict `RouterTags` to guide downstream agents.
   
2. **Agent 1: The Listener (`src/agents/listener.py`)** 
   - **Role:** Crystallization & focus.
   - **Mechanism:** Takes the raw query + router tags and outputs a crisp, isolated problem statement, removing emotional baggage or rambling context.

3. **Agent 2: The Skeptic (`src/agents/skeptic.py`)** 
   - **Role:** Red-teaming & stress testing.
   - **Mechanism:** Critiques the Listener’s problem statement. It uncovers hidden assumptions, outlines "fatal flaw" risks, and generates specific questions for the next agent.
   
4. **Agent 3: The Architect (`src/agents/architect.py`)** 
   - **Role:** Structural problem solving.
   - **Mechanism:** Takes the Skeptic's challenges and selects hardcoded business frameworks (e.g., Weighted Criteria Matrix, Pre-Mortem) to structure a potential solution.
   
5. **Agent 4: The Judge (`src/agents/judge.py`)**
   - **Role:** Decision gating & quality control.
   - **Mechanism:** Scores the current state of the idea on Clarity, Defensibility, and Risk. Most importantly, it outputs a **Readiness Score** (1-10). 
   - *Conditional Routing:* If the Readiness Score is `< 5`, the LangGraph orchestrator intercepts the flow and **loops back to the Listener (Agent 1)**, forcing the system to clarify the problem before proceeding.

6. **Agent 5: The Strategist (`src/agents/strategist.py`)**
   - **Role:** Final Synthesis.
   - **Mechanism:** Taking the entire context of the run, the Strategist writes a highly actionable "Bottom Line", exact next steps, and "One Question Back" to prompt human input.

## 📂 Codebase Breakdown

*   `src/state.py`: The single source of truth for the data flow. Uses typed Pydantic models (e.g., `RouterTags`, `JudgeOutput`) wrapped in a `TypedDict` to enforce strict formatting between LLM handoffs. 
*   `src/prompts.py`: Contains the system instructions for all 6 agents. 
*   `src/graph.py`: The `LangGraph` compilation file. This file contains the `route_after_judge` function that dynamically routes the execution flow based on Agent 4's readiness score.
*   `src/agents/`: Folder containing the individual executor logic for each of the 6 agents.
*   `src/agents/mock_agents.py`: Hardcoded deterministic agents used to prove graph flow and looping logic without incurring API costs.
*   `main.py`: The primary entry point for executing the true LLM-backed multi-agent pipeline.
*   `run_mock.py`: The entry point for executing the deterministic testing pipeline.

## 🚀 Execution & Usage

### Prerequisites
1. Python 3.9+ 
2. A populated `.env` file (e.g., `GOOGLE_API_KEY=your_key_here`)

### Running the Live Pipeline
```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Running the Mock Validation Pipeline
This validates the LangGraph architecture perfectly without requiring active API billing credits.
```bash
source .venv/bin/activate
python run_mock.py
```
