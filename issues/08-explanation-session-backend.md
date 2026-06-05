## ExplanationSession backend

## What to build

Implement the `ExplanationSessionOrchestrator` — the core AI tutoring engine. A Student selects a Topic and enters an ExplanationSession. The orchestrator manages a three-Pass state machine:

- **Pass 1 — FirstPrinciples**: Q&A-led explanation grounded in NCERTCorpus
- **Pass 2 — Elaboration**: Re-explanation using relatable Indian-context examples
- **Pass 3 — Socratic**: Guided questioning toward understanding

Student declares "I understand" at any point → session closes with outcome `understood`. Student declares "I don't understand" → advances to next Pass. Exhausting Pass 3 without understanding → session closes with outcome `teacher_flagged` and triggers TeacherFlag creation.

LLM responses stream token-by-token via Server-Sent Events (SSE). Mid-session conversation state is not persisted — only the final outcome and pass count at close are written to the database.

All LLM calls use the capable-tier model via LiteLLM. All prompts prepend NCERTCorpus passages retrieved via RAGService, scoped to the Student's Class and Subject.

## Acceptance criteria

- [ ] `POST /sessions/explanation` initiates a session and returns session_id and current Pass type
- [ ] `POST /sessions/explanation/{session_id}/message` accepts a student utterance and streams the AI response via SSE; response includes updated pass state
- [ ] `POST /sessions/explanation/{session_id}/close` records the outcome (understood | teacher_flagged) and pass count
- [ ] Declaring "I understand" closes the session with outcome `understood`
- [ ] Declaring "I don't understand" on Pass 1 or 2 advances to the next Pass
- [ ] Declaring "I don't understand" on Pass 3 closes the session with outcome `teacher_flagged`
- [ ] Every LLM prompt is prepended with NCERTCorpus passages from RAGService filtered to the Student's Class and Subject
- [ ] No mid-session conversation is persisted to the database; only outcome and pass count are written on close
- [ ] Unit tests for the Pass state machine covering all transitions and both terminal outcomes

## Blocked by

- #5 CoachingCenter, Enrollment & TeacherAssignment
- #32 RAGService hybrid retrieval pipeline
- #29 LLM token usage logging
- #30 Student activity event log
