# backend/app/main.py
import os
import uuid
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from app.config import settings
from app.db.session import init_db, get_connection
from app.graph.client import graph_client
from app.orchestration.local_queue import worker

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Setup database tables and run migration verification
    init_db()
    # Launch background worker
    await worker.start()
    yield
    # Shutdown: Stop workers cleanly
    await worker.stop()

app = FastAPI(
    title=settings.APP_NAME,
    description="The Open Source Operating System for Ideas (IdeaOS) Core APIs",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local Vite frontends and Tauri wrappers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow direct local desktop connection
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class ProjectCreate(BaseModel):
    name: str
    description: str

class SimulationTrigger(BaseModel):
    growth_rate: float = 0.15
    churn_rate: float = 0.05
    capital: float = 10000.0

# HTTP Endpoint Implementations

@app.get("/api/v1/health")
def health_check():
    return {"status": "ONLINE", "profile": settings.ENV, "database": settings.DATABASE_URL}

@app.post("/api/v1/inbox/ingest")
async def ingest_inbox(
    title: str = Form(...),
    content: str = Form(...),
    source_type: str = Form("TEXT")
):
    try:
        inb_id = f"inb_{uuid.uuid4().hex[:6]}"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO raw_inbox (id, workspace_id, title, content, source_type) VALUES (?, 'default', ?, ?, ?)",
            (inb_id, title, content, source_type)
        )
        conn.commit()
        conn.close()
        
        # Automatically spawn background processing of this raw inbox node
        logger.info(f"Ingested raw input item {inb_id}: {title}")
        return {"inbox_id": inb_id, "status": "QUEUED", "message": "Structured input saved."}
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/projects")
def list_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/v1/projects")
def create_project(data: ProjectCreate):
    try:
        project_id = f"proj_{uuid.uuid4().hex[:6]}"
        dna_hash = f"dna_{uuid.uuid4().hex[:10]}"
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO projects 
               (id, workspace_id, name, description, dna_hash) 
               VALUES (?, 'default', ?, ?, ?)""",
            (project_id, data.name, data.description, dna_hash)
        )
        conn.commit()
        conn.close()
        
        # 1. Insert Base Node in Knowledge Graph
        graph_client.add_node(project_id, "Project", {
            "title": data.name,
            "description": data.description,
            "dna_hash": dna_hash,
            "project_id": project_id
        })
        
        # 2. Dispatch background RAG, analysis, and task-generation routines
        worker.enqueue_job("RESEARCH", {
            "project_id": project_id,
            "project_name": data.name,
            "description": data.description
        })
        
        worker.enqueue_job("BUILD_CODE", {
            "project_id": project_id
        })
        
        return {"project_id": project_id, "dna_hash": dna_hash, "status": "QUEUED"}
    except Exception as e:
        logger.error(f"Project creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/project/{project_id}")
def get_project_details(project_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return dict(row)

@app.get("/api/v1/project/{project_id}/graph")
def get_project_graph(project_id: str):
    # Returns structural layout mapping
    return graph_client.get_project_subgraph(project_id)

@app.get("/api/v1/project/{project_id}/tasks")
def get_project_tasks(project_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/v1/project/{project_id}/decisions")
def get_project_decisions(project_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM decision_ledger WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/v1/project/{project_id}/simulate")
def run_simulation(project_id: str, data: SimulationTrigger):
    job_id = worker.enqueue_job("SIMULATE", {
        "project_id": project_id,
        "growth_rate": data.growth_rate,
        "churn_rate": data.churn_rate,
        "capital": data.capital
    })
    return {"job_id": job_id, "status": "QUEUED"}

@app.get("/api/v1/project/{project_id}/simulation-results")
def get_simulation_results(project_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cache_value FROM local_kv_cache WHERE cache_key = ?", (f"sim_{project_id}",))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return []
    return json.loads(row[0])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
