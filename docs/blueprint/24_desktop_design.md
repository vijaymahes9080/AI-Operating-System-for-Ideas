# Desktop Application Design

IdeasOS is packaged as a lightweight native desktop application using **Tauri** (Rust runtime + system WebView). Tauri is chosen over Electron because it delivers a smaller installer size, consumes less memory, and provides native OS integrations.

---

## 1. Tauri Host Configuration (`tauri.conf.json`)

Tauri handles native window controls, global keyboard shortcuts, systems tray menus, and file system boundaries.

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devPath": "http://localhost:5173",
    "distDir": "../dist"
  },
  "package": {
    "productName": "IdeasOS",
    "version": "1.0.0"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "fs": {
        "all": true,
        "scope": ["$APPCONFIG/*", "$DOCUMENT/*", "$APPDATA/*"]
      },
      "dialog": {
        "open": true,
        "save": true
      },
      "shell": {
        "open": true
      }
    },
    "bundle": {
      "active": true,
      "targets": "all",
      "identifier": "com.ideasos.desktop",
      "icon": ["icons/32x32.png", "icons/128x128.png", "icons/icon.icns", "icons/icon.ico"]
    },
    "windows": [
      {
        "title": "IdeasOS - Operating System for Ideas",
        "width": 1280,
        "height": 800,
        "resizable": true,
        "fullscreen": false,
        "decorations": true,
        "transparent": true
      }
    ]
  }
}
```

---

## 2. System Tray & Window Lifecycle

Tauri runs as a background service accessible from the system tray:

- **Minimize to Tray**: Clicking the close window button hides the window instead of terminating the app, allowing background agents to continue processing tasks.
- **Tray Menu options**:
  - `Quick Add Idea (Alt+N)`: Opens a small input window.
  - `Open Workspace`: Restores the primary application window.
  - `Pause Agent Orchestration`: Suspends NATS workers.
  - `Quit`: Exits the application.

---

## 3. Rust-Native FS Command Bridging

When the TypeScript frontend needs to perform direct filesystem edits (such as creating folder structures, writing generated codebase files, or running build checkers), it invokes Rust functions:

```rust
// src-tauri/src/main.rs
#![cfg_attr(
  all(not(debug_assertions), flags = "windows"),
  windows_subsystem = "windows"
)]

use std::fs;
use std::path::PathBuf;

#[tauri::command]
fn scaffold_project_directory(base_path: String, project_name: String) -> Result<String, String> {
    let mut path = PathBuf::from(base_path);
    path.push(project_name);
    
    // Create folders
    fs::create_dir_all(&path).map_err(|e| e.to_string())?;
    
    // Sub-directories
    fs::create_dir_all(path.join("backend")).map_err(|e| e.to_string())?;
    fs::create_dir_all(path.join("frontend")).map_err(|e| e.to_string())?;
    fs::create_dir_all(path.join("tests")).map_err(|e| e.to_string())?;
    
    Ok(format!("Directory scaffolded successfully at {:?}", path))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![scaffold_project_directory])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```typescript
// frontend/src/utils/tauriBridge.ts
import { invoke } from '@tauri-apps/api/tauri';

export async function runScaffold(basePath: string, name: string): Promise<string> {
  try {
    const message = await invoke<string>('scaffold_project_directory', {
      basePath,
      projectName: name,
    });
    return message;
  } catch (error) {
    throw new Error(`Tauri FS scaffold failed: ${error}`);
  }
}
```
