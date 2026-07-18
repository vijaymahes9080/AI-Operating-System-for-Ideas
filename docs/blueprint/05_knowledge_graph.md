# Knowledge Graph Schema

Every project, requirement, research paper, API, and codebase entity in IdeasOS is represented as a node in a unified, queryable **Knowledge Graph**. This page specifies node types, edge properties, and query patterns.

---

## 1. Graph Model Definition

```
        (p:Project) -[:HAS_CONCEPT]-> (c:Concept)
             |                             |
     [:HAS_TASK]               [:RESOLVED_BY]-> (r:ResearchPaper)
             v                             |
         (t:Task) -[:DEPENDS_ON]-> (d:Dependency)
             |                             |
     [:PROTOTYPES]              [:CONSUMES_API]-> (a:APIEndpoint)
             v
        (s:Screen)
```

---

## 2. Nodes, Edges, and Properties

### Nodes

| Node Label | Key Properties | Purpose |
|---|---|---|
| `:Project` | `id`, `name`, `description`, `created_at` | The root project context node. |
| `:Concept` | `id`, `title`, `summary`, `novelty_score` | A core abstract business or scientific idea. |
| `:ResearchPaper` | `id`, `title`, `authors`, `url`, `bibtex`, `citation_count` | An academic source ingested by RAG. |
| `:Task` | `id`, `title`, `status`, `priority`, `estimated_hours` | A concrete, trackable work ticket. |
| `:Dependency` | `id`, `package_name`, `license_type`, `version` | Libraries or packages utilized in code. |
| `:APIEndpoint` | `id`, `path`, `method`, `protocol` (HTTP/WS), `auth_type` | An internal or external API route. |
| `:Screen` | `id`, `name`, `wireframe_schema` (JSON), `layout_type` | UI view layouts designed by the prototyping system. |

### Edges

| Edge Type | Source Node | Target Node | Properties | Description |
|---|---|---|---|---|
| `:HAS_CONCEPT` | `:Project` | `:Concept` | `weight: Float` | Link to concepts defined in the inbox. |
| `:RESOLVED_BY` | `:Concept` | `:ResearchPaper` | `relevance: Float` | Papers that supply solutions to concepts. |
| `:HAS_TASK` | `:Project` | `:Task` | `created_at: Int` | Issues tied to the project scope. |
| `:DEPENDS_ON` | `:Task` / `:Task` | `:Task` | `type: String` | Critical path scheduling lock. |
| `:CONSUMES_API` | `:Project` / `:Task` | `:APIEndpoint` | `is_internal: Bool` | Code execution dependencies on external endpoints. |
| `:PROTOTYPES` | `:Task` | `:Screen` | `version: Int` | UI tasks linked to mock screens. |

---

## 3. Cypher Query Implementations

### Finding Project Risk Chains
Identify incomplete tasks that have parent dependencies that are currently blocked:

```cypher
MATCH (p:Project {id: $project_id})-[:HAS_TASK]->(t:Task)
MATCH (t)-[:DEPENDS_ON]->(dep:Task)
WHERE t.status <> 'DONE' AND dep.status IN ['BACKLOG', 'TODO']
RETURN t.title AS BlockedTask, dep.title AS Blocker, dep.status AS BlockerStatus
```

### Contextual Graph RAG Retrieval
Retrieve concepts, research papers, and dependencies associated with a project to build LLM context prompts:

```cypher
MATCH (p:Project {id: $project_id})-[:HAS_CONCEPT]->(c:Concept)
OPTIONAL MATCH (c)-[:RESOLVED_BY]->(r:ResearchPaper)
OPTIONAL MATCH (p)-[:CONSUMES_API]->(a:APIEndpoint)
RETURN c.title, c.summary, collect(r.title) AS Papers, collect(a.path) AS APIs
LIMIT 10
```

---

## 4. Local Graph Implementation (Embedded Option)

To guarantee the **Docker-Free** local startup requirement, the server uses a Python driver interface (`graph_client.py`) that falls back to a local disk-serialized **NetworkX** object or an embedded **DuckDB Graph / SQLite** table layout if Neo4j is not locally running:

```python
# backend/app/graph/client.py
import os
import json
import networkx as nx

class GraphClient:
    def __init__(self, db_dir: str, use_neo4j: bool = False):
        self.use_neo4j = use_neo4j
        self.db_path = os.path.join(db_dir, "knowledge_graph.gml")
        if not self.use_neo4j:
            if os.path.exists(self.db_path):
                self.graph = nx.read_gml(self.db_path)
            else:
                self.graph = nx.DiGraph()
        else:
            # Initialize Neo4j driver connection
            pass

    def add_node(self, node_id: str, label: str, properties: dict):
        if not self.use_neo4j:
            self.graph.add_node(node_id, label=label, **properties)
            self._save()
        else:
            # Cypher insert logic
            pass

    def add_edge(self, source_id: str, target_id: str, edge_type: str, properties: dict):
        if not self.use_neo4j:
            self.graph.add_edge(source_id, target_id, type=edge_type, **properties)
            self._save()
        else:
            # Cypher edge link logic
            pass

    def _save(self):
        nx.write_gml(self.graph, self.db_path)
```
