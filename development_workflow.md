# Vidyasaarthi — Development Workflow

## Before you write a single line of code

All project context lives in the `docs` repo. Read in this order every time you pick up a new issue:

1. `CONTEXT.md` — canonical domain glossary. Every term used in issues and ADRs is defined here. If you use a synonym marked _Avoid_, rewrite it.
2. `ARCHITECTURE.md` — system component map and technology choices.
3. `adr/` — read the ADR(s) relevant to what you are about to build.
4. The GitHub issue for the task:

```bash
gh issue view <number> --repo biswajit-713/vidyasaarthi-documentation
```

**Issue numbers on GitHub are the authoritative reference.** The local markdown filenames in `docs/issues/` were written before the GitHub tracker existed and their numbers do not match. Always use GitHub issue numbers.

---

## The three code repositories

| Repo | Role | Tech |
|---|---|---|
| `vidyasaarthi-backend` | FastAPI service — all business logic, data, LLM, RAG | Python 3.12, FastAPI, SQLAlchemy, Alembic, LiteLLM, pgvector |
| `vidyasaarthi-app` | Student-facing mobile app | React Native / Expo |
| `vidyasaarthi-portal` | Teacher and CenterAdmin web portal | React + Vite, Nginx |

The `docs` repo contains no runnable code. It is the source of truth for specs only.

---

## Why service-first matters

Issues are vertically sliced — each issue delivers a complete end-to-end feature. But within a slice, the service API must exist before the frontend can consume it. Always implement in this order:

```
service (backend) → app and/or portal (frontend)
```

The app and portal never share an issue — frontend issues are repo-specific. Once the service API for a feature is merged, the corresponding app and portal issues can be worked in parallel.

---

## Issue dependency map

The table below shows the recommended implementation sequence. Issues within a phase that share no dependency on each other can be parallelised.

### Phase 1 — Infrastructure (no TDD)

| GitHub issue | Repo | Title | Blocked by |
|---|---|---|---|
| #1 | backend | Local dev environment | — |
| #2 | backend | GCP production deployment | #1 |

Issue #1 is pure infrastructure setup (Docker Compose). There are no acceptance-criteria tests to write — validate it by running `docker compose up` and confirming the checklist.

### Phase 2 — Service foundation

| GitHub issue | Repo | Title | Blocked by |
|---|---|---|---|
| #3 | backend | Authentication & identity | #1 |
| #4 | backend | Curriculum structure | #3 |
| #5 | backend | CoachingCenter, Enrollment & TeacherAssignment | #3, #4 |
| #6 | backend | NCERTCorpus ingestion CLI + RAGService | #1 |
| #7 | backend | QuestionBank generation CLI + QuestionBankSampler | #6 |

### Phase 3 — Core feature services

| GitHub issue | Repo | Title | Blocked by |
|---|---|---|---|
| #8 | backend | ExplanationSession backend | #5, #6 |
| #9 | backend | TeacherFlag + NotificationDispatcher | #8 |
| #10 | backend | MiniTest backend | #7, #8 |
| #11 | backend | ProficiencyEngine + TimedTest backend | #5, #7 |
| #12 | backend | DailyConcept + RevisionSession backend | #5 |
| #13 | backend | ScheduledTest authoring & window management | #5 |
| #14 | backend | ScheduledTestGatekeeper | #13 |
| #15 | backend | StudyNote backend | #5 |
| #16 | backend | PerformanceReport backend | #8, #9, #11 |
| #17 | backend | FCM push notifications | #9, #12, #15 |

### Phase 4 — Frontend scaffolds (can start once Phase 2 is done)

| GitHub issue | Repo | Title | Blocked by |
|---|---|---|---|
| #18 | app | Student app — scaffold + auth + curriculum navigation | #3, #4 |
| #24 | portal | TeacherPortal — scaffold + auth | #3 |

These two can be started as soon as #3 and #4 are done, in parallel with Phase 3.

### Phase 5 — Student app feature UIs

| GitHub issue | Repo | Title | Blocked by |
|---|---|---|---|
| #19 | app | ExplanationSession + MiniTest UI | #8, #10, #18 |
| #20 | app | TimedTest UI | #11, #18 |
| #21 | app | ScheduledTest UI | #14, #18 |
| #22 | app | DailyConcept + RevisionSession UI | #12, #18 |
| #23 | app | PerformanceReport + StudyNote UI | #15, #16, #18 |

### Phase 6 — Teacher Portal feature UIs

| GitHub issue | Repo | Title | Blocked by |
|---|---|---|---|
| #25 | portal | DailyConcept + StudyNote UI | #12, #15, #24 |
| #26 | portal | ScheduledTest authoring + results UI | #13, #14, #24 |
| #27 | portal | TeacherFlag + student monitoring UI | #9, #24 |
| #28 | portal | CenterAdmin configuration UI | #5, #24 |

