# User Flows

This document details the step-by-step interactive flows for key user activities in IdeasOS.

---

## 1. Flow A: Ingesting an Idea to Graph Mapping

This flow maps how a raw user idea input is digested, structured, researched, and linked to the Knowledge Graph.

```
[ User ]                      [ Ingestion UI ]              [ FastAPI Backend ]              [ LLM / RAG Agent ]           [ Database / Graph ]
   |                                 |                               |                                |                             |
   |-- 1. Drags PDF Research paper -->|                               |                                |                             |
   |   (or speaks Voice Note)        |-- 2. POST /inbox/ingest ---->|                                |                             |
   |                                 |                               |-- 3. Parse content (Whisper/Tika)|                            |
   |                                 |                               |-- 4. Publish NATS Event ------>|                             |
   |                                 |                               |                                |-- 5. Fetch academic links ->|
   |                                 |                               |                                |-- 6. Evaluate Innovation ->|
   |                                 |                               |                                |                             |-- 7. Write Neo4j Node & Edges
   |                                 |                               |<-- 8. WS Stream Update --------|                             |
   |<-- 9. Dynamic Graph updates ----|                               |                                |                             |
```

1. **Upload Phase**: The user drags a PDF paper or speaks a voice note in the **Inbox View**.
2. **Ingestion Request**: The React UI calls `POST /api/v1/inbox/ingest` carrying the media payload.
3. **Cognitive Parsing**: The backend processes the media (e.g., runs Whisper for audio, Tika for PDF text) and stores the raw text inside SQLite `raw_inbox`.
4. **Agent Analysis**: NATS triggers the `Research Agent` to extract keywords and search arXiv or patents in the background.
5. **Score Generation**: The `Idea Intelligence Engine` computes novelty, monetization potential, and developer complexity.
6. **Graph Creation**: The database client inserts node relationships (e.g. `(Project) -[:HAS_CONCEPT]-> (Concept) -[:RESOLVED_BY]-> (ResearchPaper)`).
7. **UI Render**: The backend sends a message over WebSockets to trigger a React state transition, dynamically rendering the new nodes in the **Knowledge Graph Viewer**.

---

## 2. Flow B: Running a Multi-Agent Architecture Debate

This flow maps how architectural or product decisions are validated using the AI Debate Room.

1. **Trigger Debate**: In the **Planner View**, the user clicks "Run AI Debate" on a proposed feature.
2. **Select Personas**: The user selects or approves debate participants (e.g., "Postgres Maximalist", "SQLite/Local-First Advocate", "Security Architect").
3. **Initialize Chamber**: The backend launches a LangGraph state loop, instantiating the prompt system template configurations for each agent.
4. **Round-Robin Arguments**:
   - Agent 1 (Postgres) argues: *"Postgres provides row-level security and scales horizontally."*
   - Agent 2 (SQLite) critiques: *"Postgres requires a separate server process, breaking our offline-first local desktop requirement. SQLite is embedded and faster."*
   - Agent 3 (Security) summarizes: *"SQLite is acceptable, but we must implement local database encryption (AES-256) at rest."*
5. **Record Choice**: The supervisor agent compiles the debate transcript, outputs a recommendation, and automatically saves the resolution to the `Decision Ledger` database table.

---

## 3. Flow C: Autonomous Code Generation & Self-Repair Loop

This flow maps how the coding and testing agents implement features and auto-correct errors.

```
       +--------------------------------------------+
       |                                            |
       v                                            |
[Code Generation] ---> [Write to File] ---> [Execute Compiler / Pytest]
                                            /                      \
                                        (Pass)                    (Fail)
                                          /                          \
                                         v                            v
                                  [Git Commit Code]         [Pass logs to Coder Agent]
```

1. **Select Task**: The developer assigns a task card marked "Code Synthesis" to the `Coding Agent`.
2. **Boilerplate Creation**: The agent reads the system schemas (`04_database_design.md` specs) and outputs the initial code structure.
3. **Execution Verification**: The `QA Agent` spins up a subprocess executing `pytest` or `npm run build` inside the local project folder.
4. **Self-Repair Logic**:
   - **Scenario A (Compilation Fails)**: The compiler returns stack trace errors. The QA agent feeds these error strings back into the Coding agent's short-term history prompt. The coder repairs the file. The process loops until compilation passes.
   - **Scenario B (Compilation Passes)**: The files are saved, and the task status updates to `DONE`.
