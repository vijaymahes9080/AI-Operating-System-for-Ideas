# Deployment Strategy (Dockerless & Native)

IdeasOS prioritizes developer-first setups. While it supports enterprise cloud deployments via standard containers, the **primary installation strategy is completely native and Dockerless**, utilizing local shell tooling, virtual environments, and native binaries.

---

## 1. Local Native Installation Blueprint

IdeasOS runs natively on Windows, macOS, and Linux. The installation process uses:
- **`uv` / `pip`**: Fast, compiler-free Python package installations.
- **`npm`**: Frontend packaging and execution.
- **Tauri**: Packages the frontend and launches the native webview client window.

### System Prerequisites
1. **Python 3.11+**
2. **Node.js 18+**
3. **Rust Toolchain** (only required if building Tauri native app from source, otherwise pre-compiled binaries are used).

---

## 2. Platform Setup Scripting

We provide a script (`setup.ps1` for Windows, `setup.sh` for Unix-like systems) to bootstrap dependencies without requiring manual configurations.

### Unix/macOS Setup Script (`scripts/setup.sh`)
```bash
#!/bin/bash
set -e

echo "=== Initializing IdeasOS Local Workspace ==="

# 1. Create Python virtual environment using uv
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "Creating python environment..."
uv venv .venv
source .venv/bin/activate

# 2. Install backend Python dependencies
echo "Installing backend dependencies..."
cd backend
uv pip install -r pyproject.toml
cd ..

# 3. Install frontend node modules
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# 4. Initialize local SQLite databases and run migrations
echo "Configuring databases..."
python backend/app/main.py --init-db

echo "=== Setup Complete. Run './scripts/dev.sh' to launch. ==="
```

### Development Start Script (`scripts/dev.sh`)
Runs the backend API server, local database listeners, and Tauri/Vite frontend in parallel using lightweight background threads:

```bash
#!/bin/bash
source .venv/bin/activate

# Launch Backend FastAPI (Uvicorn) in background
cd backend
uvicorn app.main:app --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Launch Frontend UI (Vite) / Tauri Dev window
cd frontend
npm run tauri dev

# Clean up processes on exit
trap "kill $BACKEND_PID" EXIT
```

---

## 3. Production Running (PM2 & systemd)

For server deployments or persistent local instances, IdeasOS uses **PM2** (Process Manager 2) or standard Linux **systemd** service profiles instead of Docker.

### PM2 Application Manifest (`ecosystem.config.js`)
```javascript
module.exports = {
  apps: [
    {
      name: 'ideas-os-backend',
      script: '.venv/bin/uvicorn',
      args: 'app.main:app --host 127.0.0.1 --port 8000',
      cwd: './backend',
      interpreter: 'none',
      env: {
        DATABASE_URL: 'sqlite:///d:/open source projects/AI Operating System for Ideas/data/production.db',
        ENV: 'production'
      }
    },
    {
      name: 'ideas-os-frontend',
      script: 'npm',
      args: 'run start',
      cwd: './frontend'
    }
  ]
};
```

Using PM2 allows developers to run `pm2 start ecosystem.config.js` to immediately start, monitor, and configure the application servers with auto-restart on system crash or reboot.
