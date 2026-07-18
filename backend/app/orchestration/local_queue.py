# backend/app/orchestration/local_queue.py
import asyncio
import json
import logging
import random
import uuid
from app.db.session import get_connection
from app.graph.client import graph_client
from app.agents.orchestrator import agent_orchestrator

logger = logging.getLogger("orchestrator_queue")

class LocalQueueWorker:
    def __init__(self):
        self._running = False
        self._loop_task = None

    def enqueue_job(self, event_type: str, payload: dict) -> str:
        job_id = f"job_{uuid.uuid4().hex[:10]}"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO event_queue (event_id, event_type, payload, status) VALUES (?, ?, ?, 'PENDING')",
            (job_id, event_type, json.dumps(payload))
        )
        conn.commit()
        conn.close()
        logger.info(f"Enqueued background job '{job_id}' of type '{event_type}'")
        return job_id

    async def start(self):
        self._running = True
        self._loop_task = asyncio.create_task(self._run_loop())
        logger.info("Local background queue worker started.")

    async def stop(self):
        self._running = False
        if self._loop_task:
            self._loop_task.cancel()
        logger.info("Local background queue worker stopped.")

    async def _run_loop(self):
        while self._running:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT event_id, event_type, payload FROM event_queue WHERE status = 'PENDING' LIMIT 1"
                )
                row = cursor.fetchone()
                
                if row:
                    job_id, event_type, payload_str = row
                    payload = json.loads(payload_str)
                    
                    # Lock job
                    cursor.execute(
                        "UPDATE event_queue SET status = 'PROCESSING' WHERE event_id = ?",
                        (job_id,)
                    )
                    conn.commit()
                    conn.close()
                    
                    # Execute task in background thread
                    asyncio.create_task(self._execute_job(job_id, event_type, payload))
                else:
                    conn.close()
                    
                await asyncio.sleep(2)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in background processing loop: {e}")
                await asyncio.sleep(5)

    async def _execute_job(self, job_id: str, event_type: str, payload: dict):
        logger.info(f"Executing background job {job_id} ({event_type})...")
        status = "COMPLETED"
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            project_id = payload.get("project_id")
            
            if event_type == "RESEARCH":
                # Simulates autonomous deep research
                await asyncio.sleep(3) # Heavy research delay simulation
                
                # Fetch multi-agent debate and scores
                debate = await agent_orchestrator.run_collaborative_debate(
                    payload.get("project_name", "New Project"),
                    payload.get("description", "")
                )
                
                # Dynamic score evaluation
                innov_score = round(random.uniform(0.65, 0.95), 2)
                monet_score = round(random.uniform(0.50, 0.90), 2)
                complexity = random.choice(["LOW", "MEDIUM", "HIGH"])
                
                # Update SQL tables
                cursor.execute(
                    """UPDATE projects SET 
                       innovation_score = ?, monetization_score = ?, complexity_level = ? 
                       WHERE id = ?""",
                    (innov_score, monet_score, complexity, project_id)
                )
                
                # Add nodes to GML Graph
                graph_client.add_node(f"concept_{project_id}", "Concept", {
                    "project_id": project_id,
                    "title": "Core Concept: " + payload.get("project_name"),
                    "summary": debate.get("research_summary")
                })
                graph_client.add_edge(project_id, f"concept_{project_id}", "HAS_CONCEPT")
                
                # Add competitor node
                comp_name = "Obsidian Clone"
                graph_client.add_node("competitor_node", "Company", {
                    "project_id": project_id,
                    "title": comp_name,
                    "description": "Indirect competitor in notes synthesis spaces"
                })
                graph_client.add_edge(f"concept_{project_id}", "competitor_node", "COMPETES_WITH")
                
                # Write debate results to Decision Ledger table
                ledger_id = f"dec_{uuid.uuid4().hex[:6]}"
                cursor.execute(
                    """INSERT INTO decision_ledger 
                       (id, project_id, decision_title, context, choice, rationale, alternatives) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        ledger_id, 
                        project_id, 
                        "Select License & Database", 
                        "Evaluating license compliance and offline constraints",
                        debate.get("target_license"),
                        "Debated and agreed: " + debate.get("database_layout"),
                        json.dumps(["GPL-3.0", "MIT", "PostgreSQL"])
                    )
                )
                conn.commit()
                
            elif event_type == "SIMULATE":
                await asyncio.sleep(2)
                # Parameters
                growth = payload.get("growth_rate", 0.1)
                churn = payload.get("churn_rate", 0.05)
                starting_capital = payload.get("capital", 5000.0)
                
                runs = []
                # Simple Monte Carlo simulation modeling capital trajectory over 12 months
                for month in range(1, 13):
                    growth_multiplier = (1 + growth) ** month
                    churn_loss = (1 - churn) ** month
                    # Simulated runs
                    median = starting_capital * growth_multiplier * churn_loss
                    low = median * random.uniform(0.75, 0.95)
                    high = median * random.uniform(1.05, 1.30)
                    
                    runs.append({
                        "month": month,
                        "lowOutcome": round(low, 2),
                        "medianOutcome": round(median, 2),
                        "highOutcome": round(high, 2)
                    })
                    
                # Cache results in SQL local key value store
                cursor.execute(
                    "INSERT OR REPLACE INTO local_kv_cache (cache_key, cache_value, expiration_timestamp) VALUES (?, ?, ?)",
                    (f"sim_{project_id}", json.dumps(runs), 9999999999)
                )
                conn.commit()
                
            elif event_type == "BUILD_CODE":
                await asyncio.sleep(4)
                # Scaffold simulated tasks in database
                tasks_data = [
                    ("Init virtualenv", "Setting up local python packages", "DONE"),
                    ("Design DB tables", "Creating projects, tasks SQL statements", "DONE"),
                    ("Write FastAPI main", "Adding GET, POST app routes", "IN_PROGRESS"),
                    ("Setup React Graph Component", "D3 force node UI widget", "TODO")
                ]
                
                for title, desc, t_status in tasks_data:
                    t_id = f"task_{uuid.uuid4().hex[:6]}"
                    cursor.execute(
                        """INSERT INTO tasks 
                           (id, project_id, title, description, status, priority, estimated_hours) 
                           VALUES (?, ?, ?, ?, ?, 'HIGH', 3.0)""",
                        (t_id, project_id, title, desc, t_status)
                    )
                    # Add task node to Graph
                    graph_client.add_node(t_id, "Task", {
                        "project_id": project_id,
                        "title": title,
                        "status": t_status
                    })
                    graph_client.add_edge(project_id, t_id, "HAS_TASK")
                conn.commit()

            conn.close()
        except Exception as e:
            logger.error(f"Failed job execution {job_id}: {e}")
            status = "FAILED"
            
        # Write back status
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE event_queue SET status = ? WHERE event_id = ?",
                (status, job_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to update job status: {e}")

# Global worker instance
worker = LocalQueueWorker()
