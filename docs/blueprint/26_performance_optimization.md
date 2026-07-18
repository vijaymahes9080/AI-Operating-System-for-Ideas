# Performance Optimization

To deliver a highly responsive UI, IdeasOS implements a suite of performance optimization strategies across the database layer, the network API, and the React front-end client.

---

## 1. Database Indexing & SQLite Configuration

SQLite runs in **Write-Ahead Logging (WAL) mode** instead of default Rollback Journal mode. This allows concurrent read connections while a background agent is writing to the database.

### Core SQLite Tuning Parameters
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000; -- Allocates 64MB of cache memory
PRAGMA temp_store = MEMORY;
PRAGMA mmap_size = 268435456; -- Maps 256MB database into memory directly
```

### Relational Index Setup
```sql
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_raw_inbox_processed ON raw_inbox(processed);
```

---

## 2. API Streaming & Content Caching

- **Token Streaming**: Long-running agent text responses are streamed token-by-token using SSE (**Server-Sent Events**) or WebSockets. This minimizes user-perceived latency (Time to First Token) compared to waiting for complete text blocks.
- **RAG Embedding Cache**: Computed chunk vectors are cached in the `local_kv_cache` database table using the hash of the source text block. If the same reference paragraph is ingested across projects, vector compute is bypassed.

---

## 3. Front-End Render Tuning & Lazy Loading

Rendering thousands of nodes in the Knowledge Graph can easily cause UI stuttering and low frames per second.

```typescript
// frontend/src/components/graph/LazyGraphRenderer.tsx
import React, { useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

interface GraphProps {
  data: any;
  viewportBound: { x1: number; y1: number; x2: number; y2: number };
}

export const LazyGraphRenderer: React.FC<GraphProps> = ({ data, viewportBound }) => {
  // Filter nodes out of screen viewport bounds to prevent canvas lag
  const visibleData = useMemo(() => {
    return {
      nodes: data.nodes.filter((node: any) => {
        if (!node.x) return true; // Initial render
        return (
          node.x >= viewportBound.x1 &&
          node.x <= viewportBound.x2 &&
          node.y >= viewportBound.y1 &&
          node.y <= viewportBound.y2
        );
      }),
      links: data.links.filter((link: any) => {
        // Only render links if both source and target are visible
        return (
          data.nodes.some((n: any) => n.id === link.source && n.visible) &&
          data.nodes.some((n: any) => n.id === link.target && n.visible)
        );
      })
    };
  }, [data, viewportBound]);

  return (
    <ForceGraph2D
      graphData={visibleData}
      cooldownTicks={100} // Stops simulation physics calculation early
      enableNodeDrag={true}
    />
  );
};
```
- **React Node Memoization**: Node elements on the board use `React.memo` to prevent re-rendering when other portions of the tree change.
- **Dynamic Import Splits**: Large client pages (like the Scenario Simulator and Graph Viewer) are split using dynamic imports (`React.lazy`), reducing the initial JavaScript bundle download size.
