# State Management & Offline Synchronization

IdeasOS uses a **layered state architecture** designed to guarantee a fast, offline-first user experience. The client manages rendering state, local caching, and synchronization using a combination of **Zustand**, **React Query**, and **IndexedDB**.

---

## 1. Client-Side Store (Zustand)

Zustand manages immediate UI state (active tab, selected project, sidebar toggle) and local caches of active agent chat streams.

```typescript
// frontend/src/store/workspaceStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface ProjectState {
  id: string;
  name: string;
  dnaHash: string;
}

interface WorkspaceStore {
  currentWorkspaceId: string | null;
  activeProject: ProjectState | null;
  sidebarOpen: boolean;
  keyboardShortcutsEnabled: boolean;
  setWorkspace: (id: string) => void;
  setActiveProject: (project: ProjectState) => void;
  toggleSidebar: () => void;
}

export const useWorkspaceStore = create<WorkspaceStore>()(
  persist(
    (set) => ({
      currentWorkspaceId: null,
      activeProject: null,
      sidebarOpen: true,
      keyboardShortcutsEnabled: true,
      setWorkspace: (id) => set({ currentWorkspaceId: id }),
      setActiveProject: (project) => set({ activeProject: project }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
    }),
    {
      name: 'ideas-os-workspace-state',
      storage: createJSONStorage(() => localStorage), // Saved to local storage for instant loads
    }
  )
);
```

---

## 2. Server Cache & Synchronization (React Query)

React Query (TanStack Query) handles fetching, caching, and invalidating remote/local FastAPI resources. It ensures that network calls are deduplicated and background updates occur smoothly without freezing the UI.

- **Tasks Cache Key**: `['projects', projectId, 'tasks']`
- **Graph Cache Key**: `['projects', projectId, 'graph']`
- **Query Configuration**:
  - `staleTime`: 10,000ms (Data is considered fresh for 10 seconds).
  - `refetchOnWindowFocus`: false (Prevents unnecessary background requests when switching desktop windows).

---

## 3. Offline Cache Strategy (IndexedDB)

For large binary resources (e.g., uploaded PDFs, voice notes, and UI layouts), IdeasOS runs a local cache loop using **IndexedDB** (via `localforage` or `dexie.js`).

1. **Write Path**: When a user drags a file into the inbox, the file binary is saved directly into IndexedDB, and the file URI is passed to the backend.
2. **Read Path**: The UI checks IndexedDB before initiating network requests to fetch raw files. This guarantees that PDFs and images load instantly even when offline.

---

## 4. Conflict Resolution & Real-Time CRDT Sync

For team deployments, IdeasOS implements conflict-free sync using Conflict-Free Replicated Data Types (CRDTs) via **Yjs** over WebSockets.

- **Document Model**: The Knowledge Graph is modeled as a shared Yjs Document (`Y.Doc`). Nodes are elements in a `Y.Map`, and edges are stored in a `Y.Array`.
- **Conflict Handling**: If two team members edit the same task description or change a graph edge while offline:
  - Yjs automatically merges updates chronologically based on state vectors when connection is restored.
  - The UI uses visual markers (colored glow lines) to indicate nodes currently being modified by other active team members.
