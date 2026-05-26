## Student app — DailyConcept + RevisionSession UI

## What to build

Implement the DailyConcept list and RevisionSession screen in the React Native app.

The DailyConcept screen shows Topics posted by the Student's Teacher within the past 7 days, grouped by date. Tapping a Topic launches a RevisionSession — a single-pass SSE chat (FirstPrinciples only). The RevisionSession screen is visually similar to the ExplanationSession screen but has no Pass indicator, no "I don't understand" escalation, and no TeacherFlag outcome. The Student simply reads the explanation and closes the session.

## Acceptance criteria

- [ ] DailyConcept list shows Topics grouped by posted date; concepts older than 7 days are not shown
- [ ] Empty state shown when no DailyConcepts are available
- [ ] Tapping a Topic opens a RevisionSession screen
- [ ] RevisionSession streams a single FirstPrinciples AI response via SSE
- [ ] No "I don't understand" button is shown; no Pass indicator; no TeacherFlag outcome
- [ ] Student can close the RevisionSession at any time

## Blocked by

- #18 Student app scaffold + auth + curriculum navigation
- #12 DailyConcept + RevisionSession backend
