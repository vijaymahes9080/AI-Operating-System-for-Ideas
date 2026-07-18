# Project Folder Structure

IdeasOS is structured as a **monorepo** dividing backend, frontend, desktop packaging, configuration templates, and testing infrastructure.

---

## 1. Global Monorepo Layout

```
ideas-os/
├── .github/                  # CI/CD Workflows, release scripts, issue templates
├── backend/                  # FastAPI app & AI agent logic
├── frontend/                 # React SPA
├── src-tauri/                # Tauri Desktop packaging configuration (Rust)
├── shared/                   # Common JSON schemas, type definitions, and scripts
├── docs/                     # Architectural documents and design guides
├── scripts/                  # Dockerless dev setup & install utilities
├── package.json              # Monorepo root dependencies
└── README.md                 # Project introduction
```

---

## 2. In-Depth Subdirectory Tree

Below is the detailed file path mapping for developers.

### A. Backend Services (`backend/`)
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI server app setup & router mount
│   ├── config.py             # System environment variables and model paths
│   ├── db/                   # Database helpers & migrations
│   │   ├── session.py        # SQLAlchemy / Tortoise connection setup
│   │   └── migrations/       # Alembic/SQLite-migration scripts
│   ├── graph/                # Neo4j and NetworkX fallback client drivers
│   │   ├── client.py
│   │   └── queries.py        # Optimized Cypher queries
│   ├── agents/               # Multi-agent systems
│   │   ├── orchestrator.py   # LangGraph coordination node logic
│   │   ├── schemas.py        # Pydantic input/output schemas
│   │   └── roles/            # Specialized agent modules
│   │       ├── research.py
│   │       ├── architect.py
│   │       ├── planner.py
│   │       └── coder.py
│   ├── rag/                  # Retrieval Augmented Generation engine
│   │   ├── parser.py         # Multi-modal file reading (Tika, Whisper)
│   │   ├── chunker.py        # Parent-child chunking implementations
│   │   └── retriever.py      # Dense/sparse vector routing
│   └── orchestration/        # Long-running temporal workflows
│       ├── base.py
│       ├── temporal_wf.py    # Temporal SDK activity/workflow setups
│       └── local_queue.py    # Threaded fallback queue implementation
├── tests/                    # Backend Pytest suite
│   ├── conftest.py
│   ├── test_agents.py
│   └── test_rag.py
├── pyproject.toml            # uv / poetry backend dependency locks
└── README.md
```

### B. Frontend Client (`frontend/`)
```
frontend/
├── src/
│   ├── assets/               # Fonts, icons, static graphic vectors
│   ├── components/           # Reusable UI widgets
│   │   ├── ui/               # Base shadcn primitives (button, dialog, input)
│   │   ├── graph/            # Custom Graph visualization container
│   │   ├── terminal/         # Log viewer and chat component
│   │   └── simulator/        # ECharts based scenario planner dashboards
│   ├── hooks/                # Custom React hook utilities (useShortcut, useSync)
│   ├── layouts/              # Theme page frameworks (Sidebar, Dashboard Layout)
│   ├── pages/                # Workspace page controllers
│   │   ├── Inbox.tsx         # File ingestion landing zone
│   │   ├── GraphView.tsx     # Semantic Knowledge Graph
│   │   └── Planner.tsx       # Roadmap, task items, and milestones
│   ├── store/                # Zustand client state stores
│   │   ├── workspaceStore.ts
│   │   └── agentStore.ts
│   ├── utils/                # API Client wrappers & general utilities
│   ├── App.tsx               # Primary page routes
│   └── main.tsx              # React mounting entrypoint
├── public/                   # Public static folder
├── tailwind.config.js        # Design tokens and tailwind style setup
├── tsconfig.json             # TypeScript compiler settings
├── vite.config.ts            # Vite compile and local dev configuration
├── package.json              # Front-end dependencies (Zustand, Lucide, Recharts)
└── README.md
```

### C. Tauri Native Window Runtime (`src-tauri/`)
```
src-tauri/
├── src/
│   ├── cmd/                  # Rust command interfaces called by React
│   │   ├── file_system.rs    # Host OS directory manipulation commands
│   │   └── system_tray.rs    # Menus and window minimization hooks
│   └── main.rs               # Rust Tauri Application entrypoint
├── tauri.conf.json           # Window specs, permissions, bundles, build targets
├── Cargo.toml                # Rust dependencies (tauri, tokio, serde)
└── build.rs                  # Native application build scripts
```
