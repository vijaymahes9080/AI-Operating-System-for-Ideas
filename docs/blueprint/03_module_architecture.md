# Module Architecture & Core Engines

This document specifies the internal architectures, class relationships, and processing engines for each of the 13 Core Modules and the Exclusive Innovative Features of IdeasOS.

---

## 1. The 13 Core Modules

### 1. Universal Idea Inbox
- **Purpose**: Consumes raw inputs in any medium and structures them into unified raw cognitive nodes.
- **Components**:
  - `IngestionPipeline`: Orchestrates file routing based on MIME type.
  - `SpeechProcessor`: Transcribes voice and audio using local Whisper.
  - `DocumentParser`: Extracts text from PDFs/Research papers via Apache Tika/Unstructured.
  - `ImageProcessor`: Extracts wireframe nodes or drawings using OpenCLIP and SAM.
  - `IntegrationConnectors`: Polls Slack, Discord, and WhatsApp export formats.
- **Output Formats**: A structured JSON payload conforming to `RawInputSchema` containing raw markdown, extracted metadata, and embedded media assets.

### 2. Idea Intelligence Engine
- **Purpose**: Conducts the primary static analysis of the ingested idea.
- **Components**:
  - `CognitiveEvaluator`: Classifies targets (Goals, Problems, Tech stack).
  - `ScoringEngine`: Analyzes innovation level, startup potential, monetization options, and social impact scores.
  - `ComplexityPredictor`: Estimates required developer hours, skill list, and risk scores.
- **Logic Flow**:
```
Raw Input JSON ---> [CognitiveEvaluator] ---> [ScoringEngine] ---> Meta Report + DNA
```

### 3. Autonomous Deep Research Engine
- **Purpose**: Performs real-time parallel information gathering.
- **Components**:
  - `LiteratureScraper`: Searches arXiv, Semantic Scholar, and Google Scholar.
  - `MarketAnalyst`: Scrapes competitor lists, open-source repositories, and pricing sheets.
  - `PatentExplorer`: Hits USPTO and EPO data pools.
  - `CitationTracker`: Resolves sources, checks licensing, and compiles bibliography structures.

### 4. Knowledge Graph Engine
- **Purpose**: Builds and traverses semantic associations across projects.
- **Components**:
  - `GraphLinker`: Auto-detects relations between new inputs and old records.
  - `CypherQueryGenerator`: Converts natural language search queries to Neo4j Cypher.
  - `VectorGraphRetriever`: Performs hybrid graph-vector lookups (Subgraphs + Semantic Embeddings).

### 5. AI Architect
- **Purpose**: Designs application architecture, databases, and deployment schemas.
- **Components**:
  - `SchemaDesigner`: Outputs complete SQL, Cypher, and Prisma database structures.
  - `ServicePlanner`: Outlines Monolith vs. Microservice topologies.
  - `InfrastructureArchitect`: Outputs Terraform scripts, local script configs, and API boundary definitions.

### 6. Product Planner
- **Purpose**: Generates functional documents (PRD, SRS, BRD, User Stories).
- **Components**:
  - `DocumentSynthesizer`: Templates documents and generates business plans.
  - `UserStoryGenerator`: Maps feature requirements to user stories and acceptance criteria.
  - `RevenueCalculator`: Formulates pricing plans and go-to-market roadmaps.

### 7. Roadmap Generator
- **Purpose**: Converts user stories and system dependencies into scheduling timelines.
- **Components**:
  - `CriticalPathFinder`: Evaluates task graphs to compute project bottle-necks.
  - `TimelineScheduler`: Maps tasks to daily, weekly, sprint, and quarterly charts.
  - `RiskAligner`: Highlights milestones with high-probability failure paths.

### 8. Task Intelligence
- **Purpose**: Populates the workspace with active issues.
- **Components**:
  - `DecompositionEngine`: Breaks down large Epics into subtasks and checklist items.
  - `CommitMapper`: Creates developer instructions and suggests git commit statements.
  - `AutomationManager`: Highlights tasks that can be fully automated by AI coding agents.

### 9. AI Pair Programmer
- **Purpose**: Code generation workspace.
- **Components**:
  - `BoilerplateGenerator`: Scaffolds backend/frontend skeletons based on the AI Architect specs.
  - `AgenticCoder`: Writes React components, endpoints, database migrations, and schema changes.
  - `RefactoringEngine`: Fixes linting errors, restructures logic, and matches style guidelines.

### 10. Prototype Generator
- **Purpose**: Renders interactive local previews.
- **Components**:
  - `UIWireframer`: Converts layout specs into pure Tailwind + React code.
  - `MockDataGenerator`: Fills databases and components with rich placeholder records.
  - `ComponentPreviewServer`: Runs a local sandboxed dev server to host mock pages.

