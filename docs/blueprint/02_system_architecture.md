# System Architecture & Topology

IdeasOS uses a **hybrid local-first, service-oriented architecture** that runs fully on a developer's desktop without requiring Docker, while maintaining the capability to scale to distributed enterprise clouds.

---

## 1. High-Level Component Topology

The local deployment topology isolates native desktop capabilities (file system access, system tray, window management) in Rust (Tauri), client interfaces in TypeScript (React), and background cognitive computations, agent scheduling, and file parsers in Python (FastAPI).

```
+--------------------------------------------------------------------------------+
|                           LOCAL DESKTOP MACHINE                                |
|                                                                                |
|  +---------------------------+             +--------------------------------+  |
|  |     TAURI DESKTOP APP     |             |         FASTAPI BACKEND        |  |
|  |  +---------------------+  |             |  +--------------------------+  |  |
|  |  | React TS Front-end  |  |             |  | API Router (Uvicorn)     |  |  |
|  |  +----------+----------+  |             |  +------------+-------------+  |  |
|  |             |             |             |               |                |  |
|  |      Rust Window IPC      |             |     LangGraph / LiteLLM        |  |  |
|  +-------------+-------------+             |  +------------+-------------+  |  |
|                |                           |               |                |  |
|                | WebSocket / HTTP          |      Temporal / In-Memory      |  |  |
|                +--------------------------->  +------------+-------------+  |  |
|                                            |               |                |  |
|                                            |     NATS Messaging Server      |  |  |
|                                            +---------------+----------------+  |
|                                                            |                   |
|  +---------------------------------------------------------v----------------+  |
|  |                               DATA LAYER                                 |  |
|  |  +-----------------+  +-------------------+  +------------------------+  |  |
|  |  |  SQLite Metadata|  | Neo4j (Local Port)|  | SQLite-vec Vector DB   |  |  |
|  |  +-----------------+  +-------------------+  +------------------------+  |  |
|  +--------------------------------------------------------------------------+  |
+--------------------------------------------------------------------------------+
```

---

## 2. C4 Context & Container Level

### Level 1: System Context
- **User**: Interacts with the interface to input ideas, guide research, review designs, and execute code tasks.
- **IdeasOS**: The cognitive desktop operating system operating locally.
- **External Interfaces**:
  - **Ollama / local model runtimes** via local APIs.
  - **Commercial LLM API Gateways** (Anthropic, OpenAI, DeepSeek, Google Gemini) via LiteLLM.
  - **Web Search APIs** (Tavily, Serper) for research tools.
  - **GitHub API** for code pushes/pulls and repository ingestion.

### Level 2: Container Spec

1. **Desktop Client (Tauri/Vite/React/TS)**:
   - Renders visual graphs, workspace views, interactive editors, and agent terminals.
   - Saves client state in Zustand, synced with IndexedDB.
   - Interacts with system APIs (like filesystem directories, global keyboard shortcuts, local files) using Tauri's Rust commands.

2. **Core Server (Python FastAPI)**:
   - Exposes REST APIs for file uploads, workspace queries, and dashboard updates.
   - Runs WebSockets for real-time Agent Chat streams, log outputs, and graph event mutations.
   - Implements cognitive routines via LlamaIndex (for data loading and RAG) and LangGraph (for multi-agent loop orchestration).

3. **Message & Event Broker (NATS)**:
   - Operates as a lightweight local binary.
   - Coordinates event-driven triggers between the API server, worker threads, and CLI applications.

4. **Workflow Orchestration (Temporal / In-Memory Runner)**:
   - Guarantees execution of long-running operations (such as multi-hour web scraping or complex prototype builds) with full state survival across application crashes.

5. **Storage Container Suite**:
   - **SQLite**: Local system configuration, project state, task management tables, and cache. Uses WAL mode.
   - **SQLite-vec / Qdrant**: Local vector index database. SQLite-vec loads dynamically inside SQLite to store embeddings locally without a server. Qdrant is supported for enterprise network hosting.
   - **Neo4j / Embedded Graph**: Graphic representations of knowledge networks. Local Neo4j CE (Community Edition) or an embedded NetworkX database for absolute local independence.

---

## 3. Data Flow & Sync Topologies

IdeasOS uses a **CRDT-based synchronization** strategy between the frontend client, local database, and optional team collaboration hubs:

```
[Local React UI] <== (Zustand Event Bridge) ==> [Local SQLite DB]
                                                        |
                                          (Incremental Sync via WebSockets)
                                                        v
                                             [Team Cloud Sync Gateway]
                                                        |
                                            [Shared Postgres/Neo4j]
```

1. **Mutation Phase**: When a user changes a node on the Knowledge Graph, the frontend applies a local transaction and pushes it immediately into the local SQLite backend.
2. **Event Dispatch Phase**: The backend receives the transaction, posts a change notification to NATS, and updates the local Neo4j graph nodes.
3. **Async Processing**: A background agent listens to the NATS change event and starts research or risk assessment if necessary, pushing results back onto NATS, which streams to the frontend UI via WebSockets.
