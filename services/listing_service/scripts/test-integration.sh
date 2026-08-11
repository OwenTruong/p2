#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/services/listing_service/docker-compose.test.yml"

cleanup() {
  docker compose \
    -f "$COMPOSE_FILE" \
    down -v --remove-orphans
}

trap cleanup EXIT

cd "$PROJECT_ROOT"

docker compose \
  -f "$COMPOSE_FILE" \
  up -d --remove-orphans

until docker compose \
  -f "$COMPOSE_FILE" \
  exec -T test_postgresql \
  pg_isready -U postgres -d listing_test_db
do
  sleep 1
done

export DB_HOST=localhost
export DB_PORT=5433
export DB_NAME=listing_test_db
export DB_USER=postgres
export DB_PASSWORD=postgres
export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5433/listing_test_db"

export PYTHONPATH="$PROJECT_ROOT/services/listing_service:$PROJECT_ROOT"

python -m app.migrate
pytest services/listing_service/tests/integration -v