### 11. Testing Intelligence
- **Purpose**: Validates outputs and prevents regression.
- **Components**:
  - `TestGenerator`: Writes unit (pytest), integration, and UI tests (Playwright).
  - `LoadStressSimulator`: Writes scripts for performance, stress, and security audit tests.
  - `BugPredictor`: Scans static code to identify probable security flaws and logic bugs.

### 12. Launch Manager
- **Purpose**: Final assets and marketing deployment.
- **Components**:
  - `AssetGenerator`: Generates landing pages, SEO, pitch decks, and release notes.
  - `MediaCreator`: Generates blog posts, emails, and social media copy.
  - `DeploymentOrchestrator`: Verifies deployment checklist state.

### 13. Continuous Evolution Engine
- **Purpose**: Monitors production runtime and provides live iteration suggestions.
- **Components**:
  - `FeedbackAnalyzer`: Analyzes logs, errors, user feedback, and usage metrics.
  - `DebtOptimizer`: Detects technical debt and generates structural improvement suggestions.

---

## 2. Exclusive Innovative Features

```
+-----------------------------------------------------------------------------+
|                          COGNITIVE ADVANCED SUITE                           |
|                                                                             |
|  +--------------------+  +--------------------+  +-----------------------+  |
|  |     IDEA DNA       |  |  DECISION LEDGER   |  |   SCENARIO SIMULATOR  |  |
|  |  Origin, evolution |  | Immutable log of   |  | Monte Carlo modeling  |  |
|  |  innovation metrics|  | design choices     |  | of success/failure    |  |
|  +--------------------+  +--------------------+  +-----------------------+  |
|                                                                             |
|  +--------------------+  +--------------------+  +-----------------------+  |
|  |   AI DEBATE ROOM   |  |    RISK RADAR      |  |     DIGITAL TWIN      |  |
|  | Multi-agent debate |  | Real-time threat   |  | Predictive project    |  |
|  | on architecture    |  | scoring & analysis |  | forecasting model     |  |
|  +--------------------+  +--------------------+  +-----------------------+  |
+-----------------------------------------------------------------------------+
```

### Idea DNA (`docs/blueprint/03_module_architecture.md#idea-dna`)
- **Execution Class**: `IdeaDNATracker`
- **Data Saved**: Generates a composite hash tracking the originality index, system evolution path, lineage connections to parent ideas, and technology footprint.
- **Visualization**: An interactive tree displaying project mutations, branches, and code additions over time.

### Idea Time Machine (`docs/blueprint/03_module_architecture.md#idea-time-machine`)
- **Execution Class**: `ProjectTimelineReplayer`
- **Mechanism**: Maintains a chronological event log in SQLite. Allows the developer to "rewind" the workspace to any point in history, restoring the state of the Knowledge Graph, the code directory, the tasks list, and the active LLM context.

### Scenario Simulator
- **Execution Class**: `MarketMonteCarloSimulator`
- **Mechanism**: Simulates business and technical trajectories. Simulates variables like cloud resource costs, user registration rates, funding milestones, API outage scenarios, and technical debt accumulation over a 12-month period, generating confidence graphs.

### AI Debate Room
- **Execution Class**: `MultiAgentDebateChamber`
- **Mechanism**: Spins up a panel of specialized agent personas (e.g., Senior Architect, Product Manager, Security Specialist, Financial Analyst) to critique proposals. Output includes an architecture/business assessment report outlining pros, cons, and alternatives.

### Decision Ledger
- **Execution Class**: `DecisionLedgerManager`
- **Mechanism**: Records critical architecture, business, or task decisions. Each ledger entry includes:
  - Context & Alternatives Evaluated.
  - Final Choice.
  - AI Architect & User Rationale.
  - Potential Impact vector.

### Risk & Innovation Radars
- **Execution Class**: `ContinuousRadarScanner`
- **Mechanism**:
  - **Risk Radar**: Continuously scans files, code, and task logs to identify operational, financial, licensing, security, and scalability issues.
  - **Innovation Radar**: Matches current project keywords against newly crawled GitHub projects, ArXiv publications, and APIs to suggest library updates and technology replacements.

### Digital Twin & Autonomous Mentor
- **Execution Class**: `DigitalTwinEngine` / `MentorCoach`
- **Mechanism**:
  - **Digital Twin**: Simulates code performance, bottlenecks, and user interaction patterns.
  - **Autonomous Mentor**: Coaches the user through daily actions, identifying skill gaps (e.g., recommends TypeScript exercises if the user runs into compile errors often) and guiding the workflow.
