#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -U pip
pip install -r backend/requirements.txt
cp .env.example backend/.env || true
cd backend && alembic upgrade head
uvicorn app.main:app --reload --port 8000
