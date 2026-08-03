#!/usr/bin/env bash

set -euo pipefail

USER="${POSTGRES_USER}"
DATABASES=(
  "${AUTH_DB_NAME:-auth_db_example}"
  "${LISTING_DB_NAME:-listing_db_example}"
  "${RESERVATION_DB_NAME:-reservation_db_example}"
)

echo "Creating databases: ${DATABASES[*]}"

for db in "${DATABASES[@]}"; do
  echo "Now creating db ${db}"
  createdb -U "${USER}" "${db}"
done