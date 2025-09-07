.PHONY: install backend frontend dev db-up db-down migrate-up seed lint test

install:
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
	cd frontend && npm i

backend:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port $${PORT:-8000} --reload

frontend:
	cd frontend && npm run dev

migrate-up:
	cd backend && . .venv/bin/activate && alembic upgrade head

seed:
	cd scripts && ../backend/.venv/bin/python seed.py
