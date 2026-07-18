# Extension API & UI Slots

While the **Plugin SDK** dictates how third-party code executes securely, the **Extension API** governs how plugins inject UI components, buttons, and custom views directly into the IdeasOS React client.

---

## 1. UI Extension Target Slots

IdeasOS defines explicit **extension coordinates** where plugins can inject UI elements:

```
+-------------------------------------------------------------------------------+
|                       IDEASOS WEB / DESKTOP SYSTEM                            |
|                                                                               |
|  [Sidebar Navigation]                                                         |
|  +-------------------------------------------------------------------------+  |
|  | Slot: nav_item_bottom                                                   |  |
|  +-------------------------------------------------------------------------+  |
|                                                                               |
|  [Workspace Center Canvas]                                                    |
|  +---------------------------+  +------------------------------------------+  |
|  | Slot: graph_node_context  |  | Slot: doc_toolbar_actions                |  |
|  | (Custom right-click menu) |  | (Adds buttons like 'Export Patent')      |  |
|  +---------------------------+  +------------------------------------------+  |
|                                                                               |
|  [Agent Sidebar Drawer]                                                       |
|  +-------------------------------------------------------------------------+  |
|  | Slot: agent_chat_actions                                                |  |
|  +-------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------+
```

---

## 2. API Interface: Registering UI Slots

Plugins register their components dynamically by exporting a standard hook configuration in JavaScript/TypeScript:

```typescript
// sample-plugin/src/frontend.ts
import { ExtensionAPI } from 'ideas-os-extension-api';

export function initialize(api: ExtensionAPI) {
  // 1. Inject a custom document toolbar action
  api.registerExtensionSlot({
    slotId: 'doc_toolbar_actions',
    id: 'patent-compiler-action',
    label: 'Generate Patent Draft',
    icon: 'Gavel', // Lucide icon name
    onClick: async (context) => {
      const activeProject = context.project;
      api.showToast(`Analyzing ${activeProject.name} for patent claims...`, 'info');
      
      // Call backend plugin function
      const result = await api.callBackend('generate_claims', { projectId: activeProject.id });
      api.showModal('Patent Results', result.markdown_summary);
    }
  });

  // 2. Register custom rendering node logic for the Knowledge Graph
  api.registerGraphNodeRenderer('ResearchPaper', (node, ctx) => {
    // Custom SVG drawing for ResearchPaper nodes
    const svg = ctx.createElementNS('http://www.w3.org/2000/svg', 'g');
    
    const circle = ctx.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('r', '8');
    circle.setAttribute('fill', '#06b6d4'); // Cyan accent
    circle.setAttribute('stroke', '#ffffff');
    circle.setAttribute('stroke-width', '1.5');
    
    svg.appendChild(circle);
    return svg;
  });
}
```

---

## 3. Sandboxed Render Loop (PostMessage UI IPC)

When the React app mounts an extension target, it fetches the registered plugin UI iframe and passes down context coordinates:

```typescript
// frontend/src/components/ui/ExtensionSlotRenderer.tsx
import React from 'react';

interface SlotProps {
  slotId: string;
  contextData: any;
}

export const ExtensionSlotRenderer: React.FC<SlotProps> = ({ slotId, contextData }) => {
  // Query all active plugins registered to this slotId
  const registeredExtensions = useExtensionStore((state) => state.slots[slotId] || []);

  return (
    <div className="flex space-x-2">
      {registeredExtensions.map((ext) => (
        <button
          key={ext.id}
          className="flex items-center space-x-1 px-3 py-1.5 rounded bg-white/5 border border-white/10 hover:bg-white/10 text-xs transition"
          onClick={() => ext.onClick(contextData)}
        >
          <span>{ext.label}</span>
        </button>
      ))}
    </div>
  );
};
```
