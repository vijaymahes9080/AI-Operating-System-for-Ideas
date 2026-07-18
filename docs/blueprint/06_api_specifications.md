# API Specifications

IdeasOS exposes a structured **REST API (via FastAPI)** for system control, file ingestion, and graph queries, combined with **WebSockets** for streaming agent communications, and **NATS Pub/Sub** for event-driven message queuing.

---

## 1. REST Endpoints (OpenAPI Spec)

Below is the OpenAPI-compliant interface specification for the primary runtime controllers.

### Ingestion: `POST /api/v1/inbox/ingest`
Ingests unstructured documents, audio, or links into the Idea Inbox.
- **Request Type**: `multipart/form-data`
- **Request Body**:
  - `title`: String (Optional)
  - `source_type`: String (Enum: `TEXT`, `VOICE`, `IMAGE`, `PDF`, `WEBSITE`, `GITHUB`)
  - `file`: File binary (Optional)
  - `url`: String (Optional)
- **Response** (`202 Accepted`):
  ```json
  {
    "inbox_id": "inb_87f9e8a7bc",
    "status": "QUEUED",
    "received_at": "2026-07-03T10:25:00Z",
    "message": "File uploaded and scheduled for background parsing."
  }
  ```

### Analysis: `GET /api/v1/project/{project_id}/intelligence`
Retrieves synthesized analysis scores (Complexity, Patentability, Innovation DNA) from the Idea Intelligence Engine.
- **Response** (`200 OK`):
  ```json
  {
    "project_id": "proj_a2f897db",
    "dna_hash": "dna_c3029f2bb0a11",
    "scores": {
      "innovation": 0.89,
      "patent_potential": 0.74,
      "monetization": 0.65,
      "difficulty": "HIGH"
    },
    "estimated_development_hours": 320,
    "missing_requirements": [
      "No database configuration was specified in the raw proposal",
      "Authentication method is unknown"
    ]
  }
  ```

### Graph Mutation: `POST /api/v1/graph/node`
Applies structural updates manually to the Knowledge Graph.
- **Request Body**:
  ```json
  {
    "project_id": "proj_a2f897db",
    "node_label": "Task",
    "properties": {
      "title": "Configure SQLite-vec DB connection",
      "status": "TODO",
      "priority": "HIGH"
    }
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "node_id": "node_t_4892c90f",
    "success": true
  }
  ```

---

## 2. WebSocket Real-Time Interface

Used by the Tauri UI to stream terminal logs and agent conversations.

### Agent Streaming Connection: `WS /api/v1/ws/agents/{session_id}`
- **Client Frame (Authentication & Subscription)**:
  ```json
  {
    "action": "subscribe",
    "agent_id": "research_agent"
  }
  ```
- **Server Stream Frame (Token Generation)**:
  ```json
  {
    "event": "agent_token",
    "agent_id": "research_agent",
    "chunk": "Based on our academic research on SQLite vector extensions, we recommend using...",
    "timestamp": 1783074300
  }
  ```
- **Server Stream Frame (Tool Execution Update)**:
  ```json
  {
    "event": "tool_start",
    "tool_name": "arxiv_search",
    "query": "SQLite-vec performance benchmarks",
    "timestamp": 1783074315
  }
  ```

---

## 3. NATS Message Broker Event Schema

The background Python workers, Tauri processes, and CLI utilities communicate over NATS pub/sub channels.

### Subject: `ideas.inbox.received`
Fired when a new raw inbox item is created.
```json
{
  "inbox_id": "inb_87f9e8a7bc",
  "workspace_id": "work_09df878a",
  "source_type": "PDF",
  "storage_path": "/var/data/inbox/paper.pdf"
}
```

### Subject: `ideas.agent.task.proposed`
Fired when the Product Planner agent suggests a new subtask to the database.
```json
{
  "project_id": "proj_a2f897db",
  "proposed_by": "planning_agent",
  "task": {
    "title": "Setup pytest configuration file",
    "estimated_hours": 1.5,
    "priority": "LOW",
    "dependencies": []
  }
}
```
