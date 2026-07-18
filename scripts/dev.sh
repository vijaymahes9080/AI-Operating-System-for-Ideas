#!/bin/bash
# scripts/dev.sh
source .venv/bin/activate

echo "=== Starting IdeaOS Backend Engine (Uvicorn) ==="
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
cd ..

echo "=== Starting IdeaOS Frontend Console (Vite) ==="
cd frontend
npm run dev

# Terminate backend on exit
trap "kill $BACKEND_PID" EXIT
