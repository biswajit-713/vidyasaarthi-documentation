## StudyNote backend

## What to build

Implement the StudyNote feature end-to-end on the backend. A Teacher uploads a PDF (max 20 MB) through the TeacherPortal. The binary is stored in GCS (MinIO in dev). Metadata is stored in Postgres. The Teacher can share the note with all Students in a TeacherAssignment or a named subset. A push notification is dispatched to eligible Students when a note is shared (subject to CenterAdmin toggle). The Teacher can delete a StudyNote — the GCS object is removed, but Students who already downloaded it retain their local copy.

StudyNotes require only a title. An optional Topic or Chapter tag can be attached.

## Acceptance criteria

- [ ] `POST /teacher/study-notes` accepts a multipart PDF upload (max 20 MB), stores binary to GCS/MinIO, writes metadata to Postgres
- [ ] Metadata includes: teacher_id, title, optional topic_id, optional chapter_id, GCS object path, shared scope (full TeacherAssignment or subset of student_ids), created_at
- [ ] `GET /student/study-notes` returns StudyNotes shared with the authenticated Student
- [ ] `GET /student/study-notes/{note_id}/download` returns a signed GCS/MinIO URL for the PDF
- [ ] `DELETE /teacher/study-notes/{note_id}` removes the GCS object and soft-deletes the metadata record; the note no longer appears in Student responses
- [ ] Push notification is dispatched via NotificationDispatcher to eligible Students on share, subject to CenterAdmin StudyNote notification toggle
- [ ] Uploads exceeding 20 MB are rejected with a clear error

## Blocked by

- #8 TeacherFlag + NotificationDispatcher
