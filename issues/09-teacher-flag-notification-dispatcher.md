## TeacherFlag + NotificationDispatcher

## What to build

Implement TeacherFlag creation and the `NotificationDispatcher` that routes notifications to three transports: in-portal notification store (permanent record), FCM (Student push), and WhatsApp Business API (Teacher nudge).

When a TeacherFlag is raised, the responsible Teacher receives an in-portal notification (always) and a WhatsApp nudge (only if WhatsApp is enabled for the CoachingCenter). The Student sees a transparent message: "We've let your teacher know you need help with this topic."

The NotificationDispatcher checks all relevant CenterAdmin-level toggles before sending. Transports are injected as dependencies — WhatsApp and FCM clients are stubbed in dev. Teacher can mark a flag resolved with an optional note.

TeacherFlag routing is scoped to the TeacherAssignment — only the Teacher assigned to the relevant Subject + Class receives the flag.

## Acceptance criteria

- [ ] TeacherFlag record is created with: student_id, topic_id, teacher_id, raised_at, is_resolved (false), resolved_at (null), resolution_note (null)
- [ ] In-portal notification record is created for the Teacher on every TeacherFlag (regardless of toggles)
- [ ] WhatsApp nudge is sent only when the CoachingCenter has WhatsApp enabled
- [ ] TeacherFlag is routed to the correct Teacher via TeacherAssignment (Subject + Class scoping)
- [ ] `PATCH /teacher/flags/{flag_id}/resolve` marks flag resolved with optional note; sets resolved_at timestamp
- [ ] `GET /teacher/flags` returns only flags scoped to the authenticated Teacher's TeacherAssignment
- [ ] NotificationDispatcher transports are injected as dependencies; unit tests assert correct routing and toggle suppression with mocked transports
- [ ] WhatsApp and FCM clients are stubbed/mocked in the dev environment

## Blocked by

- #8 ExplanationSession backend
