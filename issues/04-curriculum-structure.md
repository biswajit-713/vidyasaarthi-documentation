## Curriculum structure

## What to build

Define the schema and read API for the four curriculum entities: Class, Subject, Chapter, and Topic. Topic is the atom that all student interactions, tests, and performance tracking reference. Seed the database with the CBSE Classes 8–10 NCERT table of contents so that Topics exist before any content features are built.

No write API is needed in v1 — the curriculum is static and managed via seed scripts.

## Acceptance criteria

- [ ] Schema created for Class, Subject, Chapter, Topic with correct relationships (Class → Subject → Chapter → Topic)
- [ ] Read endpoints: list Subjects by Class, list Chapters by Subject, list Topics by Chapter
- [ ] Seed script populates all Classes 8–10, Subjects, Chapters, and Topics from the NCERT table of contents
- [ ] Topics are uniquely addressable by ID
- [ ] Endpoints are accessible to authenticated users of any role

## Blocked by

- #1 Local dev environment
