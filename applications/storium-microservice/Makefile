.PHONY: run migrate test test-smoke seed docker-up docker-down docker-logs docker-ps openapi

run:
	uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

migrate:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(m)"

test:
	python -m compileall -q app

test-smoke:
	pytest tests/smoke -v

openapi:
	python scripts/export_openapi.py

seed:
	python -m app.seed

seed-demo-user:
	SEED_DEMO_USER=true python -m app.seed

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f api ui traefik

docker-ps:
	docker compose ps
