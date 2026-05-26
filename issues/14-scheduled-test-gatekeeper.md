## ScheduledTestGatekeeper

## What to build

Implement `ScheduledTestGatekeeper` — the pure logic layer that enforces all ScheduledTest rules on the Student side. Contains no I/O; clock and attempt repository are injected as dependencies.

Rules enforced:
1. A Student cannot start a new attempt after the availability window has closed
2. A submission is rejected if the availability window has closed at the time of submission
3. Correct answers are withheld from the Student response payload until after the availability window closes
4. Attempt count is tracked and enforced; no new attempt is allowed once the limit is reached

Timer expiry triggers an auto-submit via a client-initiated call. The server validates window state at receipt — if the window has closed, the submission is rejected and no record is written.

ScheduledTest scores do not affect ProficiencyLevel.

## Acceptance criteria

- [ ] `POST /tests/scheduled/{test_id}/start` is rejected if the availability window has closed or the Student's attempt limit is reached
- [ ] `POST /tests/scheduled/{test_id}/submit` is rejected if the availability window has closed at submission time; no attempt record is written on rejection
- [ ] On successful submission, score is returned immediately; correct answers are omitted from the response until the window closes
- [ ] After the availability window closes, correct answers are included in the results response
- [ ] Attempt count is incremented on each accepted submission; subsequent starts are blocked once the limit is reached
- [ ] ScheduledTest score is stored but does not trigger ProficiencyEngine or update ProficiencyLevel
- [ ] Integration test: full path through gatekeeper to attempt record; window-closed rejection path writes no record
- [ ] Unit tests for all gatekeeper rules using mocked clock and mocked attempt repository

## Blocked by

- #13 ScheduledTest authoring & window management
- #30 Student activity event log
