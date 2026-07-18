// frontend/src/store/workspaceStore.ts
import { create } from 'zustand';


export interface Project {
  id: string;
  workspace_id: string;
  name: string;
  description: string;
  dna_hash: string;
  innovation_score: number;
  monetization_score: number;
  complexity_level: string;
  created_at: string;
}

export interface Task {
  id: string;
  project_id: string;
  title: string;
  description: string;
  status: 'BACKLOG' | 'TODO' | 'IN_PROGRESS' | 'REVIEW' | 'DONE';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  assignee: string;
  estimated_hours: number;
}

export interface Decision {
  id: string;
  project_id: string;
  decision_title: string;
  context: string;
  choice: string;
  rationale: string;
}

export interface GraphData {
  nodes: Array<{ id: string; label: string; title: string; [key: string]: any }>;
  links: Array<{ source: string; target: string; type: string }>;
}

interface WorkspaceState {
  projects: Project[];
  activeProject: Project | null;
  tasks: Task[];
  decisions: Decision[];
  graphData: GraphData;
  simulationResults: any[];
  logs: string[];
  isLoading: boolean;
  runningAgents: string[];
  
  // Actions
  fetchProjects: () => Promise<void>;
  createProject: (name: string, description: string) => Promise<void>;
  selectProject: (project: Project) => Promise<void>;
  fetchProjectTasks: (projectId: string) => Promise<void>;
  fetchProjectDecisions: (projectId: string) => Promise<void>;
  fetchProjectGraph: (projectId: string) => Promise<void>;
  runProjectSimulation: (projectId: string, growth: number, churn: number, capital: number) => Promise<void>;
  fetchSimulationResults: (projectId: string) => Promise<void>;
  ingestIdea: (title: string, content: string) => Promise<void>;
  addLog: (message: string) => void;
}

const API_BASE = "http://127.0.0.1:8000/api/v1";

export const useWorkspaceStore = create<WorkspaceState>((set, get) => ({
  projects: [],
  activeProject: null,
  tasks: [],
  decisions: [],
  graphData: { nodes: [], links: [] },
  simulationResults: [],
  logs: ["System booted. Ready for ingestion."],
  isLoading: false,
  runningAgents: [],

  fetchProjects: async () => {
    set({ isLoading: true });
    try {
      const res = await fetch(`${API_BASE}/projects`);
      const data = await res.json();
      set({ projects: data });
      if (data.length > 0 && !get().activeProject) {
        get().selectProject(data[0]);
      }
    } catch (e) {
      get().addLog(`Error loading projects: ${e}`);
    } finally {
      set({ isLoading: false });
    }
  },

  createProject: async (name, description) => {
    set({ isLoading: true, runningAgents: ["researcher", "coder"] });
    get().addLog(`Spawning Researcher & Developer agents for '${name}'...`);
    try {
      const res = await fetch(`${API_BASE}/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
      });
      const result = await res.json();
      get().addLog(`Project scaffolded. DNA generated: ${result.dna_hash}`);
      
      // Reload projects list
      await get().fetchProjects();
    } catch (e) {
      get().addLog(`Failed to create project: ${e}`);
    } finally {
      set({ isLoading: false, runningAgents: [] });
    }
  },

  selectProject: async (project) => {
    set({ activeProject: project });
    get().addLog(`Workspace context set to Project: ${project.name}`);
    await get().fetchProjectTasks(project.id);
    await get().fetchProjectDecisions(project.id);
    await get().fetchProjectGraph(project.id);
    await get().fetchSimulationResults(project.id);
  },

  fetchProjectTasks: async (projectId) => {
    try {
      const res = await fetch(`${API_BASE}/project/${projectId}/tasks`);
      const data = await res.json();
      set({ tasks: data });
    } catch (e) {
      get().addLog(`Failed fetching tasks: ${e}`);
    }
  },

  fetchProjectDecisions: async (projectId) => {
    try {
      const res = await fetch(`${API_BASE}/project/${projectId}/decisions`);
      const data = await res.json();
      set({ decisions: data });
    } catch (e) {
      get().addLog(`Failed fetching decisions: ${e}`);
    }
  },

  fetchProjectGraph: async (projectId) => {
    try {
      const res = await fetch(`${API_BASE}/project/${projectId}/graph`);
      const data = await res.json();
      set({ graphData: data });
    } catch (e) {
      get().addLog(`Failed fetching graph: ${e}`);
    }
  },

  runProjectSimulation: async (projectId, growth, churn, capital) => {
    set({ runningAgents: [...get().runningAgents, "finance"] });
    get().addLog(`Triggering Monte Carlo simulation engine...`);
    try {
      await fetch(`${API_BASE}/project/${projectId}/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ growth_rate: growth, churn_rate: churn, capital: capital })
      });
      // Wait for simulator
      await new Promise(r => setTimeout(r, 2500));
      await get().fetchSimulationResults(projectId);
      get().addLog(`Simulation completed. Cached results updated.`);
    } catch (e) {
      get().addLog(`Simulation calculation failed: ${e}`);
    } finally {
      set({ runningAgents: get().runningAgents.filter(a => a !== "finance") });
    }
  },

  fetchSimulationResults: async (projectId) => {
    try {
      const res = await fetch(`${API_BASE}/project/${projectId}/simulation-results`);
      const data = await res.json();
      set({ simulationResults: data });
    } catch (e) {
      get().addLog(`Failed loading simulations: ${e}`);
    }
  },

  ingestIdea: async (title, content) => {
    try {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("content", content);
      formData.append("source_type", "TEXT");
      
      const res = await fetch(`${API_BASE}/inbox/ingest`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      get().addLog(`Ingested raw input node: ${data.inbox_id}`);
    } catch (e) {
      get().addLog(`Inbox ingestion failed: ${e}`);
    }
  },

  addLog: (message) => {
    const time = new Date().toLocaleTimeString();
    set((state) => ({ logs: [...state.logs, `[${time}] ${message}`] }));
  }
}));
