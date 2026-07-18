# Component Library Specifications

IdeasOS extends basic UI elements (like shadcn button, card, input) with three highly specialized, custom interactive components: the **Interactive Knowledge Graph Viewer**, the **Scenario Simulator Dashboard**, and the **Streaming Agent Console**.

---

## 1. Interactive Knowledge Graph Viewer (`GraphViewer.tsx`)

This component displays project components (Concepts, Papers, Code files) as nodes in a 2D/3D workspace. It allows users to click nodes, create manual links, and run graph mutations.

- **Technology**: React Force Graph (d3-force-3d wrapper) or cytoscape.js.
- **Interface Definition**:
  ```typescript
  // frontend/src/components/graph/GraphViewer.tsx
  import React from 'react';
  
  export interface GraphNode {
    id: string;
    label: string;      // e.g., 'ResearchPaper', 'Task'
    title: string;
    color?: string;
    val?: number;       // Size multiplier
    properties: Record<string, any>;
  }
  
  export interface GraphLink {
    source: string;     // Node ID
    target: string;     // Node ID
    type: string;       // e.g., 'DEPENDS_ON'
  }
  
  interface GraphViewerProps {
    projectId: string;
    nodes: GraphNode[];
    links: GraphLink[];
    onNodeClick: (node: GraphNode) => void;
    onEdgeCreate: (sourceId: string, targetId: string, type: string) => void;
    engine: '2D' | '3D';
  }
  
  export const GraphViewer: React.FC<GraphViewerProps> = ({
    projectId,
    nodes,
    links,
    onNodeClick,
    onEdgeCreate,
    engine
  }) => {
    // Renders canvas using d3 force graph
    // Implements zoom, pan, select, search nodes
    return <div id={`graph-canvas-${projectId}`} className="w-full h-full relative" />;
  };
  ```

---

## 2. Scenario Simulator Dashboard (`ScenarioSimulator.tsx`)

Runs simulations (Monte Carlo forecasts) of project success, funding, user growth, and technical debt accumulation.

- **Technology**: Apache ECharts or Recharts.
- **Visuals**: Line chart with range bands showing 10th, 50th, and 90th percentile outcomes.
- **Interface Definition**:
  ```typescript
  // frontend/src/components/simulator/ScenarioSimulator.tsx
  import React from 'react';
  
  export interface SimulationMetrics {
    month: number;
    lowOutcome: number;     // 10th percentile
    medianOutcome: number;  // 50th percentile
    highOutcome: number;    // 90th percentile
  }
  
  interface SimulatorProps {
    projectId: string;
    scenarioType: 'STARTUP_FUNDING' | 'DEV_TIMELINE' | 'INFRA_COST';
    initialConditions: Record<string, number>;
    onRunSimulation: (params: any) => Promise<SimulationMetrics[]>;
  }
  
  export const ScenarioSimulator: React.FC<SimulatorProps> = ({
    projectId,
    scenarioType,
    initialConditions,
    onRunSimulation
  }) => {
    // Renders custom parameter input sliders
    // Renders ECharts graph showing confidence bands
    return <div className="glass-panel p-6 rounded-lg neon-glow-cyan" />;
  };
  ```

---

## 3. Streaming Agent Console & Terminal (`AgentConsole.tsx`)

A split-panel terminal. The top panel streams agent responses in real time, and the bottom panel shows system logs (such as file edits, git commands, and test logs).

- **Technology**: xterm.js (for CLI/logs) and React Markdown (with syntax highlighting for agent text).
- **Interface Definition**:
  ```typescript
  // frontend/src/components/terminal/AgentConsole.tsx
  import React, { useEffect, useRef } from 'react';
  
  export interface LogMessage {
    id: string;
    level: 'INFO' | 'WARN' | 'ERROR' | 'SUCCESS';
    module: string;
    text: str;
    timestamp: number;
  }
  
  interface AgentConsoleProps {
    sessionId: string;
    activeAgentId: string;
    logs: LogMessage[];
    onSendCommand: (cmd: string) => void;
  }
  
  export const AgentConsole: React.FC<AgentConsoleProps> = ({
    sessionId,
    activeAgentId,
    logs,
    onSendCommand
  }) => {
    const termRef = useRef<HTMLDivElement>(null);
    
    // Connects to WebSocket /api/v1/ws/agents/{sessionId}
    // Pulls xterm terminal feeds
    return (
      <div className="flex flex-col h-full bg-[#020408] border-l border-white/10">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Agent response stream markdown */}
        </div>
        <div ref={termRef} className="h-48 border-t border-white/10" />
      </div>
    );
  };
  ```
