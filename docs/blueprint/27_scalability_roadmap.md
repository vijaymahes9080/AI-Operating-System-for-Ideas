# Scalability Roadmap

While IdeasOS is designed to boot instantly on a local desktop machine without Docker, it includes a clear architectural path to scale into a distributed, multi-tenant enterprise cloud operating system.

---

## 1. Scalability Phases

```
[Phase 1: Local Desktop]  --->  [Phase 2: Single Node Server]  --->  [Phase 3: Distributed Cluster]
- SQLite + SQLite-vec           - PostgreSQL + Qdrant               - Multi-region Postgres
- Embedded Graph                - Neo4j Community Server            - Neo4j Enterprise Cluster
- Local thread queue            - Temporal + NATS Single Instance   - Multi-tenant Temporal Namespace
```

---

## 2. Infrastructure Scaling Specifications

### Database Layer
- **Local SQLite -> PostgreSQL (RDS/Aurora)**: The SQLAlchemy database connector switches via the `DATABASE_URL` environment parameter. PostgreSQL handles multi-tenant transaction locking and horizontal scaling.
- **Embedded NetworkX -> Neo4j Enterprise Cluster**: Migrates from file-backed GML objects to a distributed Neo4j cluster running Cypher routing protocols for enterprise-wide knowledge graph querying.
- **SQLite-vec -> Qdrant Cluster**: Large-scale vector storage migrates to a multi-node Qdrant cluster, which features vector partitioning, index segment isolation, and high-performance HNSW indexes.

### Message & Event Queue Layer
- **Local Thread Queue -> Distributed Temporal Cluster**: Long-running background jobs run on dedicated worker nodes connected to a managed Temporal Namespace backend backed by Cassandra/PostgreSQL.
- **Local Pub/Sub -> Clustered NATS JetStream**: Local event communication is upgraded to a clustered configuration of NATS instances to ensure message persistence, replica recovery, and low-latency websocket streaming across geo-distributed API servers.

---

## 3. Configuration Profiles

Developers select the deployment target using the `IDEASOS_PROFILE` environment variable on start:

```
# Default Local Run
IDEASOS_PROFILE=local

# Enterprise Production Cloud Run
IDEASOS_PROFILE=production
```

The config loader mounts specific drivers dynamically:

```python
# backend/app/config.py
import os

PROFILE = os.getenv("IDEASOS_PROFILE", "local")

if PROFILE == "production":
    DATABASE_URL = os.getenv("DATABASE_URL") # postgresql://...
    GRAPH_URI = os.getenv("NEO4J_URI")        # neo4j://...
    VECTOR_DB_URL = os.getenv("QDRANT_URL")    # http://...
    USE_TEMPORAL = True
else:
    # Fallback to local files
    DATABASE_URL = "sqlite:///d:/open source projects/AI Operating System for Ideas/data/local.db"
    GRAPH_URI = None
    VECTOR_DB_URL = None
    USE_TEMPORAL = False
```
---

## 4. Multi-Tenant Tenancy Isolation

For universities, research labs, or startup incubators hosting a shared IdeasOS cluster:
- **Tenant ID Enveloping**: Every database table contains a `tenant_id` column.
- **Row-Level Security (RLS)**: PostgreSQL executes RLS policies preventing workspace reads across tenant boundaries.
- **Graph Partitioning**: Graph nodes contain `tenantId` property labels. Cypher queries are automatically appended with `WHERE node.tenantId = $tenantId` at the API handler level.
