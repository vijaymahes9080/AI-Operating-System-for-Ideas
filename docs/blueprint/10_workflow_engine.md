# Workflow Engine & Event Orchestration

IdeasOS requires a robust orchestration engine to handle long-running, asynchronous tasks (e.g., scraping academic literature, scanning GitHub codebases, or compiling local prototypes). 

---

## 1. Dual Orchestration Strategy

To support the **Docker-Free** local desktop requirement while offering enterprise scalability, IdeasOS implements a unified execution interface with two target runtime strategies:

| Execution Mode | Runtime | Best For | Prerequisites |
|---|---|---|---|
| **Local Native (Default)** | Threaded In-Memory Event Scheduler (SQL-backed queue) | Lightweight local desktop runs. | None. Running native python loop. |
| **Enterprise Distributed** | **Temporal Server** + NATS messaging | Multi-user web setups, robust state replays. | Docker or native Temporal/NATS service binary running on host. |

Both runtimes implement the same abstract base class:

```python
# backend/app/orchestration/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class WorkflowOrchestrator(ABC):
    @abstractmethod
    def start_workflow(self, workflow_name: str, payload: Dict[str, Any]) -> str:
        """Starts a long running workflow task and returns execution ID."""
        pass

    @abstractmethod
    def get_status(self, execution_id: str) -> Dict[str, Any]:
        """Gets current state, logs, and outputs of the running workflow."""
        pass
```

---

## 2. Core Workflows & State Machines

Workflows are modeled as declarative State Machines. Below are the key workflows managed by the engine:

### A. Deep Research Workflow (`DeepResearchWorkflow`)
- **Step 1: Expand Query**: LLM expands raw search term into multiple query parameters (Scholar, Patents, Competitors).
- **Step 2: Scrape Scholars**: Runs parallel queries to Semantic Scholar and arXiv.
- **Step 3: Analyze Competitors**: Queries web search endpoints (Tavily/Serper).
- **Step 4: Vector Ingestion**: Downloads documents, extracts text, chunks them, and builds Qdrant/SQLite-vec indexes.
- **Step 5: Graph Link**: Links newly discovered papers to concepts in the database.

### B. Code Build & QA Workflow (`CodeBuildWorkflow`)
```
               [Start Build]
                     |
                     v
             [Scaffold Directories]
                     |
                     v
             [Generate Boileplate]
                     |
                     v
             [Execute Lint check]
             /                  \
         (Pass)                (Fail)
           /                      \
          v                        v
    [Inject Mock Data]      [Invoke Agent Refactor]
          |                        |
          v                        v
     [Run Pytest]         [Feed error logs back]
```

---

## 3. SQLite In-Memory Queue Implementation (Local Dev Fallback)

Below is the execution logic for the local python background runner:

```python
# backend/app/orchestration/local_runner.py
import asyncio
import uuid
import sqlite3
import json
from typing import Dict, Any
from .base import WorkflowOrchestrator

class LocalThreadedOrchestrator(WorkflowOrchestrator):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._loop_task = None
        self._running = False

    def start_workflow(self, workflow_name: str, payload: Dict[str, Any]) -> str:
        exec_id = f"wf_{uuid.uuid4().hex}"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO event_queue (event_id, event_type, payload, status) VALUES (?, ?, ?, 'PENDING')",
            (exec_id, workflow_name, json.dumps(payload))
        )
        conn.commit()
        conn.close()
        return exec_id

    def get_status(self, execution_id: str) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status, payload FROM event_queue WHERE event_id = ?", (execution_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return {"status": "UNKNOWN"}
        return {"status": row[0], "payload": json.loads(row[1])}

    async def start(self):
        self._running = True
        self._loop_task = asyncio.create_task(self._process_loop())

    async def stop(self):
        self._running = False
        if self._loop_task:
            self._loop_task.cancel()

    async def _process_loop(self):
        while self._running:
            # Poll pending jobs in SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT event_id, event_type, payload FROM event_queue WHERE status = 'PENDING' LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                event_id, w_type, payload_str = row
                # Lock row
                cursor.execute(
                    "UPDATE event_queue SET status = 'PROCESSING' WHERE event_id = ?", (event_id,)
                )
                conn.commit()
                conn.close()
                
                # Execute asynchronously
                asyncio.create_task(self._run_task(event_id, w_type, json.loads(payload_str)))
            else:
                conn.close()
                await asyncio.sleep(1)

    async def _run_task(self, event_id: str, w_type: str, payload: Dict[str, Any]):
        try:
            # Task routing logic based on w_type
            # Simulating execution:
            await asyncio.sleep(5) 
            status = 'COMPLETED'
        except Exception as e:
            status = 'FAILED'
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE event_queue SET status = ? WHERE event_id = ?", (status, event_id)
        )
        conn.commit()
        conn.close()
```
