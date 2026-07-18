#!/bin/bash
# scripts/setup.sh
set -e

echo "=== Initializing IdeaOS Dev Environment (Unix) ==="

# 1. Setup python environment
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment in .venv..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing backend dependency modules..."
pip install --upgrade pip
pip install -r backend/pyproject.toml --use-pep517

# 2. Setup Node frontend
echo "Installing React Node modules..."
cd frontend
npm install
cd ..

# 3. Create database path
mkdir -p backend/data

echo "==============================================="
echo "Bootstrap complete. Run './scripts/dev.sh' to launch."
echo "==============================================="
