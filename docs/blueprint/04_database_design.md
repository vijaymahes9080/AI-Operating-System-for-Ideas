# Database Design & Relational Schema

IdeasOS uses SQLite as the default embedded local-first storage engine (using WAL mode for concurrent access) and supports PostgreSQL for multi-tenant and enterprise cloud deployments.

---

## 1. Entity Relationship (ER) Diagram

```
+------------------+         +------------------+         +------------------+
|    WORKSPACES    |         |     PROJECTS     |         |     RAW_INBOX    |
|------------------|         |------------------|         |------------------|
| id (PK)          |         | id (PK)          |         | id (PK)          |
| name             |<------- | workspace_id(FK) |<------- | workspace_id(FK) |
| created_at       |         | name             |         | title            |
| settings_json    |         | description      |         | content          |
+------------------+         | dna_hash         |         | source_type      |
                             | created_at       |         | raw_metadata     |
                             +--------+---------+         +------------------+
                                      |
                                      | 1
                                      |
                                      | N
                             +--------v---------+         +------------------+
                             |  TASKS / ISSUES  |         | DECISION_LEDGER  |
                             |------------------|         |------------------|
                             | id (PK)          |         | id (PK)          |
                             | project_id (FK)  |         | project_id (FK)  |<--+
                             | parent_id (FK)   |<--------| decision_title   |   |
                             | title            |         | context          |   |
                             | status           |         | choice           |   |
                             | priority         |         | rationale        |   |
                             | assignee         |         | alternatives     |   |
                             | estimated_hours  |         +------------------+   |
                             +------------------+                                |
                                                                                 |
                             +------------------+                                |
                             |   SIMULATIONS    |                                |
                             |------------------|                                |
                             | id (PK)          |--------------------------------+
                             | project_id (FK)  |
                             | sim_type         |
                             | input_parameters |
                             | simulation_runs  |
                             +------------------+
```

---

## 2. Core Table Schemas (SQL DDL)

Below are the production-grade DDL definitions for the local SQLite implementation:

### Workspaces Table
```sql
CREATE TABLE workspaces (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    settings_json TEXT DEFAULT '{}'
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    dna_hash TEXT UNIQUE,
    innovation_score REAL DEFAULT 0.0,
    monetization_score REAL DEFAULT 0.0,
    complexity_level TEXT CHECK(complexity_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    state_timeline TEXT DEFAULT '[]', -- JSON event log of states
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE
);
```

### Raw Inbox Table
```sql
CREATE TABLE raw_inbox (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_type TEXT CHECK(source_type IN ('TEXT', 'VOICE', 'IMAGE', 'PDF', 'WEBSITE', 'GITHUB', 'MEETING')),
    file_path TEXT,
    raw_metadata TEXT DEFAULT '{}', -- JSON for arbitrary extra info
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    parent_id TEXT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('BACKLOG', 'TODO', 'IN_PROGRESS', 'REVIEW', 'DONE')) DEFAULT 'BACKLOG',
    priority TEXT CHECK(priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')) DEFAULT 'MEDIUM',
    assignee TEXT DEFAULT 'UNASSIGNED', -- AI Agent ID or User Name
    estimated_hours REAL,
    actual_hours REAL DEFAULT 0.0,
    dependencies TEXT DEFAULT '[]', -- JSON array of task IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY(parent_id) REFERENCES tasks(id) ON DELETE SET NULL
);
```

### Decision Ledger Table
```sql
CREATE TABLE decision_ledger (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    decision_title TEXT NOT NULL,
    context TEXT NOT NULL,
    choice TEXT NOT NULL,
    rationale TEXT NOT NULL,
    alternatives TEXT DEFAULT '[]', -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

### Cache & Queue Tables
For offline-first orchestration without heavy external services, SQLite acts as an event store and metadata cache.

```sql
CREATE TABLE local_kv_cache (
    cache_key TEXT PRIMARY KEY,
    cache_value TEXT NOT NULL,
    expiration_timestamp INTEGER NOT NULL
);

CREATE TABLE event_queue (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT CHECK(status IN ('PENDING', 'PROCESSING', 'FAILED', 'COMPLETED')) DEFAULT 'PENDING',
    retry_count INTEGER DEFAULT 0,
    locked_until INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. Migration and DB Hook Pattern

The FastAPI backend uses **Alembic** (or a built-in sqlite-migration loop) to automatically verify and execute schema migrations on boot:

```python
# backend/app/db/migrations.py
import sqlite3
import logging

logger = logging.getLogger("db")

def run_migrations(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Initialize schema version table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
    """)
    
    # Check current version
    cursor.execute("SELECT version FROM schema_version")
    row = cursor.fetchone()
    current_version = row[0] if row else 0
    
    # Step-by-step migrations
    if current_version < 1:
        logger.info("Applying migration v1 (Init Tables)...")
        # SQL Statements here...
        cursor.execute("INSERT OR REPLACE INTO schema_version (version) VALUES (1)")
        conn.commit()
        
    conn.close()
```
