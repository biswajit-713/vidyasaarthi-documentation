# Vidyasaarthi — Development Workflow

## How the project is structured

There are four repositories:

| Repo | What it is |
|---|---|
| `vidyasaarthi-documentation` (this repo) | Specs, domain glossary, ADRs, issue tracker. No runnable code. |
| `vidyasaarthi-backend` | FastAPI service. All business logic, database, LLM calls, RAG. |
| `vidyasaarthi-app` | React Native student app. Mobile only. Students use this. |
| `vidyasaarthi-portal` | React + Vite teacher/admin web portal. Desktop. Teachers and CenterAdmins use this. |

The issue tracker for all work is at:
**https://github.com/biswajit-713/vidyasaarthi-documentation/issues**

---

## What a vertical slice means here

Each GitHub issue is a vertically sliced feature — it describes a complete, working piece of functionality from end to end. "Complete" means a user can actually use it.

Because there are three code repos, a single product feature is often split across multiple issues:

| Feature | Backend issue | Student app issue | Portal issue |
|---|---|---|---|
| Authentication | #3 | #18 | #24 |
| ExplanationSession | #8 | #19 | — |
| MiniTest | #10 | #19 | — |
| TimedTest + ProficiencyLevel | #11 | #20 | — |
| ScheduledTest | #13, #14 | #21 | #26 |
| DailyConcept + RevisionSession | #12 | #22 | #25 |
| StudyNote | #15 | #23 | #25 |
| PerformanceReport | #16 | #23 | — |
| TeacherFlag + WhatsApp nudge | #9 | — | #27 |
| FCM push notifications | #17 | (consumed by app) | — |
| CoachingCenter / Enrollment | #5 | — | #28 |
| NCERT corpus + RAG | #6 | — | — |
| Question bank | #7 | — | — |
| LLM token logging | #29 | — | — |
| Student activity log | #30 | — | — |

---

## Why the backend always comes first

The student app and teacher portal are clients — they call the backend API. A frontend issue cannot be started until the backend endpoint it depends on exists and is merged. This is enforced by the `Blocked by` field on each issue.

For any feature: **finish and merge the backend issue first, then start the frontend issue(s).** Once the backend is done, the app and portal issues for that feature can be developed in parallel.

---

## Development phases

The issues are grouped into phases based on their dependencies. Issues within a phase that don't block each other can be worked in parallel.

### Phase 1 — Infrastructure

| Issue | Repo | Title |
|---|---|---|
| #1 | backend | Local dev environment |
| #2 | backend | GCP production deployment |

Start here. Nothing else can run without #1.

### Phase 2 — Service foundation

| Issue | Repo | Title | Blocked by |
|---|---|---|---|
| #3 | backend | Authentication & identity | #1 |
| #4 | backend | Curriculum structure | #3 |
| #5 | backend | CoachingCenter, Enrollment & TeacherAssignment | #3, #4 |
| #6 | backend | NCERTCorpus ingestion CLI + RAGService | #1 |
| #7 | backend | QuestionBank generation CLI + QuestionBankSampler | #6 |

Once #3 and #4 are done, the frontend scaffold issues (#18, #24) can begin in parallel with the rest of Phase 2.

### Phase 3 — Core feature services (backend)

| Issue | Repo | Title | Blocked by |
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

### Phase 4 — Frontend scaffolds

| Issue | Repo | Title | Blocked by |
|---|---|---|---|
| #18 | app | Student app — scaffold + auth + navigation | #3, #4 |
| #24 | portal | TeacherPortal — scaffold + auth | #3 |

These establish the app shell. All subsequent frontend issues slot feature screens into this scaffold.

### Phase 5 — Student app features

| Issue | Repo | Title | Blocked by |
|---|---|---|---|
| #19 | app | ExplanationSession + MiniTest UI | #8, #10, #18 |
| #20 | app | TimedTest UI | #11, #18 |
| #21 | app | ScheduledTest UI | #14, #18 |
| #22 | app | DailyConcept + RevisionSession UI | #12, #18 |
| #23 | app | PerformanceReport + StudyNote UI | #15, #16, #18 |

### Phase 6 — Teacher Portal features

| Issue | Repo | Title | Blocked by |
|---|---|---|---|
| #25 | portal | DailyConcept + StudyNote UI | #12, #15, #24 |
| #26 | portal | ScheduledTest authoring + results UI | #13, #14, #24 |
| #27 | portal | TeacherFlag + student monitoring UI | #9, #24 |
| #28 | portal | CenterAdmin configuration UI | #5, #24 |

### Phase 7 — Observability

| Issue | Repo | Title | Blocked by |
|---|---|---|---|
| #29 | backend | LLM token usage logging | #8, #12 |
| #30 | backend | Student activity event log | #8, #11, #12, #13, #14 |

Can be developed in parallel with Phases 5 and 6.

---

## How to pick up an issue

1. Open the issue on GitHub: `gh issue view <N> --repo biswajit-713/vidyasaarthi-documentation`
2. Check its `Blocked by` list. Every listed issue must be merged before you start.
3. Identify which repo the issue targets (backend / app / portal).
4. Open Claude Code from inside that repo's directory.
5. Read `CONTEXT.md` and `ARCHITECTURE.md` from this docs repo before writing any code — domain terms in the issue map directly to code names.

Each repo's `CLAUDE.md` describes how to develop within that repo specifically (test setup, implementation order, conventions, definition of done).

---

## Tracking progress

All work is tracked through GitHub:

- **Issue list**: https://github.com/biswajit-713/vidyasaarthi-documentation/issues — open issues are pending, closed issues are done.
- **Pull requests**: each code repo has its own PR list. Every PR references its documentation issue with `Closes #N` or `Part of #N`.
- **A vertical slice is complete** when the backend PR and all frontend PR(s) for that feature are merged, and the documentation issue is closed.

To see what is in progress across all three repos at once, check open PRs in each:
```
https://github.com/biswajit-713/vidyasaarthi-backend/pulls
https://github.com/biswajit-713/vidyasaarthi-app/pulls
https://github.com/biswajit-713/vidyasaarthi-portal/pulls
```
