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

# General mock responses fallback
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

# Rich custom innovation templates for the Inspiration Lab
DYNAMIC_MOCK_RESPONSES = {
    "biomemory": {
        "researcher": {
            "summary": "Feasibility confirmed. DNA storage density allows 215 PB/gram. Key constraints include chemical synthesis throughput and read/write latencies.",
            "citations": [
                "DNA Data Storage: Progress and Challenges, Organick et al. (2018)",
                "Next-Gen Nucleotide Encoding Schemes, Goldman et al. (2013)"
            ],
            "competitors": [
                {"name": "Catalog DNA", "url": "https://catalogdna.com", "weakness": "High cost, non-local-first processing"}
            ],
            "suggested_license": "CERN-OHL-W-2.0",
            "required_skills": ["Python", "BioPython", "Basecalling Algorithms"]
        },
        "architect": {
            "database_type": "PostgreSQL + pgvector & binary sequence store",
            "schema_diagram": (
                "CREATE TABLE dna_codons (id UUID PRIMARY KEY, sequence TEXT, quality_score REAL);\n"
                "CREATE TABLE reads (id UUID PRIMARY KEY, codon_id REFERENCES dna_codons(id), payload BYTEA);"
            ),
            "endpoints": [
                {"path": "/api/v1/dna/encode", "method": "POST", "auth": "Bearer Token"},
                {"path": "/api/v1/dna/decode", "method": "POST", "auth": "Bearer Token"}
            ],
            "scaling_strategy": "Distribute codon decoding across CUDA-accelerated edge GPU nodes."
        },
        "planner": {
            "epics": ["Sequence Design", "Codec Encoding Algorithm", "Physical Synthesis Simulator"],
            "tasks": [
                {"title": "Implement Huffman coding for base4 conversion", "estimated_hours": 4.0, "priority": "HIGH"},
                {"title": "Add Reed-Solomon error correction module", "estimated_hours": 6.5, "priority": "HIGH"},
                {"title": "Simulate sequencing noise models", "estimated_hours": 3.0, "priority": "MEDIUM"}
            ]
        },
        "business": {
            "monetization": "Enterprise cold-storage archival service at $0.05 per Terabyte per month, with hardware compiler licensing.",
            "simulation_parameters": {
                "monthly_user_growth": 0.25,
                "monthly_churn_rate": 0.02,
                "infrastructure_cost_per_user": 2.50,
                "starting_capital": 35000.0
            }
        }
    },
    "ecomesh": {
        "researcher": {
            "summary": "Validates mesh topology using LoRaWAN protocols. Solves sensor telemetry drops in dense forest canopies using dynamic route optimization based on solar panel charging rates.",
            "citations": [
                "Ad-hoc Mesh Networking for Environmental Sensing, Hart et al. (2015)",
                "Solar Harvesting Logic for Low-Power IoT, Kansal et al. (2007)"
            ],
            "competitors": [
                {"name": "Helium Network", "url": "https://helium.com", "weakness": "Requires crypto tokenomics, unreliable local routing latency"}
            ],
            "suggested_license": "GPL-3.0-only",
            "required_skills": ["Embedded C++", "LoRaWAN", "Networkx routing"]
        },
        "architect": {
            "database_type": "SQLite with SpatiaLite extension",
            "schema_diagram": (
                "CREATE TABLE sensors (id TEXT PRIMARY KEY, lat REAL, lng REAL, battery REAL);\n"
                "CREATE TABLE mesh_edges (source TEXT, target TEXT, quality REAL);"
            ),
            "endpoints": [
                {"path": "/api/v1/mesh/telemetry", "method": "POST", "auth": "MeshSecret"},
                {"path": "/api/v1/mesh/routes", "method": "GET", "auth": "OAuth2"}
            ],
            "scaling_strategy": "Use regional broker gateways with MQTT clustering to scale to 10k nodes."
        },
        "planner": {
            "epics": ["Firmware Base", "Dijkstra Charging Route Engine", "Gateway MQTT Integration"],
            "tasks": [
                {"title": "Implement solar state telemetry parsing", "estimated_hours": 2.0, "priority": "HIGH"},
                {"title": "Create adaptive battery-aware routing algorithm", "estimated_hours": 5.0, "priority": "HIGH"},
                {"title": "Test message forwarding under packet loss simulator", "estimated_hours": 4.0, "priority": "MEDIUM"}
            ]
        },
        "business": {
            "monetization": "B2B telemetry dashboard subscription ($50/sensor group/month) and enterprise deployment consulting.",
            "simulation_parameters": {
                "monthly_user_growth": 0.12,
                "monthly_churn_rate": 0.04,
                "infrastructure_cost_per_user": 0.08,
                "starting_capital": 15000.0
            }
        }
    },
    "patent": {
        "researcher": {
            "summary": "Automates USPTO documentation drafts using semantic RAG parsing. Resolves legal compliance issues by generating verifiable IP logs on-chain before public disclosure.",
            "citations": [
                "AI in Intellectual Property Law, Abbott et al. (2019)",
                "Decentralized Registries for Scientific Claims, DeSci Wiki (2023)"
            ],
            "competitors": [
                {"name": "IP.com", "url": "https://ip.com", "weakness": "High proprietary fees, lacks automatic drafting engines"}
            ],
            "suggested_license": "MIT",
            "required_skills": ["Solidity", "Tauri/Rust", "RAG Prompt Engineering"]
        },
        "architect": {
            "database_type": "SQLite with SQLite-vec & IPFS hash mappings",
            "schema_diagram": (
                "CREATE TABLE patent_drafts (id TEXT PRIMARY KEY, claims_json TEXT, ipfs_hash TEXT);\n"
                "CREATE TABLE notary_logs (id TEXT PRIMARY KEY, tx_hash TEXT, status TEXT);"
            ),
            "endpoints": [
                {"path": "/api/v1/patent/draft", "method": "POST", "auth": "OAuth2"},
                {"path": "/api/v1/patent/notarize", "method": "POST", "auth": "OAuth2"}
            ],
            "scaling_strategy": "Store raw PDFs on decentralized IPFS/Arweave and commit root state hashes to Arbitrum L2."
        },
        "planner": {
            "epics": ["RAG Patent Parser", "Arbitrum Notary Bridge", "Export PDF Suite"],
            "tasks": [
                {"title": "Design patent-claims structure prompt schema", "estimated_hours": 3.0, "priority": "HIGH"},
                {"title": "Write smart contract for state hash notary", "estimated_hours": 6.0, "priority": "HIGH"},
                {"title": "Integrate PDF generation library for USPTO formatting", "estimated_hours": 4.0, "priority": "MEDIUM"}
            ]
        },
        "business": {
            "monetization": "Pay-per-notarization ($19/draft) or annual patent portfolio management subscription starting at $99/month.",
            "simulation_parameters": {
                "monthly_user_growth": 0.18,
                "monthly_churn_rate": 0.03,
                "infrastructure_cost_per_user": 0.45,
                "starting_capital": 25000.0
            }
        }
    },
    "holographic": {
        "researcher": {
            "summary": "Spatial optimization system. Translates ergonomic specifications into parametric mesh representations using constrained geometry resolvers.",
            "citations": [
                "Parametric Layout Planning in Virtual Environments, Smith et al. (2021)",
                "Ergonomic Guidelines for Computer Workstations, OSHA Standards (2019)"
            ],
            "competitors": [
                {"name": "Planner 5D", "url": "https://planner5d.com", "weakness": "Purely manual editor, no AI-driven cognitive constraint mapping"}
            ],
            "suggested_license": "Apache-2.0",
            "required_skills": ["Three.js / WebGL", "Python optimization libraries", "Vector Math"]
        },
        "architect": {
            "database_type": "PostgreSQL with spatial extensions",
            "schema_diagram": (
                "CREATE TABLE rooms (id TEXT PRIMARY KEY, bounds_json TEXT);\n"
                "CREATE TABLE furniture_items (id TEXT PRIMARY KEY, room_id TEXT, mesh_gltf_url TEXT, transform_matrix TEXT);"
            ),
            "endpoints": [
                {"path": "/api/v1/layout/optimize", "method": "POST", "auth": "OAuth2"},
                {"path": "/api/v1/layout/gltf", "method": "GET", "auth": "OpenAccess"}
            ],
            "scaling_strategy": "Pre-render layout configurations as GLTF previews on CDN caches; run optimizer async on cloud workers."
        },
        "planner": {
            "epics": ["Layout Solver Engine", "Three.js Workspace Canvas", "Furniture Library Seed"],
            "tasks": [
                {"title": "Build boundary constraint collision resolver", "estimated_hours": 5.0, "priority": "HIGH"},
                {"title": "Set up React Three Fiber scene loader", "estimated_hours": 4.0, "priority": "HIGH"},
                {"title": "Define standard ergonomic parameter checks", "estimated_hours": 3.0, "priority": "MEDIUM"}
            ]
        },
        "business": {
            "monetization": "Freemium design access; pro licenses at $29/month for furniture retail integrations and commercial export features.",
            "simulation_parameters": {
                "monthly_user_growth": 0.20,
                "monthly_churn_rate": 0.06,
                "infrastructure_cost_per_user": 0.15,
                "starting_capital": 12000.0
            }
        }
    }
}

def get_mock_response(role: str, context_prompt: str) -> dict:
    """Detects matching project concepts in prompt text and returns tailored response, or falls back to general mock."""
    prompt_lower = context_prompt.lower()
    
    # 1. Determine key
    key = None
    if "biomemory" in prompt_lower or "dna" in prompt_lower or "lattice" in prompt_lower:
        key = "biomemory"
    elif "ecomesh" in prompt_lower or "mesh" in prompt_lower or "solar" in prompt_lower:
        key = "ecomesh"
    elif "patent" in prompt_lower or "ip-graph" in prompt_lower or "notary" in prompt_lower:
        key = "patent"
    elif "holographic" in prompt_lower or "room" in prompt_lower or "furniture" in prompt_lower:
        key = "holographic"
        
    # 2. Get value
    if key and key in DYNAMIC_MOCK_RESPONSES:
        role_mocks = DYNAMIC_MOCK_RESPONSES[key]
        if role in role_mocks:
            return role_mocks[role]
            
    # Fallback to general responses
    return MOCK_RESPONSES.get(role, {"message": "Empty response"})
