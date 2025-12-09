# BMECatDemo Justfile

# Default recipe - show available commands
default:
    @just --list

# Start PostgreSQL and OpenSearch containers
up:
    docker compose up -d

# Stop containers
down:
    docker compose down

# Stop containers and remove volumes
down-clean:
    docker compose down -v

# Show container status
status:
    docker compose ps

# Show container logs
logs *ARGS:
    docker compose logs {{ ARGS }}

# Convert BMECat XML to JSONL
convert INPUT OUTPUT:
    uv run python main.py {{ INPUT }} {{ OUTPUT }}

# Convert with header extraction
convert-with-header INPUT OUTPUT HEADER:
    uv run python main.py {{ INPUT }} {{ OUTPUT }} {{ HEADER }}

# Import JSONL to PostgreSQL
import FILE:
    uv run python -m src.db.import_jsonl {{ FILE }}

# Index products from PostgreSQL to OpenSearch
index:
    uv run python -m src.search.indexer

# Start API server
serve:
    uv run uvicorn src.api.app:app --reload --port 9019

# Start API server (production mode)
serve-prod:
    uv run uvicorn src.api.app:app --host 0.0.0.0 --port 9019

# Run unit tests
test-unit:
    uv run pytest tests/unit -v

# Run integration tests (requires running containers)
test-integration:
    uv run pytest tests/integration -v -m integration

# Run smoke tests (requires running API server)
test-smoke:
    uv run pytest tests/smoke -v -m smoke

# Run all tests
test:
    uv run pytest -v

# Full setup: start containers, import data, index, and serve
setup FILE:
    just up
    @echo "Waiting for services to be ready..."
    sleep 5
    just import {{ FILE }}
    just index
    @echo "Setup complete. Run 'just serve' to start the API."

# Quick pipeline: convert XML, import, index
pipeline INPUT:
    just convert {{ INPUT }} data/products.jsonl
    just import data/products.jsonl
    just index
