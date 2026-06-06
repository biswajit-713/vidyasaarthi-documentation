## ProficiencyEngine + TimedTest backend

## What to build

Implement the `ProficiencyEngine` and the TimedTest flow end-to-end.

`ProficiencyEngine.recalculate(current_level, chosen_difficulty, score_pct)` is a pure function with no database dependency. Thresholds (80% for promotion, 40% for demotion) are injected as configurable parameters. Transition rules:

- Beginner ≥80% → Intermediate
- Intermediate ≥80% → Expert
- Expert ≥80% → Expert (no further promotion)
- Intermediate or Expert 40–79% → unchanged
- Expert <40% → Intermediate
- Intermediate or Beginner <40% → Beginner

ProficiencyLevel is stored per (student_id, topic_id), defaulting to Beginner until the first TimedTest is completed for that Topic.

TimedTest flow: Student starts test → questions sampled from QuestionBank at chosen difficulty → questions returned to client (no server state until submit) → Student holds answers client-side → submit or timer expiry triggers single submission call → at-least-one-answer rule enforced → attempt written → ProficiencyEngine recalculation triggered → ProficiencyLevel updated.

## Acceptance criteria

- [ ] `ProficiencyEngine.recalculate()` is a pure function; unit tests cover all 6 transition cells and both configurable threshold boundaries with a table-driven test suite
- [ ] ProficiencyLevel defaults to Beginner for a Student + Topic pair until first TimedTest completion
- [ ] `POST /tests/timed/start` samples questions at the Student's chosen difficulty and returns them; no server-side attempt record is created at this point
- [ ] `POST /tests/timed/submit` enforces at-least-one-answer rule; rejects submissions with no answers; writes attempt record; calls ProficiencyEngine; updates ProficiencyLevel
- [ ] Attempt record stores: student_id, topic_id, chosen_difficulty, score_pct, question_count, timestamp
- [ ] Integration test: full path from submit through ProficiencyEngine recalculation to ProficiencyLevel row update

## Blocked by

- #5 CoachingCenter, Enrollment & TeacherAssignment
- #7 QuestionBank generation CLI + QuestionBankSampler
