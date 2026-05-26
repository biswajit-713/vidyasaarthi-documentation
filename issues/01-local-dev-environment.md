## Local dev environment

## What to build

Set up a Docker Compose environment that runs the full application stack locally. This is the Day 1 development environment — all subsequent backend and frontend issues are developed against this.

The environment must include:
- FastAPI service (Docker container)
- Postgres with the pgvector extension (Docker container)
- MinIO for local GCS-compatible object storage (Docker container, used for StudyNote uploads in place of GCS)

The FastAPI container must be built from the same Dockerfile used in production so that local and production environments are identical. Environment variables (database URL, LLM API keys, MinIO credentials) are managed via a `.env` file excluded from version control.

## Acceptance criteria

- [ ] `docker compose up` starts FastAPI, Postgres (with pgvector), and MinIO with no manual steps
- [ ] FastAPI `/health` endpoint returns 200
- [ ] pgvector extension is confirmed installed in Postgres
- [ ] MinIO console accessible at localhost
- [ ] `.env.example` documents all required environment variables
- [ ] `docker compose down -v` cleanly tears down the environment

## Blocked by

None — can start immediately
