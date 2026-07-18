// frontend/src/App.tsx
import React, { useEffect, useState } from 'react';
import { 
  useWorkspaceStore, 
  Project, 
  Task, 
  Decision 
} from './store/workspaceStore';
import { 
  Layers, 
  Compass, 
  FolderPlus, 
  Play, 
  Activity, 
  Terminal as TermIcon,
  Cpu, 
  GitFork, 
  TrendingUp, 
  GanttChartSquare,
  AlertTriangle,
  Lightbulb
} from 'lucide-react';

export default function App() {
  const {
    projects,
    activeProject,
    tasks,
    decisions,
    graphData,
    simulationResults,
    logs,
    runningAgents,
    fetchProjects,
    createProject,
    selectProject,
    runProjectSimulation,
    ingestIdea
  } = useWorkspaceStore();

  // Tab routing: 'graph' | 'arch' | 'tasks' | 'simulate'
  const [activeTab, setActiveTab] = useState<'graph' | 'arch' | 'tasks' | 'simulate'>('graph');
  
  // Creation States
  const [newProjName, setNewProjName] = useState('');
  const [newProjDesc, setNewProjDesc] = useState('');
  const [quickInput, setQuickInput] = useState('');

  // Simulation Sliders
  const [growth, setGrowth] = useState(0.15);
  const [churn, setChurn] = useState(0.05);
  const [capital, setCapital] = useState(10000);

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreateProject = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjName.trim()) return;
    createProject(newProjName, newProjDesc);
    setNewProjName('');
    setNewProjDesc('');
  };

  const handleQuickCommand = (e: React.FormEvent) => {
    e.preventDefault();
    if (!quickInput.trim()) return;
    
    if (quickInput.startsWith('/idea ')) {
      const content = quickInput.replace('/idea ', '');
      ingestIdea("Quick Capture Idea", content);
    } else {
      createProject(quickInput, "Auto-scaffolded via command box.");
    }
    setQuickInput('');
  };

  return (
    <div className="flex h-screen w-screen bg-background overflow-hidden relative grid-overlay">
      {/* BACKGROUND ACCENT GLOWS */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-accentPrimary/10 rounded-full filter blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-accentCyan/10 rounded-full filter blur-[120px] pointer-events-none" />

      {/* LEFT SIDEBAR PANEL: NAVIGATION & PROJECTS */}
      <aside className="w-72 border-r border-borderFrost glass-panel flex flex-col justify-between z-10">
        <div>
          {/* Brand header */}
          <div className="p-6 border-b border-borderFrost flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-accentPrimary to-accentCyan flex items-center justify-center shadow-lg shadow-accentPrimary/35">
              <Cpu className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg tracking-wider text-white">IdeaOS</h1>
              <p className="text-[10px] text-accentCyan uppercase tracking-widest font-mono">Cognitive Shell</p>
            </div>
          </div>

          {/* Scaffold Project Panel */}
          <div className="p-4 border-b border-borderFrost">
            <h2 className="text-xs uppercase text-slate-400 font-mono tracking-wider mb-3">Scaffold Project</h2>
            <form onSubmit={handleCreateProject} className="space-y-2">
              <input
                type="text"
                placeholder="Project Name..."
                value={newProjName}
                onChange={(e) => setNewProjName(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded px-3 py-1.5 text-sm focus:outline-none focus:border-accentPrimary text-white"
              />
              <textarea
                placeholder="Describe raw idea..."
                value={newProjDesc}
                onChange={(e) => setNewProjDesc(e.target.value)}
                rows={2}
                className="w-full bg-white/5 border border-white/10 rounded px-3 py-1.5 text-sm focus:outline-none focus:border-accentPrimary text-white resize-none"
              />
              <button
                type="submit"
                className="w-full py-1.5 rounded bg-gradient-to-r from-accentPrimary to-accentCyan text-white font-medium text-xs flex items-center justify-center gap-1 hover:brightness-110 transition shadow-md shadow-accentPrimary/20"
              >
                <FolderPlus className="w-4 h-4" /> Seed Digital Organism
              </button>
            </form>
          </div>

          {/* Projects List */}
          <div className="p-4">
            <h2 className="text-xs uppercase text-slate-400 font-mono tracking-wider mb-2">Workspace Organisms</h2>
            <div className="space-y-1.5 max-h-60 overflow-y-auto pr-1">
              {projects.map((p) => (
                <button
                  key={p.id}
                  onClick={() => selectProject(p)}
                  className={`w-full text-left px-3 py-2 rounded text-sm transition flex items-center justify-between border ${
                    activeProject?.id === p.id 
                      ? 'bg-accentPrimary/15 border-accentPrimary text-white shadow-sm' 
                      : 'bg-white/5 border-transparent text-slate-300 hover:bg-white/10'
                  }`}
                >
                  <span className="font-medium truncate">{p.name}</span>
                  <GitFork className="w-3.5 h-3.5 text-slate-500" />
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Global metadata status footer */}
        <div className="p-4 border-t border-borderFrost bg-white/[0.02] text-xs font-mono text-slate-400">
          <div>Profile: <span className="text-accentCyan">local</span></div>
          <div className="truncate">Database: sqlite3 WAL</div>
        </div>
      </aside>

      {/* CENTER PANELS: WORKSPACE CANVAS */}
      <main className="flex-1 flex flex-col justify-between overflow-hidden z-10">
        {/* Header Ribbon tab selector */}
        <header className="h-16 border-b border-borderFrost glass-panel flex items-center justify-between px-8">
          <div className="flex items-center space-x-1">
            {(['graph', 'arch', 'tasks', 'simulate'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 text-sm rounded font-medium capitalize transition-all ${
                  activeTab === tab 
                    ? 'bg-white/10 text-white border-b-2 border-accentCyan' 
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tab === 'graph' ? 'Knowledge Graph' : 
                 tab === 'arch' ? 'Architecture Studio' : 
                 tab === 'tasks' ? 'Task Board' : 'Scenario Simulator'}
              </button>
            ))}
          </div>

          {/* Active project health dashboard */}
          {activeProject && (
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-xs text-slate-400 font-mono">Innovation DNA Score</div>
                <div className="text-sm font-bold text-accentCyan">{Math.round(activeProject.innovation_score * 100)}%</div>
              </div>
              <div className="w-10 h-10 rounded-full border border-borderFrost flex items-center justify-center relative overflow-hidden bg-white/5">
                {/* Visual score spinner */}
                <div className="absolute inset-0 bg-gradient-to-tr from-accentPrimary/20 to-accentCyan/20 animate-pulse" />
                <Lightbulb className="w-5 h-5 text-accentCyan" />
              </div>
            </div>
          )}
        </header>

        {/* Dynamic Display Canvas View */}
        <section className="flex-1 p-8 overflow-y-auto">
          {activeTab === 'graph' && (
            <div className="w-full h-full glass-panel rounded-lg flex flex-col p-6 relative overflow-hidden">
              <h3 className="text-md font-bold mb-1 text-white flex items-center gap-1.5"><Compass className="w-5 h-5 text-accentCyan" /> Semantic Map Network</h3>
              <p className="text-xs text-slate-400 mb-4">Visualizing connections across raw inbox ideas, academic references, database concepts, and developer checklist tasks.</p>
              
              {/* Dynamic SVG Node-Edge graph layout */}
              <div className="flex-1 border border-white/5 rounded bg-black/45 relative flex items-center justify-center">
                {graphData.nodes.length === 0 ? (
                  <div className="text-sm text-slate-500 font-mono">No nodes active. Seed a project on the left to spawn research links.</div>
                ) : (
                  <svg className="w-full h-full min-h-[400px]">
                    {/* Draw connections first */}
                    {graphData.links.map((link, idx) => {
                      const sourceNode = graphData.nodes.find(n => n.id === link.source);
                      const targetNode = graphData.nodes.find(n => n.id === link.target);
                      if (!sourceNode || !targetNode) return null;
                      
                      // Calculate mock offsets for lines
                      const x1 = 150 + (graphData.nodes.indexOf(sourceNode) * 120) % 400;
                      const y1 = 100 + (graphData.nodes.indexOf(sourceNode) * 90) % 250;
                      const x2 = 150 + (graphData.nodes.indexOf(targetNode) * 120) % 400;
                      const y2 = 100 + (graphData.nodes.indexOf(targetNode) * 90) % 250;
                      
                      return (
                        <g key={idx}>
                          <line
                            x1={x1}
                            y1={y1}
                            x2={x2}
                            y2={y2}
                            stroke="rgba(255,255,255,0.08)"
                            strokeWidth="1.5"
                          />
                          <text
                            x={(x1 + x2) / 2}
                            y={(y1 + y2) / 2 - 4}
                            fill="#06b6d4"
                            fontSize="8"
                            className="font-mono text-center opacity-65"
                          >
                            {link.type}
                          </text>
                        </g>
                      );
                    })}
                    {/* Draw Nodes */}
                    {graphData.nodes.map((node, idx) => {
                      const x = 150 + (idx * 120) % 400;
                      const y = 100 + (idx * 90) % 250;
                      const isProject = node.label === 'Project';
                      const isTask = node.label === 'Task';
                      
                      return (
                        <g key={node.id}>
                          <circle
                            cx={x}
                            cy={y}
                            r={isProject ? 22 : 14}
                            fill={isProject ? '#6366f1' : isTask ? '#06b6d4' : '#1e293b'}
                            stroke="rgba(255,255,255,0.2)"
                            strokeWidth="1.5"
                            className="cursor-pointer hover:stroke-accentCyan"
                          />
                          <text
                            x={x}
                            y={y + 3}
                            fill="#ffffff"
                            fontSize="8"
                            textAnchor="middle"
                            className="font-bold pointer-events-none select-none"
                          >
                            {node.label[0]}
                          </text>
                          <text
                            x={x}
                            y={y + (isProject ? 34 : 26)}
                            fill="#cbd5e1"
                            fontSize="10"
                            textAnchor="middle"
                            className="font-mono"
                          >
                            {node.title.length > 18 ? node.title.slice(0, 18) + '...' : node.title}
                          </text>
                        </g>
                      );
                    })}
                  </svg>
                )}
              </div>
            </div>
          )}

          {activeTab === 'arch' && (
            <div className="space-y-6">
              {/* Relational database layout */}
              <div className="glass-panel p-6 rounded-lg">
                <h3 className="text-md font-bold mb-2 text-white">Relational DB Schemas</h3>
                <pre className="p-4 rounded bg-black/45 border border-white/5 text-xs text-slate-300 font-mono overflow-x-auto">
{`CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    dna_hash TEXT UNIQUE,
    innovation_score REAL
);

CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES projects(id),
    title TEXT NOT NULL,
    status TEXT CHECK(status IN ('BACKLOG', 'TODO', 'IN_PROGRESS', 'REVIEW', 'DONE'))
);`}
                </pre>
              </div>

              {/* Decision Ledger */}
              <div className="glass-panel p-6 rounded-lg">
                <h3 className="text-md font-bold mb-4 text-white flex items-center gap-1.5"><GanttChartSquare className="w-5 h-5 text-accentPrimary" /> Architecture Decision Ledger</h3>
                <div className="border border-white/5 rounded overflow-hidden">
                  <table className="w-full text-left text-sm text-slate-300">
                    <thead className="bg-white/5 text-xs font-mono uppercase text-slate-400 border-b border-white/5">
                      <tr>
                        <th className="p-3">Decision</th>
                        <th className="p-3">Context</th>
                        <th className="p-3">Choice</th>
                        <th className="p-3">AI Rationale</th>
                      </tr>
                    </thead>
                    <tbody>
                      {decisions.length === 0 ? (
                        <tr>
                          <td colSpan={4} className="p-4 text-center text-slate-500 font-mono">No ledger entries loaded. Run RAG/Analysis first.</td>
                        </tr>
                      ) : (
                        decisions.map((d) => (
                          <tr key={d.id} className="border-b border-white/5 hover:bg-white/[0.01]">
                            <td className="p-3 font-semibold text-white">{d.decision_title}</td>
                            <td className="p-3 text-slate-400">{d.context}</td>
                            <td className="p-3 text-accentCyan font-mono">{d.choice}</td>
                            <td className="p-3 text-slate-300 text-xs italic">{d.rationale}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'tasks' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full min-h-[450px]">
              {/* Kanban: TODO column */}
              <div className="glass-panel p-4 rounded-lg flex flex-col">
                <h4 className="text-sm font-mono uppercase font-bold text-accentCyan mb-4 flex items-center justify-between border-b border-white/5 pb-2">
                  <span>Backlog / Todo</span>
                  <span className="bg-white/5 text-xs rounded-full px-2 py-0.5">{tasks.filter(t => t.status === 'TODO' || t.status === 'BACKLOG').length}</span>
                </h4>
                <div className="flex-1 space-y-3 overflow-y-auto">
                  {tasks.filter(t => t.status === 'TODO' || t.status === 'BACKLOG').map(t => (
                    <TaskCard key={t.id} task={t} />
                  ))}
                </div>
              </div>

              {/* Kanban: IN_PROGRESS column */}
              <div className="glass-panel p-4 rounded-lg flex flex-col">
                <h4 className="text-sm font-mono uppercase font-bold text-accentPrimary mb-4 flex items-center justify-between border-b border-white/5 pb-2">
                  <span>In Progress</span>
                  <span className="bg-white/5 text-xs rounded-full px-2 py-0.5">{tasks.filter(t => t.status === 'IN_PROGRESS').length}</span>
                </h4>
                <div className="flex-1 space-y-3 overflow-y-auto">
                  {tasks.filter(t => t.status === 'IN_PROGRESS').map(t => (
                    <TaskCard key={t.id} task={t} />
                  ))}
                </div>
              </div>

              {/* Kanban: DONE column */}
              <div className="glass-panel p-4 rounded-lg flex flex-col">
                <h4 className="text-sm font-mono uppercase font-bold text-emerald-400 mb-4 flex items-center justify-between border-b border-white/5 pb-2">
                  <span>Done</span>
                  <span className="bg-white/5 text-xs rounded-full px-2 py-0.5">{tasks.filter(t => t.status === 'DONE').length}</span>
                </h4>
                <div className="flex-1 space-y-3 overflow-y-auto">
                  {tasks.filter(t => t.status === 'DONE').map(t => (
                    <TaskCard key={t.id} task={t} />
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'simulate' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Parameter Settings */}
              <div className="glass-panel p-6 rounded-lg space-y-6">
                <h3 className="text-md font-bold text-white flex items-center gap-1.5"><Activity className="w-5 h-5 text-accentCyan" /> Simulator Parameters</h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-xs text-slate-400 block mb-1">Growth rate per month ({Math.round(growth * 100)}%)</label>
                    <input 
                      type="range" min="0.05" max="0.5" step="0.01" 
                      value={growth} onChange={(e) => setGrowth(parseFloat(e.target.value))}
                      className="w-full accent-accentCyan" 
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-400 block mb-1">Churn rate per month ({Math.round(churn * 100)}%)</label>
                    <input 
                      type="range" min="0.01" max="0.2" step="0.01" 
                      value={churn} onChange={(e) => setChurn(parseFloat(e.target.value))}
                      className="w-full accent-accentCyan" 
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-400 block mb-1">Starting capital (${capital.toLocaleString()})</label>
                    <input 
                      type="range" min="1000" max="50000" step="500" 
                      value={capital} onChange={(e) => setCapital(parseInt(e.target.value))}
                      className="w-full accent-accentCyan" 
                    />
                  </div>
                </div>

                <button
                  onClick={() => activeProject && runProjectSimulation(activeProject.id, growth, churn, capital)}
                  className="w-full py-2 bg-accentCyan text-background font-bold text-xs rounded hover:brightness-110 flex items-center justify-center gap-1 shadow-md shadow-accentCyan/20"
                >
                  <Play className="w-4 h-4" /> Run Monte Carlo Simulator
                </button>
              </div>

              {/* Confidence Band Results */}
              <div className="lg:col-span-2 glass-panel p-6 rounded-lg flex flex-col justify-between">
                <div>
                  <h3 className="text-md font-bold mb-1 text-white flex items-center gap-1.5"><TrendingUp className="w-5 h-5 text-accentPrimary" /> Project Capital Trajectory</h3>
                  <p className="text-xs text-slate-400 mb-4">12-Month Monte Carlo confidence range detailing success pathways and failure thresholds.</p>
                </div>
                
                <div className="border border-white/5 rounded overflow-hidden flex-1 max-h-72 overflow-y-auto">
                  <table className="w-full text-left text-xs font-mono text-slate-300">
                    <thead className="bg-white/5 text-slate-400 border-b border-white/5">
                      <tr>
                        <th className="p-2">Month</th>
                        <th className="p-2 text-rose-400">10th Percentile (Low)</th>
                        <th className="p-2 text-accentCyan">50th Percentile (Median)</th>
                        <th className="p-2 text-emerald-400">90th Percentile (High)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {simulationResults.length === 0 ? (
                        <tr>
                          <td colSpan={4} className="p-4 text-center text-slate-500">Click run simulation above to compute confidence metrics.</td>
                        </tr>
                      ) : (
                        simulationResults.map((r) => (
                          <tr key={r.month} className="border-b border-white/5 hover:bg-white/[0.01]">
                            <td className="p-2 font-bold text-white">Month {r.month}</td>
                            <td className="p-2 text-rose-400/90">${r.lowOutcome.toLocaleString()}</td>
                            <td className="p-2 text-accentCyan">${r.medianOutcome.toLocaleString()}</td>
                            <td className="p-2 text-emerald-400/90">${r.highOutcome.toLocaleString()}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </section>

        {/* BOTTOM SHELL DOCK: COMMAND PALETTE & SCROLLING DEVELOPER LOGS */}
        <footer className="glass-panel border-t border-borderFrost p-4 flex flex-col gap-3 z-10 bg-background/80">
          <form onSubmit={handleQuickCommand} className="flex gap-2">
            <div className="flex-1 relative">
              <input
                type="text"
                value={quickInput}
                onChange={(e) => setQuickInput(e.target.value)}
                placeholder="Enter command (e.g. '/idea Scaffold a webapp using SQLite' or input custom project name)..."
                className="w-full bg-[#020408] border border-white/10 rounded px-4 py-2 text-xs font-mono text-white focus:outline-none focus:border-accentCyan placeholder-slate-600"
              />
              <span className="absolute right-3 top-2.5 bg-white/5 border border-white/10 rounded px-1.5 py-0.5 text-[9px] font-mono text-slate-400 uppercase select-none">Alt+Enter</span>
            </div>
            <button
              type="submit"
              className="bg-white/5 border border-white/10 text-white px-4 text-xs font-mono rounded hover:bg-white/10 transition"
            >
              RUN
            </button>
          </form>

          {/* Scrolling Terminal logs */}
          <div className="h-28 bg-[#010204] border border-white/5 rounded p-3 font-mono text-[10px] text-slate-400 overflow-y-auto flex flex-col gap-1 relative scanline">
            <div className="flex items-center gap-1.5 border-b border-white/5 pb-1 mb-1 text-slate-500 font-bold uppercase tracking-wider">
              <TermIcon className="w-3.5 h-3.5 text-accentCyan" /> Development Environment Logs
            </div>
            {logs.map((log, idx) => (
              <div key={idx} className="truncate select-text">{log}</div>
            ))}
          </div>
        </footer>
      </main>

      {/* RIGHT SIDEBAR PANEL: COGNITIVE AGENTS DRIVER PANEL */}
      <aside className="w-80 border-l border-borderFrost glass-panel p-6 flex flex-col justify-between z-10 bg-background/90">
        <div>
          <h3 className="text-sm font-bold uppercase tracking-wider text-white mb-4 flex items-center gap-1.5"><Cpu className="w-4 h-4 text-accentPrimary" /> Copilot Sidecar</h3>
          
          <div className="space-y-4">
            {/* Researcher Agent status */}
            <AgentStatusCard
              name="Research Agent"
              role="Market & Literature crawling"
              isRunning={runningAgents.includes("researcher")}
            />
            {/* Architect Agent status */}
            <AgentStatusCard
              name="Architect Agent"
              role="Database design & schemas"
              isRunning={runningAgents.includes("coder")}
            />
            {/* Coder Agent status */}
            <AgentStatusCard
              name="Coding Agent"
              role="Code synthesis & testing"
              isRunning={runningAgents.includes("coder")}
            />
            {/* Business Advisor status */}
            <AgentStatusCard
              name="Business Agent"
              role="Monetization & forecast modeling"
              isRunning={runningAgents.includes("finance")}
            />
          </div>
        </div>

        {/* Dynamic warning checklist alerts */}
        <div className="border border-yellow-500/20 bg-yellow-500/5 p-4 rounded text-xs text-yellow-400 space-y-1 font-sans">
          <div className="flex items-center gap-1 font-bold font-mono text-[10px] uppercase tracking-wider">
            <AlertTriangle className="w-4 h-4" /> Risk Radar Notification
          </div>
          <p className="opacity-90 leading-relaxed">No external OAuth identity services configured. Running in local-first database mode.</p>
        </div>
      </aside>
    </div>
  );
}

// Sub components

interface AgentCardProps {
  name: string;
  role: string;
  isRunning: boolean;
}

function AgentStatusCard({ name, role, isRunning }: AgentCardProps) {
  return (
    <div className={`p-3.5 rounded border transition-all ${
      isRunning 
        ? 'border-accentCyan bg-accentCyan/5 shadow-[0_0_12px_rgba(6,182,212,0.08)]' 
        : 'border-white/5 bg-white/[0.01] hover:border-white/10'
    }`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-bold text-white">{name}</span>
        <span className={`w-2 h-2 rounded-full ${isRunning ? 'bg-accentCyan animate-ping' : 'bg-slate-700'}`} />
      </div>
      <p className="text-[10px] text-slate-500 mt-1 font-mono">{role}</p>
    </div>
  );
}

function TaskCard({ task }: { task: Task }) {
  const priorityColors = {
    LOW: 'text-slate-400 bg-slate-500/10 border-slate-500/20',
    MEDIUM: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    HIGH: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    URGENT: 'text-rose-400 bg-rose-500/10 border-rose-500/20'
  };

  return (
    <div className="p-3 bg-white/[0.02] border border-white/5 rounded glass-card-hover text-xs space-y-2">
      <div className="flex items-center justify-between">
        <span className="font-semibold text-white tracking-wide">{task.title}</span>
        <span className={`px-1.5 py-0.5 text-[8px] font-mono font-bold uppercase rounded border ${priorityColors[task.priority]}`}>
          {task.priority}
        </span>
      </div>
      <p className="text-slate-400 text-[11px] leading-relaxed truncate">{task.description}</p>
      <div className="flex items-center justify-between pt-1 text-[10px] text-slate-500 font-mono border-t border-white/5">
        <span>Hours: {task.estimated_hours}h</span>
        <span className="text-accentCyan uppercase">{task.assignee}</span>
      </div>
    </div>
  );
}
