#!/bin/bash

set -e

echo "Running Auth Service tests..."
(
    base_directory="services/auth_service"
    python -m pytest $base_directory/tests/unit $base_directory/tests/http
)

echo "Running Listing Service tests..."
(
    base_directory="services/auth_service"
    python -m pytest $base_directory/tests/unit $base_directory/tests/http
)

echo "Running Reservation Service tests..."
(
    base_directory="services/auth_service"
    python -m pytest $base_directory/tests/unit $base_directory/tests/http
)