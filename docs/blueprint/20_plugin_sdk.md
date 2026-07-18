# Plugin SDK & Sandboxed Runtime

IdeasOS features a modular plugin ecosystem that allows developers to write custom connectors, agent logic, UI extensions, and reporting templates.

---

## 1. Plugin Manifest Specification

Every plugin is packaged in a directory containing a `manifest.json` file defining properties, permissions, and script locations.

```json
{
  "id": "ideas-os-patent-export",
  "name": "Patent PDF Generator",
  "version": "1.0.4",
  "description": "Compiles a completed concept and its research node citations into a USPTO-formatted draft application.",
  "author": "Open Patent Labs",
  "permissions": [
    "fs:read",
    "fs:write",
    "network:api.uspto.gov",
    "graph:read"
  ],
  "entrypoints": {
    "backend": "dist/backend.py",
    "frontend": "dist/index.js"
  }
}
```

---

## 2. Sandboxing Architecture

To protect user environments from malicious third-party code:

1. **Frontend Plugins (Iframe Sandboxing)**:
   - Plugin views render inside a HTML5 `<iframe>` with strict sandbox flags: `sandbox="allow-scripts"`.
   - The iframe cannot access `window.parent` or the parent DOM directly.
   - All communication between the Tauri host and the plugin iframe occurs via a secure asynchronous JSON-RPC messaging bridge over `window.postMessage`.
2. **Backend Plugins (WASM / WebAssembly)**:
   - High-privilege backend plugins run inside a sandboxed **Wasmtime** or **Wasmer** runtime.
   - The runtime denies arbitrary shell commands (`os.system`), file operations outside the project scope, and raw network sockets unless specified in the manifest permission list.

---

## 3. Python SDK Blueprint

Plugins inherit classes from the core SDK to hook into application state changes.

```python
# shared/plugin_sdk/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class IdeasOSPlugin(ABC):
    def __init__(self, api_client: Any):
        self.api = api_client

    @abstractmethod
    def on_load(self):
        """Called when plugin is loaded into memory."""
        pass

    @abstractmethod
    def on_unload(self):
        """Called on application exit or plugin disable."""
        pass


class ProjectHookPlugin(IdeasOSPlugin):
    """Hooks into project creation and update lifecycle events."""
    
    @abstractmethod
    def before_project_create(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allows modifying project schema inputs before DB commit."""
        return project_data

    @abstractmethod
    def after_project_create(self, project_id: str):
        """Asynchronous post-creation hook (e.g. sending slack alerts)."""
        pass
```

---

## 4. TypeScript Client SDK Blueprint

```typescript
// shared/plugin_sdk/client.ts
export interface SystemMessage {
  type: 'GET_ACTIVE_PROJECT' | 'MUTATE_GRAPH' | 'SHOW_TOAST';
  payload: any;
}

export class IdeasOSPluginBridge {
  private targetWindow: Window;

  constructor() {
    this.targetWindow = window.parent;
  }

  public async getActiveProject(): Promise<{ id: string; name: string }> {
    return this.sendRequest('GET_ACTIVE_PROJECT');
  }

  public showToast(message: string, style: 'info' | 'error'): void {
    this.postMessage('SHOW_TOAST', { message, style });
  }

  private sendRequest(type: string): Promise<any> {
    return new Promise((resolve) => {
      const requestId = Math.random().toString(36).substring(7);
      
      const listener = (event: MessageEvent) => {
        if (event.data?.requestId === requestId) {
          window.removeEventListener('message', listener);
          resolve(event.data.payload);
        }
      };

      window.addEventListener('message', listener);
      this.postMessage(type, { requestId });
    });
  }

  private postMessage(type: string, data: any) {
    this.targetWindow.postMessage({ type, ...data }, '*');
  }
}
```
