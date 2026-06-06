## ScheduledTest authoring & window management

## What to build

Implement the Teacher-facing side of ScheduledTest: authoring a test and the data model that the ScheduledTestGatekeeper (next issue) enforces against.

A Teacher creates a ScheduledTest by providing MCQ questions with correct answers, setting an availability window (start and end datetime), configuring per-attempt duration, and setting the number of allowed attempts (defaulting to 1). The test is assigned to all Students in the Teacher's TeacherAssignment.

Each question stores a `question_type` field (always "mcq" in v1) to support future short-answer extension without a schema migration.

Teachers can view full results — submission status and per-student, per-question scores — from the moment the first Student submits, throughout and after the availability window.

## Acceptance criteria

- [ ] `POST /teacher/scheduled-tests` creates a ScheduledTest with: questions (with correct answers), availability window, per-attempt duration, allowed attempts (default 1)
- [ ] Each question record includes a `question_type` field (value "mcq")
- [ ] ScheduledTest is automatically assigned to all Students in the Teacher's TeacherAssignment
- [ ] `GET /teacher/scheduled-tests/{test_id}/results` returns per-student, per-question scores; available from first submission onward
- [ ] Teacher results endpoint is not subject to the answer-reveal restriction that applies to Students
- [ ] Students can list their assigned ScheduledTests with availability window metadata

## Blocked by

- #5 CoachingCenter, Enrollment & TeacherAssignment
