# Vidyasaarthi Frontend — Agent Workflow

> Copy this file to `CLAUDE.md` in the respective frontend repo root.

---

## Project context

You are working on the **frontend** of Vidyasaarthi — an AI-powered CBSE learning platform. There are two separate frontend repos:

| Repo | Stack | Users |
|---|---|---|
| `vidyasaarthi-student-app` | React Native + Expo | Students (mobile) |
| `vidyasaarthi-teacher-portal` | React + Vite | Teachers, CenterAdmins (desktop web) |

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

The developers on this project are **backend developers** (primarily Java/Python) with **basic React knowledge in JavaScript** and **no prior TypeScript experience**. They understand components, props, and useState, but are not fluent in React patterns or TypeScript's type system.

When you implement anything, you must:

1. **Explain what you built and why** — describe the React/TypeScript concept involved, not just what the code does.
2. **Connect it to backend concepts they already know** — e.g. "A React component is like a method that returns HTML. Props are like method parameters."
3. **Explain TypeScript constructs inline** — interfaces, generics, union types, type narrowing, etc., the first time they appear in the file.
4. **Flag React-specific behaviour** that surprises backend developers — re-renders, stale closures, effect cleanup, dependency arrays.

Do this as short comment blocks above the relevant code. Keep each explanation to 3–5 lines — enough to teach, not so much that it overwhelms.

Example of the expected style:
```tsx
// In TypeScript, interfaces define the "shape" of an object — similar to a Java interface
// but used for data, not behaviour. Props are typed with an interface so TypeScript catches
// missing or wrong-typed props at compile time instead of at runtime.
interface ExplanationSessionScreenProps {
  topicId: string;
  onComplete: () => void;
}

// A React component is a function that returns JSX (HTML-like syntax).
// Every time props or state change, React calls this function again and re-renders the UI.
export function ExplanationSessionScreen({ topicId, onComplete }: ExplanationSessionScreenProps) {
```

## Tech stack

| Layer | Choice |
|---|---|
| Student App | React Native + Expo |
| Teacher Portal | React + Vite |
| Language | TypeScript (strict mode) |
| Push notifications | Firebase FCM (student app only) |
| Auth | Mobile number + password / OTP via backend API |

## Local dev environment

```bash
# Student App
npx expo start          # scan QR code with Expo Go, or press i/a for simulator

# Teacher Portal
npm run dev             # http://localhost:5173
```

The backend must be running for API calls to work:
```bash
# In vidyasaarthi-backend repo:
docker compose up       # backend at http://localhost:8000
```

## Workflow for every issue

### 1. Read the spec
```bash
gh issue view <number> --repo biswajit-713/vidyasaarthi-documentation
```
Read every line of **What to build** and **Acceptance criteria** before writing code. Domain terms in the spec map directly to component names, function names, and API calls.

---

### 2. Verify the backend API is available

Frontend issues depend on backend issues being merged first. Before writing any UI code:
```bash
curl http://localhost:8000/docs   # check Swagger UI for the required endpoints
```

If the endpoint doesn't exist yet, the backend issue must be completed first. Do not mock or hardcode data to work around a missing API.

---

### 3. Create a feature branch
```bash
git checkout -b feature/<short-slug>
# e.g. feature/explanation-session-ui
```
Branch from `main`. Never commit directly to `main`.

---

### 4. Write the test first (TDD)

**Always write a failing test before writing any component or logic.** This applies to UI code too.

The red-green-refactor cycle:
1. **Red** — write a test that captures one acceptance criterion. Run it. It must fail.
2. **Green** — write the minimum code to make it pass.
3. **Refactor** — clean up without changing behaviour. Tests must still pass.
4. Repeat for the next acceptance criterion.

For React Native (student app), use **React Native Testing Library**:
```tsx
// tests/ExplanationSessionScreen.test.tsx
// Write this BEFORE building the screen.

import { render, fireEvent, waitFor } from '@testing-library/react-native';

test('shows Pass 1 content after session starts', async () => {
  // This will fail until the component exists — that's correct.
  const { getByText } = render(<ExplanationSessionScreen topicId="t1" />);
  await waitFor(() => expect(getByText(/explain/i)).toBeTruthy());
});
```

For the Teacher Portal, use **Vitest + React Testing Library**:
```tsx
// tests/DailyConceptForm.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

it('disables submit when no topics are selected', () => {
  render(<DailyConceptForm />);
  expect(screen.getByRole('button', { name: /post/i })).toBeDisabled();
});
```

Each acceptance criterion must have at least one test.

---

### 5. Implement in layers

Once the test is written and failing, implement in this order:

