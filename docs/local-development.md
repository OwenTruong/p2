# Local Development

## Prerequisites

- Docker
- Docker Compose

## Running the Application

From the project root:

```bash
cd p2
```

Create a local environment file:

```bash
cp .env.example .env
```

> Docker Compose automatically loads `.env` from the project root. Alternatively, you can specify a different file using `--env-file`.

Build and start the services:

```bash
docker compose up -d --build
```

To stop the application:

```bash
docker compose down -v
```

---

# Project Notes

## Docker Build Context

Docker Compose uses the **project root** as the build context.

When updating a service's Dockerfile, ensure that all `COPY` instructions are written relative to the project root.

Example:

```dockerfile
COPY services/auth_service/requirements.txt .
COPY shared/ ./shared/
```

---

## Database Initialization

During local development, PostgreSQL initializes the databases using:

```
scripts/dev/init-scripts/create_db.sh
```

This script is responsible only for creating the required databases.

---

## Database Schema

The database schema can be initialized in either of the following ways:

- **Migration scripts**
- **Application startup**

The migration step is currently optional and may be performed manually while the migration workflow is still under development.

---

# Production Deployment

For AKS deployments:

- Database initialization will be handled by a Kubernetes Job.
- Schema migrations are supported but optional for this project.
- Applications may either:
  - apply migrations before startup (recommended), or
  - create the required tables during startup if migrations are not used.