### Phase 7 — Observability (can be parallelised with Phase 5/6)

| GitHub issue | Repo | Title | Blocked by |
|---|---|---|---|
| #29 | backend | LLM token usage logging | #8, #12 |
| #30 | backend | Student activity event log | #8, #11, #12, #13, #14 |

---

## TDD workflow per issue

Use `/tdd` in Claude Code from within the repo you are working on. Open a Claude Code session rooted at the repo, not at the `docs` directory.

```bash
# example: working on #8 ExplanationSession backend
cd vidyasaarthi-backend
claude
# then invoke /tdd
```

The red-green-refactor cycle maps directly to acceptance criteria:

```
For each acceptance criterion in the issue:
  1. Red   — write a failing test that proves the criterion is not yet met
  2. Green — write the minimum code to make the test pass
  3. Refactor — clean up without changing behaviour; tests must still pass
  4. Commit, move to next criterion
```

**One criterion = one or more tests. Every criterion must have a test before it is implemented.**

### Backend test rules (vidyasaarthi-backend)

- Use `pytest` + `pytest-asyncio`
- Tests hit a real test database — do not mock the database. Mocking hides the exact class of bug (migration errors, constraint violations) most likely to break production.
- Run the target test file while developing: `pytest tests/test_<feature>.py -v`
- Run the full suite before opening a PR: `pytest`

### Frontend test rules (vidyasaarthi-app, vidyasaarthi-portal)

- Tests call a real local backend via `docker compose up` in `vidyasaarthi-backend`
- Do not mock the API. The same reason applies: mock/real divergence masks integration bugs.
- App: React Native Testing Library + Jest
- Portal: React Testing Library + Vitest

---

## Workflow steps for every issue

### 1. Read the spec

```bash
gh issue view <number> --repo biswajit-713/vidyasaarthi-documentation
```

Read every word of **What to build** and **Acceptance criteria** before writing anything.

### 2. Create a feature branch

```bash
git checkout -b feature/<short-slug>
# e.g. feature/explanation-session
```

Branch from `main`. Never commit directly to `main`.

### 3. Invoke /tdd and write tests first

With the issue open, invoke `/tdd` in Claude Code. Provide the issue number. The skill will:
- Derive the test targets from the acceptance criteria
- Guide you through the red-green-refactor loop criterion by criterion

Do not write implementation code until the first test is written and confirmed red.

### 4. Implement in layers (backend only)

Once the first test is failing, implement in this order:

1. SQLAlchemy model + Alembic migration
2. Pydantic request/response schemas
3. Service layer (business logic, LLM calls, RAG queries)
4. FastAPI router (wiring only — no business logic in routers)

Commit after each criterion turns green.

### 5. Open a pull request

```bash
gh pr create \
  --title "<short description>" \
  --body "Part of biswajit-713/vidyasaarthi-documentation#<issue-number>

## What this PR does
- bullet 1
- bullet 2

## Acceptance criteria covered
- [ ] criterion 1
- [ ] criterion 2"
```

Use `Part of` when the full vertical slice (service + frontend) is not yet complete. Use `Closes` only on the last PR that completes the slice.

---

## Definition of done for a vertical slice

A feature is done when all of the following are true:

- [ ] Tests were written before implementation (TDD — enforced by `/tdd`)
- [ ] Every acceptance criterion in the GitHub issue has at least one passing test
- [ ] Full test suite passes in the repo (`pytest` / `jest` / `vitest`)
- [ ] `docker compose up` in `vidyasaarthi-backend` still works cleanly
- [ ] PR is open and references the documentation issue number
- [ ] No TODO comments remain in code
- [ ] For a vertical slice: service PR and frontend PR(s) are both merged

---

## Quick reference: which GitHub issue covers what

| Concern | GitHub issue |
|---|---|
| Authentication (backend) | #3 |
| Authentication (student app) | #18 |
| Authentication (teacher portal) | #24 |
| Curriculum navigation | #4, #18 |
| Student enrollment | #5 |
| NCERT content + RAG | #6 |
| Question bank | #7 |
| ExplanationSession | #8, #19 |
| TeacherFlag + WhatsApp | #9, #27 |
| MiniTest | #10, #19 |
| TimedTest + ProficiencyLevel | #11, #20 |
| DailyConcept + RevisionSession | #12, #22, #25 |
| ScheduledTest | #13, #14, #21, #26 |
| StudyNote | #15, #23, #25 |
| PerformanceReport | #16, #23 |
| Push notifications (FCM) | #17 |
| LLM usage logging | #29 |
| Student activity log | #30 |
