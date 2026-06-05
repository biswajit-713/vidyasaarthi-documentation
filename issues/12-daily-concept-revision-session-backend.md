## DailyConcept + RevisionSession backend

## What to build

Implement DailyConcept posting by Teachers and the RevisionSession triggered when a Student selects a DailyConcept.

A Teacher posts up to 5 Topics as DailyConcepts for the current day, scoped to their TeacherAssignment. Posting is idempotent per (teacher_assignment_id, date). Students see a 7-day rolling window — concepts older than 7 days are filtered out on read. DailyConcepts always point to existing Topics; no free-form content.

A RevisionSession is a single FirstPrinciples pass on a Topic, grounded in NCERTCorpus via RAGService, streamed via SSE. No Pass escalation, no TeacherFlag, no outcome record written.

## Acceptance criteria

- [ ] `POST /teacher/daily-concept` accepts up to 5 topic_ids scoped to the Teacher's TeacherAssignment; idempotent per (teacher_assignment_id, date)
- [ ] `GET /student/daily-concepts` returns only DailyConcepts posted within the last 7 days for the Student's TeacherAssignments
- [ ] DailyConcepts older than 7 days are excluded from the response
- [ ] `POST /sessions/revision` initiates a RevisionSession for a given topic_id; streams a single FirstPrinciples pass via SSE grounded in NCERTCorpus
- [ ] RevisionSession does not advance to a second Pass, does not raise a TeacherFlag, and writes no outcome record
- [ ] Teacher cannot post more than 5 Topics per TeacherAssignment per day; the endpoint rejects excess entries

## Blocked by

- #32 RAGService hybrid retrieval pipeline
- #8 ExplanationSession backend
- #29 LLM token usage logging
- #30 Student activity event log
