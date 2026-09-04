#!/usr/bin/env bash
# Start FastAPI RAG engine from the sih root (one level above sihFrontend)
set -e

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo ""
echo "⚡ [FastAPI] Activating Python venv..."
source "$ROOT/venv/bin/activate"

echo "⚡ [FastAPI] Starting RAG server on http://localhost:8000 ..."
cd "$ROOT"
exec uvicorn fastapi_server:server --host 0.0.0.0 --port 8000
