# AI Agent Architecture & Coordination

IdeasOS features a specialized, collaborative multi-agent execution framework built using **LangGraph** and **LlamaIndex**. Instead of relying on a single large LLM prompt, tasks are delegated to specialized cognitive roles that critique, refine, and check each other's outputs.

---

## 1. Multi-Agent Orchestration Topologies

IdeasOS supports three multi-agent patterns, depending on complexity:

### A. Supervisor Pattern
Used for general execution (e.g., generating a full application blueprint). A central supervisor agent assigns tasks to sub-agents (Research, Architect, Coder), collects their outputs, validates constraints, and reports back.

```
       [ Supervisor Agent ]
          /      |      \
         v       v       v
    [Research] [Architect] [Coder]
```

### B. Peer-to-Peer Critique (QA Loop)
Used for code synthesis and testing. The Coding Agent generates files, passes them to the Testing/QA Agent for review. If linting or tests fail, the feedback is piped back to the coder for automated repair.

```
[Coding Agent]  ======(Output)======>  [QA / Compiler Agent]
      ^                                          |
      |=========== (Error Log / Critique) =======|
```

### C. Multi-Agent Debate Room
Used for strategic decisions (e.g., evaluating business monetization strategies, framework choices). A supervisor spins up conflicting agent personas (e.g., "Maximalist Rust Dev" vs "Pragmatic Python Dev") to debate trade-offs.

---

## 2. LangGraph State Machine Architecture

Below is the state representation and node transition logic for a standard execution loop in Python.

```python
# backend/app/agents/state.py
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

class AgentWorkspaceState(TypedDict):
    project_id: str
    idea_description: str
    current_phase: str  # e.g., 'RESEARCH', 'PLANNING', 'CODING'
    knowledge_graph_snapshot: Dict[str, Any]
    compiled_requirements: Dict[str, Any]
    files_written: List[str]
    errors_encountered: List[str]
    debate_transcripts: List[str]
    next_step: str

# Define node operations
def run_research_phase(state: AgentWorkspaceState) -> Dict[str, Any]:
    # Invoke Autonomous Research Agent tool suite
    # Save findings to state and write nodes to knowledge graph
    return {"current_phase": "PLANNING", "next_step": "PLAN_PROJECT"}

def run_planning_phase(state: AgentWorkspaceState) -> Dict[str, Any]:
    # Generate PRD and Tasks lists
    return {"current_phase": "ARCHITECTURE", "next_step": "ARCHITECT_SYSTEM"}

def run_architecture_phase(state: AgentWorkspaceState) -> Dict[str, Any]:
    # Build database schema and API specs
    return {"current_phase": "CODING", "next_step": "WRITE_CODE"}

def run_coding_phase(state: AgentWorkspaceState) -> Dict[str, Any]:
    # Call coder agent to synthesize code files
    return {"current_phase": "VERIFY", "next_step": "RUN_TESTS"}

def verify_and_test(state: AgentWorkspaceState) -> Dict[str, Any]:
    # Run generated tests. If errors -> go back to CODING, else END
    if state.get("errors_encountered"):
        return {"next_step": "WRITE_CODE"}
    return {"next_step": "END"}

# Building the Graph
workflow = StateGraph(AgentWorkspaceState)

workflow.add_node("research", run_research_phase)
workflow.add_node("planning", run_planning_phase)
workflow.add_node("architecture", run_architecture_phase)
workflow.add_node("coding", run_coding_phase)
workflow.add_node("verify", verify_and_test)

workflow.set_entry_point("research")

# Conditional Router Logic
def route_next_node(state: AgentWorkspaceState):
    nxt = state["next_step"]
    if nxt == "PLAN_PROJECT":
        return "planning"
    elif nxt == "ARCHITECT_SYSTEM":
        return "architecture"
    elif nxt == "WRITE_CODE":
        return "coding"
    elif nxt == "RUN_TESTS":
        return "verify"
    else:
        return END

workflow.add_conditional_edges(
    "verify",
    route_next_node,
    {
        "planning": "planning",
        "architecture": "architecture",
        "coding": "coding",
        "verify": "verify",
        "END": END
    }
)
```

---

## 3. Agent Session Memory & Context Window Management

To prevent agent token bloat and context drift:
1. **Short-Term Context (Zustand/In-Memory)**: Keeps the immediate chat message history and tool feedback logs.
2. **Intermediate Graph State (Neo4j)**: Stores structural dependencies (e.g. "Task B blocks Task A"). Instead of feeding all task cards to the LLM, the agent queries the local Graph to extract only immediate parent and child nodes.
3. **Long-Term Indexing (SQLite / SQLite-vec)**: Compresses raw logs, historical decisions, and transcript sessions. When context size exceeds 8,000 tokens, older transcript details are summarized into a concise context block and appended as a single prompt parameter.
