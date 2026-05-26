## TeacherPortal — TeacherFlag + student monitoring UI

## What to build

Implement the TeacherFlag list and Student cohort monitoring view in the TeacherPortal.

**TeacherFlag list**: All open and resolved TeacherFlags scoped to the Teacher's TeacherAssignment. Each flag shows the Student name, Topic, and time raised. Teacher can mark a flag as resolved with an optional note. Resolved flags show the resolution note and timestamp.

**Student monitoring**: All Students in the Teacher's TeacherAssignment (not just flagged ones). Per-Student view shows read-only TimedTest scores across Topics and full TeacherFlag history (open and resolved).

## Acceptance criteria

- [ ] TeacherFlag list shows only flags within the Teacher's TeacherAssignment; flags from other TeacherAssignments are never shown
- [ ] Each flag entry shows Student name, Topic name, time raised, and resolution status
- [ ] "Mark resolved" action opens a form with an optional note field; submitting updates the flag
- [ ] Resolved flags show the resolution note and resolved_at timestamp
- [ ] Student cohort list shows all Students in the TeacherAssignment, not only those with open flags
- [ ] Clicking a Student opens a detail view with their TimedTest scores per Topic and full TeacherFlag history
- [ ] TimedTest scores in the Teacher view are read-only

## Blocked by

- #24 TeacherPortal scaffold + auth
- #9 TeacherFlag + NotificationDispatcher
