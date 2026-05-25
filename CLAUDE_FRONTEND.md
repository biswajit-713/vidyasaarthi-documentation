# Vidyasaarthi Frontend — Agent Workflow

> Copy this file to `CLAUDE.md` in the `vidyasaarthi-frontend` repo root.

---

## Project context

You are working on the **frontend** of Vidyasaarthi — an AI-powered CBSE learning platform. The frontend has two surfaces sharing one backend API:

| Surface | Stack | Users |
|---|---|---|
| Student App | React Native + Expo | Students (mobile) |
| Teacher Portal | React + Vite | Teachers, CenterAdmins (desktop web) |

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
| Student App | React Native + Expo |
| Teacher Portal | React + Vite |
| State management | TBD per surface (document in ADR if non-trivial) |
| Push notifications | Firebase FCM (student app only) |
| Auth | Mobile number + password / OTP via backend API |

## Local dev environment

```bash
# Student App
cd student-app
npx expo start

# Teacher Portal
cd teacher-portal
npm run dev        # http://localhost:5173
```

The backend must be running for API calls to work:
```bash
# In vidyasaarthi-backend:
docker compose up
```

Backend base URL for local dev: `http://localhost:8000`

## Workflow for every issue

### 1. Read the spec
```bash
gh issue view <number> --repo biswajit-713/vidyasaarthi-documentation
```
Read every line of **What to build** and **Acceptance criteria** before writing code. Pay attention to the exact domain terms used — they map directly to API endpoints and data models.

### 2. Verify the backend API is available

Frontend issues depend on backend issues being merged first. Before starting UI work, confirm the relevant endpoints exist:
```bash
curl http://localhost:8000/docs   # check Swagger UI for available endpoints
```

If the backend endpoint doesn't exist yet, the backend issue must be completed first. Do not mock or hardcode data to work around a missing API.

### 3. Create a feature branch
```bash
git checkout -b feature/<short-slug>
# e.g. feature/explanation-session-ui
```

Branch from `main`. Never commit directly to `main`.

### 4. Implement

Follow this order inside each feature:
1. **API client** — typed functions that call the backend endpoints
2. **Screen/component** — UI that calls the API client
3. **Navigation wiring** — register new screens in the navigator
4. **Push notification handling** — only if the spec requires it

Keep each commit focused on one of these layers.

### 5. Streaming responses (ExplanationSession, RevisionSession)

The backend streams LLM responses as Server-Sent Events (SSE). Render tokens as they arrive — do not wait for the full response before displaying anything. Use the `EventSource` API or an SSE client library.

### 6. Offline / network failure handling

Per the spec, on network failure during test submission (TimedTest, ScheduledTest), the test is **discarded** — do not retry silently or queue for later. Show the user an explicit message and allow a fresh attempt.

### 7. Domain language in UI copy

Use the exact terms from `CONTEXT.md` in all user-visible text. The `_Avoid_` list in `CONTEXT.md` is a hard constraint — those words must not appear in the UI.

| Use | Never use |
|---|---|
| ExplanationSession | Tutoring session, doubt session |
| TimedTest | Quiz, assessment, exam |
| ScheduledTest | Class test, exam |
| TeacherFlag | Alert, escalation |
| DailyConcept | Daily update, lesson post |
| StudyNote | Notes, material, handout |
| ProficiencyLevel | Level, skill level |

### 8. Open a PR

```bash
gh pr create \
  --title "<short description>" \
  --body "Closes biswajit-713/vidyasaarthi-documentation#<issue-number>

## What this PR does
<1–3 bullet points>

## Acceptance criteria covered
- [ ] criterion 1
- [ ] criterion 2"
```

Use `Closes` when this PR is the last one completing the full slice (i.e., backend is already merged). This auto-closes the documentation issue.

## Code conventions

- **No unnecessary abstractions.** Build exactly what the acceptance criteria ask for.
- **No speculative features.** Do not add screens, settings, or behaviours not mentioned in the spec.
- **No comments explaining what the code does.** Name things clearly. Only comment on non-obvious constraints or workarounds.
- **Domain language in code too.** Component names, function names, and variable names should use the same terms as `CONTEXT.md`. `ExplanationSessionScreen`, not `TutoringScreen`.
- **No mocked data in merged code.** Placeholder data is acceptable during development but must be removed before the PR is opened.
- **Test on device / simulator.** Run the feature on an actual iOS/Android simulator before opening the PR. Do not rely only on type checking.

## Definition of done

A slice is done when:
- [ ] All acceptance criteria in the issue are met
- [ ] Feature runs without errors on iOS and Android simulators (student app) or Chrome (teacher portal)
- [ ] No hardcoded / mocked data remains
- [ ] Domain language in `CONTEXT.md` is respected in all UI copy
- [ ] PR is open and references the documentation issue with `Closes #<N>`
- [ ] No TODO comments left in code