1. **TypeScript types** — define the shape of API responses and component props
2. **API client function** — typed `fetch` or `axios` call to the backend endpoint
3. **Component** — UI that calls the API client and renders the result
4. **Navigation wiring** — register new screens in the navigator (student app only)
5. **Push notification handler** — only if the spec requires it

Keep each commit focused on one layer.

---

### 6. TypeScript — key concepts to apply

**Always type API responses.** Define an interface matching the backend's response shape:
```typescript
// This interface mirrors the JSON the backend returns.
// TypeScript will catch typos and missing fields at compile time.
interface ExplanationSession {
  id: string;
  topicId: string;
  currentPass: 'FirstPrinciples' | 'Elaboration' | 'Socratic';  // union type — one of these values only
  status: 'active' | 'understood' | 'flagged';
}
```

**Never use `any`.** `any` turns off TypeScript's checks entirely — it defeats the purpose of using TypeScript. Use `unknown` if the type is genuinely unknown, then narrow it.

**Use `async/await` for all API calls**, not `.then()` chains:
```typescript
// Preferred: reads like synchronous code, easier to follow for backend devs
const session = await createExplanationSession(topicId);

// Avoid: .then() chains are harder to read and debug
createExplanationSession(topicId).then(session => { ... });
```

---

### 7. React — concepts to understand and apply

**State (`useState`) is like a field that triggers a re-render when changed.**
```tsx
// When setIsLoading is called, React re-runs this component function and updates the UI.
// Unlike a regular variable, changes to state are visible to the user.
const [isLoading, setIsLoading] = useState(false);
```

**Effects (`useEffect`) run after render — use for API calls and subscriptions.**
```tsx
// This is like @PostConstruct in Spring — runs once after the component mounts.
// The empty array [] means "run once only". Dependencies in the array mean "re-run when these change".
useEffect(() => {
  loadSession(topicId);
}, [topicId]);
```

**Keep components small and focused.** One screen = one file. Extract a child component when a section of JSX grows beyond ~50 lines or when it needs its own state.

---

### 8. Streaming responses (ExplanationSession, RevisionSession)

The backend streams LLM tokens as Server-Sent Events (SSE). Render each token as it arrives — do not buffer the full response before displaying:
```typescript
// SSE is like a long-lived HTTP response that sends chunks of data over time.
// Each chunk is one token of the AI's response. We append it to state as it arrives
// so the student sees the text appear word by word, like ChatGPT.
```

---

### 9. Network failure during test submission

Per the spec, if the network is unavailable when a TimedTest or ScheduledTest is submitted, the test is **discarded**. Do not retry silently or queue for later. Show an explicit message and let the student start a fresh attempt.

---

### 10. Domain language in UI copy

Use exact terms from `CONTEXT.md`. The `_Avoid_` list is a hard constraint — those words must not appear in the UI.

| Use | Never use |
|---|---|
| ExplanationSession | Tutoring session, doubt session |
| TimedTest | Quiz, assessment, exam |
| ScheduledTest | Class test, exam |
| TeacherFlag | Alert, escalation |
| DailyConcept | Daily update, lesson post |
| StudyNote | Notes, material, handout |
| ProficiencyLevel | Level, skill level |

---

### 11. Open a PR

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

Use `Closes` when this PR is the last one completing the full vertical slice.

---

## Code conventions

**Simplicity over cleverness.** This is the most important rule. The audience is backend developers who are still building their React/TypeScript fluency. Write the most straightforward code that satisfies the acceptance criteria. Avoid:
- Chained `.map().filter().reduce()` pipelines — break them into named steps
- Generic utility components that try to handle every case — build for the case at hand
- Complex custom hooks when `useState` + `useEffect` inline does the job
- Ternary expressions nested more than one level deep

If a developer who knows Java but is new to React can't follow your component in 30 seconds, simplify it.

**Other conventions:**
- **No unnecessary abstractions.** Build exactly what the acceptance criteria ask for.
- **No speculative features.** No extra screens, settings, or behaviours not in the spec.
- **Domain language in code.** `ExplanationSessionScreen`, not `TutoringScreen`. Component names mirror `CONTEXT.md` terms.
- **No mocked data in merged code.** Placeholder data during development is fine, but remove it before the PR.
- **Educational comments are welcome.** Short explanations of React/TypeScript concepts are valuable for this team.

---

## Definition of done

A slice is done when:
- [ ] Tests were written before implementation (TDD)
- [ ] All acceptance criteria in the issue are met
- [ ] Full test suite passes
- [ ] Feature runs without errors on iOS and Android simulators (student app) or Chrome (teacher portal)
- [ ] No hardcoded / mocked data remains
- [ ] No `any` types remain
- [ ] Domain language from `CONTEXT.md` is respected in all UI copy and code names
- [ ] PR is open with `Closes biswajit-713/vidyasaarthi-documentation#<N>`
- [ ] No TODO comments left in code
