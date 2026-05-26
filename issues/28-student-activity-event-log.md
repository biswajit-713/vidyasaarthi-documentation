## Student activity event log

## What to build

Implement a structured `student_activity_event` table that records a lightweight event each time a Student takes a meaningful action. This fills a gap in the current data model: RevisionSession and MiniTest write no database records today, leaving those interactions invisible for operational monitoring.

`student_activity_event` table columns:
- `id`, `created_at`
- `student_id`
- `event_type` — Postgres enum (see below)
- `topic_id` — nullable
- `chapter_id` — nullable
- `metadata` — jsonb; event-specific fields listed below

Event types and their `metadata` fields:

| event_type | metadata fields |
|---|---|
| `explanation_session_started` | `session_id` |
| `explanation_session_closed` | `session_id`, `outcome` (understood \| teacher_flagged), `pass_count` |
| `revision_session_started` | — |
| `mini_test_started` | `source_session_id` |
| `timed_test_submitted` | `score_pct`, `chosen_difficulty`, `proficiency_level_after` |
| `scheduled_test_submitted` | `scheduled_test_id`, `score_pct` |
| `daily_concept_viewed` | `daily_concept_id` |
| `study_note_downloaded` | `study_note_id` |

`ActivityEventLogger` is a thin service with a single `record(student_id, event_type, topic_id, chapter_id, metadata)` method. It is injected as a dependency into each session orchestrator and endpoint handler. Writes are fire-and-forget: the caller does not await the result, so a slow or failed write does not block the primary response path.

The event log is the data source for the inactivity background job in issue #15 — that job should query `student_activity_event` for students with no event in the past N days rather than maintaining separate state.

Three read endpoints, accessible to CenterAdmin (scoped to their CoachingCenter) and PlatformAdmin:

- `GET /admin/activity/students/{student_id}` — paginated event timeline for a student; filterable by `event_type` and date range
- `GET /admin/activity/center/{center_id}/summary` — per-day counts by `event_type` for the center; shows feature utilization breakdown
- `GET /admin/activity/center/{center_id}/low-activity` — students in the center with fewer than N events in the past 7 days; N is configurable

No UI in v1. Endpoints are for direct API access by operators.

## Acceptance criteria

- [ ] `student_activity_event` table exists with all specified columns; `event_type` is a Postgres enum
- [ ] `ActivityEventLogger.record()` writes a row for each of the 8 event types from the correct call site in the respective orchestrator or endpoint
- [ ] `explanation_session_started` is emitted when `POST /sessions/explanation` initiates a session
- [ ] `explanation_session_closed` is emitted on `POST /sessions/explanation/{session_id}/close` with correct `outcome` and `pass_count` in metadata
- [ ] `revision_session_started` is emitted when `POST /sessions/revision` initiates a session (this is the only record written for RevisionSession)
- [ ] `mini_test_started` is emitted when a Student initiates a MiniTest (this is the only record written for MiniTest)
- [ ] `timed_test_submitted` is emitted on a successful `POST /tests/timed/submit` call, after ProficiencyEngine has run; `proficiency_level_after` reflects the updated level
- [ ] `scheduled_test_submitted` is emitted on a successful `POST /tests/scheduled/{test_id}/submit`
- [ ] `daily_concept_viewed` is emitted when a Student fetches a DailyConcept detail
- [ ] `study_note_downloaded` is emitted when a Student calls the signed-URL download endpoint
- [ ] Writes are non-blocking: a failed write is caught, logged to stderr, and does not raise an exception that alters the primary response
- [ ] `GET /admin/activity/students/{student_id}` is accessible to PlatformAdmin and CenterAdmin scoped to their center; returns 403 for cross-center access
- [ ] `GET /admin/activity/center/{center_id}/summary` returns per-day, per-event_type counts; date range filterable
- [ ] `GET /admin/activity/center/{center_id}/low-activity` returns students with fewer than N events in the configurable past-N-days window
- [ ] `ActivityEventLogger` is injected as a dependency; unit tests assert correct `event_type` and `metadata` shape for each trigger using a mock logger

## Blocked by

- #1a Local dev environment
