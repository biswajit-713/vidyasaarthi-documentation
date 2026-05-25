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

## Who is reading this code

The developers on this project come from a **Java Spring** background. They are not Python specialists. When you implement anything non-trivial, you must:

1. **Explain why you chose the approach** — what problem it solves, what the trade-offs are.
2. **Name the Spring equivalent** — e.g. "This is the FastAPI equivalent of a Spring `@Service` bean."
3. **Call out Python idioms that differ from Java** — things like dependency injection via function parameters, decorators instead of annotations, `async/await` semantics, the absence of interfaces, etc.

Do this inline as short comments above the relevant code block. These comments are for the human developer reading the diff — they are educational, not implementation notes. Keep them concise: 2–4 lines maximum per explanation block.

Example of the expected style:
```python
# FastAPI uses Python's type hints for dependency injection — similar to Spring's @Autowired,
# but declared as function parameters instead of field annotations. FastAPI resolves them at
# request time. No IoC container config needed.
async def get_explanation_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user),
):
```

## Tech stack

| Layer | Choice | Spring equivalent |
|---|---|---|
| Framework | FastAPI | Spring Boot + Spring MVC |
| ORM | SQLAlchemy (async) | JPA / Hibernate |
| Schema / validation | Pydantic | Bean Validation (`@Valid`, `@NotNull`) |
| Auth | fastapi-users | Spring Security |
| Migrations | Alembic | Flyway / Liquibase |
| LLM | LiteLLM (library) | No direct equivalent |
| Vector store | pgvector in Postgres | No direct equivalent |
| Runtime | Python 3.12, Docker | JVM, Docker |
| Database | Postgres 16 | Same |

## Local dev environment

```bash
docker compose up          # starts FastAPI + Postgres (pgvector) + MinIO
```

- FastAPI: http://localhost:8000
- API docs: http://localhost:8000/docs  ← auto-generated Swagger UI (like Springdoc)
- MinIO console: http://localhost:9001
- Environment variables: copy `.env.example` → `.env`, fill in values

The FastAPI container hot-reloads on file save. Do not restart Docker for code changes.

## Workflow for every issue

### 1. Read the spec
```bash
gh issue view <number> --repo biswajit-713/vidyasaarthi-documentation
```
Read every line of **What to build** and **Acceptance criteria** before writing any code.

---

### 2. Create a feature branch
```bash
git checkout -b feature/<short-slug>
# e.g. feature/explanation-session
```
Branch from `main`. Never commit directly to `main`.

---

### 3. Write the test first (TDD)

**Always write a failing test before writing implementation code.** This is non-negotiable.

The red-green-refactor cycle:
1. **Red** — write a test that captures one acceptance criterion. Run it. It must fail.
2. **Green** — write the minimum code to make it pass. No more.
3. **Refactor** — clean up without changing behaviour. Tests must still pass.
4. Repeat for the next acceptance criterion.

```bash
pytest tests/test_<feature>.py -v    # run while developing — watch it go red then green
pytest                                # run full suite before opening PR
```

**Test structure per feature:**

```python
# tests/test_explanation_session.py

async def test_create_session_returns_session_id(client, auth_headers):
    # Write this BEFORE implementing the endpoint.
    # It will fail (404) until the endpoint exists — that's correct.
    response = await client.post("/sessions", json={...}, headers=auth_headers)
    assert response.status_code == 201
    assert "id" in response.json()

async def test_session_raises_teacher_flag_after_three_failed_passes(client, auth_headers):
    # Write this BEFORE implementing the flag logic.
    ...
```

- Tests hit a **real test database** — do not mock the database. Mocking the DB masks the exact class of bugs (migration errors, constraint violations) most likely to break production.
- Use `pytest-asyncio` for async tests.
- Each acceptance criterion must have at least one test.

---

### 4. Implement in layers

Once the test is written and failing, implement in this order:

1. **Database model** — SQLAlchemy model + Alembic migration
2. **Schema** — Pydantic request/response models
3. **Service layer** — business logic, LLM calls, RAG queries
4. **Router** — FastAPI endpoint wiring the service

Keep each commit focused on one layer. Commit after each green test.

**Spring → FastAPI layer mapping:**

| Spring | FastAPI equivalent |
|---|---|
| `@Entity` + JPA Repository | SQLAlchemy model + `AsyncSession` |
| `@Service` | Plain Python class or module with async functions |
| `@RestController` + `@RequestMapping` | `APIRouter` with path operation decorators (`@router.post`) |
| `@RequestBody` with `@Valid` | Pydantic model as function parameter — FastAPI validates automatically |
| `@ControllerAdvice` / `@ExceptionHandler` | `@app.exception_handler` or `HTTPException` |
| `application.properties` | `.env` file read via `pydantic-settings` |

---

### 5. LLM calls — always go through LiteLLM

```python
from litellm import acompletion

# Use the capable model for student-facing sessions and report generation.
# Use the fast model for lightweight tasks like RevisionSession Pass 1.
response = await acompletion(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": prompt}],
    stream=True,   # stream=True for all student-facing interactions
)
```

Never call provider SDKs (Anthropic, OpenAI) directly. LiteLLM is the abstraction layer — swapping the model requires changing one config string, not rewriting call sites.

---

### 6. RAG queries — always retrieve before generating

```python
# Before any explanation or question generation:
# 1. Embed the student's query / the topic
# 2. Similarity-search pgvector for relevant NCERT passages
# 3. Pass retrieved passages as context in the system prompt
# The LLM must not explain beyond what the retrieved context covers.
```

---

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

Use `Part of` (not `Closes`) if the frontend PR for this slice is still pending. Use `Closes` only when this PR is the last one completing the full vertical slice.

---

## Code conventions

**Simplicity over cleverness.** This is the most important rule. Write the most straightforward code that satisfies the acceptance criteria. Avoid:
- Generator expressions, list comprehensions nested more than one level deep
- Metaclasses, descriptors, or dynamic attribute tricks
- Decorators that do non-obvious things
- Clever one-liners that require a comment to decode

If a Java developer who has been reading Python for two weeks can't understand your code in 30 seconds, rewrite it.

**Other conventions:**
- **No unnecessary abstractions.** Three similar lines is better than a premature helper.
- **No speculative features.** Build exactly what the acceptance criteria ask for.
- **Domain language.** Use exact terms from `CONTEXT.md`. Never use synonyms marked as _Avoid_.
- **Async throughout.** All DB calls, LLM calls, and I/O must be async. No blocking calls in request handlers.
- **Error handling at boundaries only.** Validate at user input and external API responses. Trust internal code.
- **Educational comments are welcome.** Short comments explaining Spring equivalents or Python idioms are valuable for this team. Keep them to 2–4 lines.

---

## Definition of done

A slice is done when:
- [ ] Tests were written before implementation (TDD)
- [ ] All acceptance criteria in the issue are met
- [ ] Full test suite passes (`pytest`)
- [ ] `docker compose up` still works cleanly
- [ ] PR is open and references the documentation issue
- [ ] No TODO comments left in code
