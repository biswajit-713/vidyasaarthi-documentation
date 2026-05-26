## TeacherPortal — ScheduledTest authoring + results UI

## What to build

Implement ScheduledTest creation and results viewing in the TeacherPortal.

**Authoring**: A form to create a ScheduledTest. Teacher inputs MCQ questions (each with answer options and the correct answer), sets an availability window (start and end datetime), configures per-attempt duration, and sets the number of allowed attempts (defaulting to 1).

**Results**: A results table showing per-student, per-question scores. Available from the first Student submission onward. Teacher sees correct answers at all times (no window restriction for the Teacher view). Students' scores are displayed as they come in.

## Acceptance criteria

- [ ] Create ScheduledTest form captures: questions + correct answers, availability window, per-attempt duration, allowed attempts
- [ ] Allowed attempts defaults to 1 and is editable
- [ ] Created test appears in a list with availability window and status (upcoming / active / closed)
- [ ] Results table is accessible once the first Student submits
- [ ] Results table shows each Student (rows) × each question (columns) with correct/incorrect indicators
- [ ] Teacher can see correct answers in results regardless of whether the availability window has closed
- [ ] Results update without requiring a page refresh (polling or live update)

## Blocked by

- #24 TeacherPortal scaffold + auth
- #14 ScheduledTestGatekeeper
