# Vidyasaarthi Backend — Agent Workflow

> Copy this file to `CLAUDE.md` in the `vidyasaarthi-backend` repo root.

---

## Project context

You are working on the **backend** of Vidyasaarthi — an AI-powered CBSE learning platform. The backend is a FastAPI service that both the Student app (React Native) and Teacher Portal (React + Vite) consume.

Before writing any code, read the project documentation:
```bash
gh issue view <issue-number> --repo biswajit-713/vidyasaarthi-documentation
```
Also read `CONTEXT.md` and `ARCHITECTURE.md` from the documentation repo:
```bash
gh api repos/biswajit-713/vidyasaarthi-documentation/contents/CONTEXT.md --jq '.content' | base64 -d
gh api repos/biswajit-713/vidyasaarthi-documentation/contents/ARCHITECTURE.md --jq '.content' | base64 -d
```

## Tech stack

| Layer | Choice |
|---|---|
| Framework | FastAPI (async) |
| ORM | SQLAlchemy (async) |
| Auth | fastapi-users — mobile number as username |
| LLM | LiteLLM (library, not proxy) — call providers directly |
| Vector store | pgvector inside Postgres — HNSW index |
| Migrations | Alembic |
| Runtime | Python 3.12, Docker container |
| Database | Postgres 16 (native on VM, not in Docker) |

## Local dev environment

```bash
docker compose up          # starts FastAPI + Postgres (pgvector) + MinIO
```

- FastAPI: http://localhost:8000
- API docs: http://localhost:8000/docs
- MinIO console: http://localhost:9001
- Environment variables: copy `.env.example` → `.env`, fill in values

The FastAPI container hot-reloads on file save. Do not restart Docker for code changes.

## Workflow for every issue

### 1. Read the spec
```bash
gh issue view <number> --repo biswajit-713/vidyasaarthi-documentation
```
Read every line of **What to build** and **Acceptance criteria** before writing code.

### 2. Create a feature branch
```bash
git checkout -b feature/<short-slug>
# e.g. feature/explanation-session
```

Branch from `main`. Never commit directly to `main`.

### 3. Implement

Follow this order inside each feature:
1. **Database model** — SQLAlchemy model + Alembic migration
2. **Schema** — Pydantic request/response models
3. **Service layer** — business logic, LLM calls, RAG queries
4. **Router** — FastAPI endpoint wiring the service
5. **Tests** — at minimum, test the happy path and the key failure modes

Keep each commit focused on one of these layers. Commit messages must describe what changed, not reference task numbers.

### 4. LLM calls — always go through LiteLLM

```python
from litellm import acompletion  # async; use for all LLM calls

response = await acompletion(
    model="claude-3-5-sonnet-20241022",   # capable model: ExplanationSession, PerformanceReport
    # model="claude-3-haiku-20240307",    # fast model: RevisionSession, lightweight tasks
    messages=[...],
    stream=True,                           # stream=True for student-facing sessions
)
```

Never call provider SDKs directly. Always use LiteLLM so the model can be swapped by config.

### 5. RAG queries — always use pgvector

Retrieve NCERT corpus chunks before generating any explanation or question:
```python
# Use pgvector similarity search to fetch relevant NCERT passages
# Pass retrieved chunks as context in the LLM system prompt
# Never let the LLM explain beyond what the retrieved context covers
```

### 6. Write tests

```bash
pytest                    # run all tests
pytest tests/test_<file>  # run specific file
```

- Tests hit a real test database — do not mock the database.
- Use `pytest-asyncio` for async endpoint tests.
- Each acceptance criterion should map to at least one test.

### 7. Open a PR

```bash
gh pr create \
  --title "<short description>" \
  --body "Part of biswajit-713/vidyasaarthi-documentation#<issue-number>

## What this PR does
<1–3 bullet points>

## Acceptance criteria covered
- [ ] criterion 1
- [ ] criterion 2"
```

Use `Part of` (not `Closes`) if the frontend PR is still outstanding. Use `Closes` only when this PR completes the full slice.

## Code conventions

- **No unnecessary abstractions.** Three similar lines is better than a premature helper.
- **No speculative features.** Build exactly what the acceptance criteria ask for.
- **No comments explaining what the code does.** Name things clearly instead. Only comment on non-obvious WHY — hidden constraints, workarounds, subtle invariants.
- **Domain language.** Use the exact terms from `CONTEXT.md` for all models, variables, and endpoints. Never use synonyms that `CONTEXT.md` marks as _Avoid_.
- **Async throughout.** All database calls, LLM calls, and I/O must be async. No blocking calls in request handlers.
- **Error handling at boundaries only.** Validate user input and external API responses. Trust internal code.

## Definition of done

A slice is done when:
- [ ] All acceptance criteria in the issue are met
- [ ] Tests pass (`pytest`)
- [ ] `docker compose up` still works cleanly
- [ ] PR is open and references the documentation issue
- [ ] No TODO comments left in code
