# IdeaOS: The Operating System for Ideas

IdeaOS is a startup-grade, open-source, local-first platform designed to transform raw ideas (text inputs, voice notes, PDFs, codebases) into structured execution environments containing interactive Knowledge Graphs, Relational Database specs, PM checklists, and Monte Carlo simulator metrics.

The system runs entirely locally, requiring **No Docker dependency** and **No proprietary cloud API keys**.

---

## 🗺️ Project Architecture Topology

```
                  [ IdeaOS Web/Desktop Client ]
                                |
                   (HTTP REST / WebSockets API)
                                |
                  [ FastAPI Local API Server ]
                                |
         +----------------------+----------------------+
         |                      |                      |
     [ SQLite ]            [ NetworkX ]          [ LiteLLM / ]
   - Project Metadata     - Knowledge Graph     - Ollama Local
   - Action Tasks         - GML Local Sync      - Mock Agents
   - Event Queues
```

- **Frontend**: React TS, Tailwind CSS (glassmorphic Cyber-Glass framework), Zustand state-routing.
- **Backend**: Python 3.11+, FastAPI web host, networkx graph parser, LiteLLM completion router.
- **Database**: SQLite with Write-Ahead Logging (WAL) enabled.

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** v18+ and **npm**
- **Python** v3.11+

### 1. Installation Setup
Execute the bootstrap script corresponding to your operating system to automatically install packages and initialize database folders:

**Windows (PowerShell):**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Unix / macOS (Terminal):**
```bash
chmod +x scripts/setup.sh scripts/dev.sh
./scripts/setup.sh
```

### 2. Run Dev Servers
Launch the FastAPI backend server (port `8000`) and the Vite React server (port `5173`) in parallel:

**Windows:**
```powershell
.\scripts\dev.ps1
```

**Unix / macOS:**
```bash
./scripts/dev.sh
```

Navigate to **`http://localhost:5173`** in your browser to open the IdeaOS client shell.

---

## ⚡ Core Command Shortcuts

The bottom dock contains a quick-entry command prompt:
- **`[Input text name]` + Enter**: Creates a new project workspace and triggers agent analysis.
- **`/idea [content]`**: Adds a new raw text node directly to the universal inbox tracker.
- **`Alt+Enter`**: Instantly submits commands to the background cognitive coordinator.

---

## 💡 Inspiration Lab

To showcase the capabilities of the local multi-agent research, planning, and simulation pipelines, we have pre-packaged four dynamic innovation templates in the sidebar **Inspiration Lab**:
1. **🧬 BioMemory Lattice**: Translates structured journal files into DNA-sequence base codings (A, T, C, G) for synthetic nucleotide storage.
2. **☀️ EcoMesh Swarm Router**: An adaptive IoT mesh network that coordinates battery/solar levels of environmental sensors.
3. **📜 Patent IP-Graph**: Auto-drafts USPTO compliance details from voice/text notes and notarizes state-hashes on L2/EVM testnets.
4. **📐 Holographic Room Planner**: Parametric Three.js layout generator optimizing spatial and ergonomic boundaries.

When seeded, the cognitive agents (Researcher, Architect, Planner, and Business Advisor) automatically mock detailed technical architectures, database schemas, prioritized epic checklists, and financial Monte Carlo simulations customized for that specific domain.

