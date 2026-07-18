# UI/UX Design System

IdeasOS is built for power-users, founders, and developers. The design language is **developer-centric, clean, dark-mode first, and keyboard-driven (keyboard-first)**.

---

## 1. Visual Language: Neo-Brutalist Glassmorphism

To give the application a premium, high-tech, and futuristic look, IdeasOS implements a design system called **Cyber-Glass**. It is characterized by:
- **Semi-transparent backdrops** utilizing CSS backdrop-filters.
- **Micro-borders** (1px solid borders with subtle gradients).
- **Vibrant accent glow lines** representing project states and processing stages.
- **Deep space color palettes** (rich blacks, deep blues, slate grays).

---

## 2. Core Color Tokens (HSL Palette)

We avoid generic colors (plain red/blue/green) in favor of high-contrast, harmonious tone scales:

```
Background:  #020408 (hsl(220, 60%, 2%))    [Deep Abyss]
Foreground:  #F8FAFC (hsl(210, 40%, 98%))   [Clean White]
Card Glass:  rgba(15, 23, 42, 0.6)          [Slate Glass]
Border:      rgba(255, 255, 255, 0.08)       [Subtle Frost]

Accents:
- Primary:   hsl(250, 95%, 65%)             [Aether Indigo]
- Secondary: hsl(190, 95%, 50%)             [Cyan Spark]
- Danger:    hsl(350, 90%, 55%)             [Crimson Laser]
- Warning:   hsl(40, 95%, 50%)              [Amber Alert]
- Success:   hsl(150, 90%, 45%)             [Emerald Grid]
```

---

## 3. Typography & Grids

- **Primary Font**: `Inter` (sans-serif) for high legibility in UI widgets, tasks, and markdown files.
- **Mono Font**: `JetBrains Mono` or `Fira Code` for schemas, terminal logs, code previews, and short commands.
- **Grid Layout**: 12-column responsive layout for configurations, defaulting to a three-pane layout in normal operation:
  - **Left Pane (width 16%)**: Navigation, workspace selection, project list, DNA status indicator.
  - **Center Pane (width 54%)**: Workspace canvas (interactive Knowledge Graph, Kanban boards, or markdown editors).
  - **Right Pane (width 30%)**: Dynamic Agent Chat Sidecar & Terminal (allows interaction with active agents).

---

## 4. Keyboard-First Shortcut Configuration

IdeasOS is fully navigable without a mouse. Below is the global keyboard binding map:

| Keybinding | Action | UI Result |
|---|---|---|
| `Ctrl + P` (or `Cmd + P`) | Command Palette | Launches search bar for projects, tasks, or agents. |
| `Ctrl + \` | Toggle Agent Sidecar | Hides or shows the right-hand Chat Pane. |
| `G` then `G` | View Knowledge Graph | Renders the fullscreen node graph. |
| `G` then `I` | View Inbox | Opens the raw input zone. |
| `G` then `T` | View Tasks | Focuses on project issue boards. |
| `Alt + N` | Add New Idea | Pops up quick text capture overlay. |
| `Alt + Enter` | Trigger Agent run | Asks the active agent panel to evaluate current state. |
| `Esc` | Close Overlay | Minimizes palettes, popups, and dropdown menus. |

---

## 5. CSS Core Variables Implementation

These values are loaded inside `frontend/src/index.css`:

```css
/* frontend/src/index.css */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 220 60% 2%;
    --foreground: 210 40% 98%;
    
    --card: 222 47% 11%;
    --card-foreground: 210 40% 98%;
    
    --popover: 224 71% 4%;
    --popover-foreground: 210 40% 98%;
    
    --primary: 250 95% 65%;
    --primary-foreground: 210 40% 98%;
    
    --secondary: 190 95% 50%;
    --secondary-foreground: 222 47% 11%;
    
    --muted: 215 25% 27%;
    --muted-foreground: 215 20% 65%;
    
    --accent: 216 34% 17%;
    --accent-foreground: 210 40% 98%;
    
    --border: 217 22% 12%;
    --input: 217 22% 12%;
    --ring: 250 95% 65%;
  }
}

.glass-panel {
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(12px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.neon-glow-cyan {
  box-shadow: 0 0 15px rgba(6, 182, 212, 0.15);
}
```
