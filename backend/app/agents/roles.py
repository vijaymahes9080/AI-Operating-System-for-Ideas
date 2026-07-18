# backend/app/agents/roles.py
from typing import Dict, Any

AGENT_SYSTEM_PROMPTS = {
    "researcher": (
        "You are the Lead Market Researcher and Academic Analyst.\n"
        "Your objective is to find real research papers, competitors, and potential "
        "licensing/technical gaps in a given project idea statement.\n"
        "Output citations, open-source alternatives, and potential risks.\n"
        "Format output as a structured JSON object."
    ),
    "architect": (
        "You are the Principal Systems Architect.\n"
        "Your objective is to design the relational database schema, database tables, "
        "microservices configuration, and deployment topology.\n"
        "Output visual database schema definitions, API paths, and scaling roadmaps.\n"
        "Format output as a structured JSON object."
    ),
    "planner": (
        "You are the Senior Product Manager & Agile Project Lead.\n"
        "Your objective is to decompose high-level requirements into epics, "
        "features, concrete task lists, subtask checklists, and time estimates.\n"
        "Format output as a structured JSON object."
    ),
    "coder": (
        "You are the Senior Coding Agent.\n"
        "Your objective is to write clean, modular, tested python files, API route handlers, "
        "and UI components.\n"
        "Format output as a structured JSON object."
    ),
    "business": (
        "You are the Startup Advisor and Financial Modeler.\n"
        "Your objective is to evaluate monetization plans, business models, "
        "and parameters for market Monte Carlo simulation runs (funding, client adoption, infra costs).\n"
        "Format output as a structured JSON object."
    )
}

# Pre-packaged mock data generators for instant out-of-the-box runs
MOCK_RESPONSES = {
    "researcher": {
        "summary": "This idea represents a novel approach to local-first cognitive systems. Major gaps identified include encryption mechanics and edge-based sync latency.",
        "citations": [
            "Llama 3: Open Foundation Models, Meta AI (2024)",
            "Local-First Software: You own your data, Kleppmann et al. (2019)"
        ],
        "competitors": [
            {"name": "Obsidian", "url": "https://obsidian.md", "weakness": "Passive storage, lacks agent workflows"},
            {"name": "Linear", "url": "https://linear.app", "weakness": "Excellent planner, but doesn't write code"}
        ],
        "suggested_license": "Apache-2.0",
        "required_skills": ["Python FastAPI", "React Native", "LiteLLM"]
    },
    "architect": {
        "database_type": "SQLite / PostgreSQL",
        "schema_diagram": (
            "CREATE TABLE projects (id TEXT PRIMARY KEY, name TEXT, dna_hash TEXT);\n"
            "CREATE TABLE tasks (id TEXT PRIMARY KEY, project_id TEXT, title TEXT, status TEXT);"
        ),
        "endpoints": [
            {"path": "/api/v1/inbox/ingest", "method": "POST", "auth": "OAuth2"},
            {"path": "/api/v1/graph/subgraph", "method": "GET", "auth": "OAuth2"}
        ],
        "scaling_strategy": "Migrate SQLite to AWS Aurora PostgreSQL and use Qdrant clusters for vector storage."
    },
    "planner": {
        "epics": ["Scaffold Repository", "Implement Database", "Connect AI agents"],
        "tasks": [
            {"title": "Initialize python virtual environment", "estimated_hours": 1.0, "priority": "HIGH"},
            {"title": "Configure SQLite-vec vector connection", "estimated_hours": 3.0, "priority": "HIGH"},
            {"title": "Build WebSocket agent stream API", "estimated_hours": 4.5, "priority": "MEDIUM"}
        ]
    },
    "business": {
        "monetization": "SaaS hosting subscription starting at $15/month, combined with self-hosted custom licenses.",
        "simulation_parameters": {
            "monthly_user_growth": 0.15,
            "monthly_churn_rate": 0.05,
            "infrastructure_cost_per_user": 0.12,
            "starting_capital": 10000.0
        }
    }
}
