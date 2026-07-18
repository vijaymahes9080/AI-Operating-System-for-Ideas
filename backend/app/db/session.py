# backend/app/db/session.py
import sqlite3
import json
import logging
from app.config import settings

logger = logging.getLogger("db")

def get_connection():
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    # Enable WAL mode for concurrent execution
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    logger.info("Initializing SQLite relational tables...")
    
    # 1. Workspaces
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workspaces (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        settings_json TEXT DEFAULT '{}'
    );
    """)
    
    # Seed default workspace if not present
    cursor.execute("SELECT id FROM workspaces WHERE id = 'default'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO workspaces (id, name) VALUES ('default', 'Default Space')")
    
    # 2. Projects
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        workspace_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        dna_hash TEXT,
        innovation_score REAL DEFAULT 0.0,
        monetization_score REAL DEFAULT 0.0,
        complexity_level TEXT DEFAULT 'MEDIUM',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE
    );
    """)
    
    # 3. Raw Inbox
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_inbox (
        id TEXT PRIMARY KEY,
        workspace_id TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        source_type TEXT CHECK(source_type IN ('TEXT', 'VOICE', 'IMAGE', 'PDF', 'WEBSITE', 'GITHUB')) DEFAULT 'TEXT',
        processed BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE
    );
    """)
    
    # 4. Tasks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        parent_id TEXT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK(status IN ('BACKLOG', 'TODO', 'IN_PROGRESS', 'REVIEW', 'DONE')) DEFAULT 'BACKLOG',
        priority TEXT CHECK(priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')) DEFAULT 'MEDIUM',
        assignee TEXT DEFAULT 'UNASSIGNED',
        estimated_hours REAL DEFAULT 0.0,
        actual_hours REAL DEFAULT 0.0,
        dependencies TEXT DEFAULT '[]', -- JSON array of task IDs
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY(parent_id) REFERENCES tasks(id) ON DELETE SET NULL
    );
    """)
    
    # 5. Decision Ledger
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decision_ledger (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        decision_title TEXT NOT NULL,
        context TEXT NOT NULL,
        choice TEXT NOT NULL,
        rationale TEXT NOT NULL,
        alternatives TEXT DEFAULT '[]', -- JSON stringified array
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """)
    
    # 6. Event/Job Queue
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS event_queue (
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL, -- e.g., 'RESEARCH', 'SIMULATE', 'BUILD_CODE'
        payload TEXT NOT NULL, -- JSON payload
        status TEXT CHECK(status IN ('PENDING', 'PROCESSING', 'FAILED', 'COMPLETED')) DEFAULT 'PENDING',
        retry_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 7. Local Key-Value cache & Vector mock index
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS local_kv_cache (
        cache_key TEXT PRIMARY KEY,
        cache_value TEXT NOT NULL,
        expiration_timestamp INTEGER NOT NULL
    );
    """)
    
    # Vector simulation table (sparse/dense storage search fallback)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vector_index_fallback (
        chunk_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        content TEXT NOT NULL,
        embedding_json TEXT, -- JSON Float List
        source_metadata TEXT DEFAULT '{}',
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()
    logger.info("Relational database initial structures verified.")
