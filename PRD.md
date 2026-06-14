# Vidyasaarthi — Product Requirements Document

## Problem Statement

Students in CBSE Classes 8–10 attending coaching centers lack personalised, on-demand academic support between scheduled classes. Teachers have no lightweight mechanism to extend their reach — sharing concepts covered in class, distributing study material, or identifying students who are genuinely struggling with specific topics. The gap between classroom instruction and individual student comprehension is invisible until exam performance reveals it, by which point remediation is costly and time-constrained.

Coaching centers, as the distribution channel, have no tooling to manage this gap at scale. They operate without visibility into per-student, per-topic understanding — only aggregate test scores are available, and those arrive late.

---

## Solution

Vidyasaarthi is an AI-powered learning platform distributed through coaching centers. Students interact with an AI tutor via a React Native mobile app. The AI explains NCERT content through structured, multi-pass ExplanationSessions grounded strictly in the NCERTCorpus, assesses understanding through MiniTests and TimedTests, and tracks ProficiencyLevel per Topic per Student. When a Student exhausts all explanation attempts, a TeacherFlag is raised — surfacing the exact Topic and Student to the responsible Teacher in near-real time.

Teachers use a web-based TeacherPortal to post DailyConcepts, upload StudyNotes, author ScheduledTests, monitor student performance, and resolve TeacherFlags. CenterAdmins manage enrollment, TeacherAssignments, and CoachingCenter configuration. All AI interactions are constrained to NCERT scope via RAG over an ingested NCERTCorpus; no AI response goes beyond the authoritative textbook content.

The platform launches at 20–30 users and is designed to scale to 100 users in its initial phase.

---

## User Stories

### Student — ExplanationSession and Passes

1. As a Student, I can browse Topics within any Chapter of my enrolled Subjects so that I can select a Topic I want to understand.
2. As a Student, when I start an ExplanationSession on a Topic, I receive a FirstPrinciples Pass — a Q&A-led AI explanation grounded in NCERTCorpus — so that I encounter the concept from first principles before anything else.
3. As a Student, when I type "I don't understand" during the FirstPrinciples Pass, the session advances to the Elaboration Pass, where the AI re-explains the Topic using relatable, Indian-context examples drawn from NCERTCorpus, so that I get a different angle on the same concept.
4. As a Student, when I type "I don't understand" during the Elaboration Pass, the session advances to the Socratic Pass, where the AI uses guided questioning to lead me toward understanding, so that I have a third and qualitatively different attempt.
5. As a Student, when I type "I understand" at any point during an ExplanationSession, the session ends and I am offered the option to proceed to a MiniTest, so that I can immediately verify my understanding.
6. As a Student, if I exhaust all three Passes without declaring understanding, I see a transparent message explaining that a TeacherFlag has been raised and my Teacher has been notified, so that I am not left without recourse.
7. As a Student, I understand that ExplanationSession state is not persisted mid-session — if I leave and return, I must start a new session — so that I have clear expectations about continuity.
8. As a Student, AI responses during an ExplanationSession stream to my screen in real time via SSE so that I am not waiting at a blank screen for a full response to arrive.

### Student — MiniTest

9. As a Student, after declaring understanding in an ExplanationSession, I can choose to take a MiniTest on that Topic so that I can self-check my comprehension immediately.
10. As a Student, the MiniTest is ungraded and untimed, so I can attempt it at my own pace without performance pressure.
11. As a Student, during a MiniTest I can ask the AI to explain any question further, so that the test itself becomes a learning moment rather than a pure assessment.
12. As a Student, MiniTest questions are drawn from the QuestionBank for the relevant Topic so that questions are aligned to NCERT content.

### Student — TimedTest

13. As a Student, I can start a TimedTest on any Topic within my enrolled Subjects so that I can assess my understanding under timed conditions.
14. As a Student, the TimedTest pre-selects a difficulty level matching my current ProficiencyLevel for that Topic, but I can override this before starting so that I have agency over the challenge level.
15. As a Student, my answers are held client-side until I explicitly submit or the timer expires, so that a partial network failure mid-test does not cause accidental submission.
16. As a Student, if the network fails at the moment I submit a TimedTest, the attempt is discarded rather than recorded with incomplete data, so that my performance record remains accurate.
17. As a Student, a TimedTest attempt is only recorded if I have answered at least one question, so that accidental or aborted openings do not pollute my performance history.
18. As a Student, after a TimedTest my ProficiencyLevel for that Topic is recalculated immediately based on my score and the difficulty I chose, so that future sessions and tests reflect my current level.

### Student — ScheduledTest

19. As a Student, I can see and attempt ScheduledTests assigned to me by my Teacher within the availability window set by the Teacher, so that I complete assessed tests on the Teacher's schedule.
20. As a Student, when the ScheduledTest timer expires, the test is auto-submitted so that I do not need to manually submit under pressure.
21. As a Student, if the network fails at submission time for a ScheduledTest, my attempt is discarded, so that incomplete data is not recorded against me.
22. As a Student, I see my score immediately after submitting a ScheduledTest, but correct answers are only revealed after the availability window closes, so that other Students cannot benefit from my early submission.
23. As a Student, I cannot submit a ScheduledTest after the availability window has closed, so that the assessment is conducted fairly within the intended period.
24. As a Student, I can attempt a ScheduledTest up to the number of attempts the Teacher has configured (defaulting to one), so that my attempts are bounded as the Teacher intends.

### Student — DailyConcept and RevisionSession

25. As a Student, I can see DailyConcepts posted by my Teacher for up to the past 7 days, so that I have a rolling window of recently taught Topics to revise.
26. As a Student, DailyConcepts older than 7 days are no longer shown to me, so that the interface stays focused on recent material.
27. As a Student, when I select a DailyConcept, I enter a RevisionSession — a single FirstPrinciples pass on that Topic — so that I can quickly revisit what was covered in class.
28. As a Student, a RevisionSession does not escalate to further Passes or raise a TeacherFlag — it is a single interaction — so that it remains a lightweight revision tool.

### Student — StudyNotes

29. As a Student, I receive a push notification when my Teacher shares a new StudyNote with me (if the CenterAdmin has enabled this notification type), so that I am aware of new material promptly.
30. As a Student, I can download any StudyNote shared with me, so that I can study offline.

### Student — PerformanceReport

31. As a Student, I can view my PerformanceReport, which shows my last 5 TimedTest results across Topics, so that I have a summary view of recent performance.
32. As a Student, I can drill into any Topic in my PerformanceReport to see up to my last 10 TimedTest results for that Topic, so that I can track my progress over time on specific Topics.
33. As a Student, my PerformanceReport includes an AI-generated narrative identifying my strong and weak Topics, nudging me toward revision, and commenting on my study consistency, so that I receive personalised guidance rather than raw numbers alone.
34. As a Student, my PerformanceReport shows ScheduledTest results as raw scores in a separate "Class Tests" section with no AI commentary, so that Teacher-assessed tests are presented distinctly from self-directed learning activity.

### Student — Notifications and Settings

35. As a Student, I can toggle my inactivity reminder notification on or off, so that I control whether I am nudged when I have not used the platform for N days.
36. As a Student, I log in using my mobile number and either a password or a one-time password (OTP), so that authentication is simple and does not require a separate username.

### Teacher — DailyConcept

37. As a Teacher, I can post up to 5 Topics as DailyConcepts for today's class, once per day, for each of my TeacherAssignments, so that my Students know exactly which Topics were covered in that session.
38. As a Teacher, DailyConcepts I post always point to existing Topics in the curriculum rather than free-form text, so that they remain anchored to NCERT content.

### Teacher — StudyNotes

39. As a Teacher, I can upload a PDF StudyNote (up to 20 MB) and share it with all Students in a TeacherAssignment or a subset of those Students, so that I can distribute material at the granularity I choose.
40. As a Teacher, I can optionally tag a StudyNote with a Topic or Chapter, so that Students can contextualise the material within the curriculum.
41. As a Teacher, I can delete a StudyNote I have previously uploaded, so that I can remove outdated or erroneous material.

### Teacher — ScheduledTest

42. As a Teacher, I can author a ScheduledTest as an MCQ test over one or more Topics, assign it to all Students in a TeacherAssignment, set an availability window, configure per-attempt duration, and set the number of allowed attempts, so that I can conduct structured assessments on my own schedule.
43. As a Teacher, the default number of allowed attempts for a ScheduledTest is 1, so that I do not need to explicitly configure this for the most common case.
44. As a Teacher, I can see full ScheduledTest results from each Student's first submission as soon as they submit, so that I have immediate visibility even while the window is still open.
45. As a Teacher, correct answers are not revealed to Students until the availability window closes, so that late-sitting Students cannot benefit from early-sitter disclosures.

### Teacher — TeacherFlags and Student Monitoring

46. As a Teacher, I receive an in-portal notification (permanent record) when a TeacherFlag is raised for a Student on a Topic within my TeacherAssignment, so that I am aware of exactly which Student is struggling with exactly which Topic.
47. As a Teacher, if WhatsApp notifications are enabled for my CoachingCenter, I also receive a WhatsApp nudge when a TeacherFlag is raised, so that I am notified even when I am not actively in the portal.
48. As a Teacher, I can mark a TeacherFlag as resolved with an optional note, so that I can record that I have followed up with the Student.
49. As a Teacher, I can view all Students in my TeacherAssignment — not only flagged Students — along with their read-only TimedTest scores and TeacherFlag history, so that I maintain visibility across my full cohort.

### CenterAdmin — Enrollment and Configuration

50. As a CenterAdmin, I can enroll a Student into specific Subjects at my CoachingCenter, so that the Student has access to exactly the curriculum areas relevant to them.
51. As a CenterAdmin, I can onboard Teachers and create TeacherAssignments mapping each Teacher to a Subject+Class combination at my CoachingCenter, so that the right Teacher is accountable for the right set of Students and Topics.
52. As a CenterAdmin, I can configure TimedTest settings — specifically question count and duration — for my CoachingCenter, so that tests are calibrated to the expectations of my center.
53. As a CenterAdmin, I can toggle push notification types (DailyConcept posted, TeacherFlag resolved, new StudyNote shared) on or off for my CoachingCenter, so that notification volume is appropriate for my context.
54. As a CenterAdmin, I can toggle WhatsApp notifications on or off for my CoachingCenter, so that Teachers receive WhatsApp nudges only if this channel is appropriate for my center.

### PlatformAdmin — Bootstrap

55. As a PlatformAdmin, I can create and configure a new CoachingCenter on the platform, so that a new partner institution can be onboarded.
56. As a PlatformAdmin, I perform CenterAdmin functions on behalf of a CoachingCenter before a dedicated CenterAdmin is in place, so that the platform is usable from the very first day of onboarding.
57. As a PlatformAdmin, I can configure ProficiencyLevel recalculation thresholds globally, so that the scoring rules can be adjusted without a code change.

### Edge Cases and Cross-Cutting Stories

58. As a Student, if I am mid-ExplanationSession and my app crashes or I close it, I return to a clean state with no mid-session data persisted, so that there is no corrupt or partial session record.
59. As a Student, the AI tutor communicates exclusively in plain, accessible English using Indian-context examples, and never introduces content outside the NCERT scope of my Class, so that explanations are always relevant and age-appropriate.
60. As a Student, if I open a ScheduledTest attempt and the availability window closes before I submit, my submission is rejected, so that results after the window cannot be recorded.
61. As a Teacher, TeacherFlags for Topics outside my TeacherAssignment are never surfaced to me, so that I am not overwhelmed with flags irrelevant to my teaching scope.
62. As a CenterAdmin, Student ProficiencyLevel defaults to Beginner for every Topic until the Student has completed their first TimedTest on that Topic, so that the default state is always defined.

---

## Implementation Decisions

### Deep Modules

**RAGService**
Interface: `retrieve(query: str, subject_id: int, chapter_id: int | None = None, top_k: int) → List[Passage]`
Hybrid retrieval pipeline: (1) BM25 keyword search (bm25s, top-50) and semantic ANN search (pgvector + bge-large-en-v1.5 embeddings, top-50) run sequentially; (2) Reciprocal Rank Fusion merges both lists to top-20; (3) cross-encoder reranking (bge-reranker-base, plain PyTorch) reduces to top-k. No LLM dependency — retrieval is fully separable from generation. All ExplanationSession and RevisionSession prompts are constructed by prepending retrieved Passages to the LLM call. `subject_id` is always applied as a filter on the pgvector search. `chapter_id` is an optional filter: when provided and `filter_by_chapter=True` (the default), retrieval is scoped to that chapter — ExplanationSession and RevisionSession always pass it; the QuestionBank CLI passes `None`. `filter_by_chapter` is a constructor parameter (default True) wired from config; setting it to False on a second RAGService instance enables A/B comparison of retrieval quality without client changes or service restarts. Stage cardinalities (BM25_TOP_N, SEMANTIC_TOP_N, RRF_TOP_N) are configurable constants.

**ProficiencyEngine**
Interface: `recalculate(current_level: ProficiencyLevel, chosen_difficulty: ProficiencyLevel, score_pct: float) → ProficiencyLevel`
Pure function encoding the score-based rule:
- Beginner, score ≥80% → Intermediate
- Intermediate, score ≥80% → Expert
- Expert, score ≥80% → Expert (no further promotion)
- Intermediate or Expert, 40–79% → unchanged
- Expert, score <40% → Intermediate
- Intermediate or Beginner, score <40% → Beginner

Thresholds (80%, 40%) are injected as configurable parameters rather than hardcoded, enabling PlatformAdmin adjustment without deployment. No database dependency — fully unit-testable with a table-driven test suite covering all transition cells.

**QuestionBankSampler**
Interface: `sample(topic_id: UUID, proficiency_level: ProficiencyLevel, count: int) → List[Question]`
Queries the QuestionBank by Topic and ProficiencyLevel, samples `count` questions randomly. The QuestionBank is populated offline by a standalone CLI script pre-launch; no admin UI exists in v1. The MiniTest question source is abstracted behind a configurable interface so that a future LLM-backed question generator can be substituted without changing callers.

**ExplanationSessionOrchestrator**
Owns the Pass state machine: Pass1 (FirstPrinciples) → Pass2 (Elaboration) → Pass3 (Socratic) → TeacherFlag. On each student utterance, evaluates whether the student has declared understanding or non-understanding and transitions accordingly. Streams LLM responses back to the Student app via FastAPI SSE. On exhaustion of Pass3 without understanding, immediately calls NotificationDispatcher to raise a TeacherFlag — this happens during the advance-pass call the moment the session becomes terminal, before the done SSE event is emitted to the client. This ensures the transparent message ("We've let your teacher know") is truthful when the Student sees it. The session outcome (teacher_flagged) is written to the database on the subsequent /close call. No mid-session state is persisted to the database — only the final outcome (understood or TeacherFlag) is written on session close. Uses the capable-tier LLM (via LiteLLM library) for all passes.

**PerformanceNarrativeGenerator**
Aggregates four signals per Student: (1) TimedTest scores by Topic, (2) ExplanationSession pass counts by Topic, (3) TeacherFlags raised by Topic, (4) activity frequency over a trailing period. Signal aggregation is a pure function and testable without any LLM. The aggregated signal object is passed to the capable-tier LLM to produce the narrative covering strong Topics, weak Topics, a revision nudge, and a study-consistency comment. Narrative may be cached with a short TTL at render time.

**NotificationDispatcher**
Interface: `dispatch(notification_type: NotificationType, recipient: User, payload: dict) → None`
Routes to three transports: FCM (Student push notifications), WhatsApp Business API (Teacher TeacherFlag nudges), and in-portal notification store (persistent, queryable). Each NotificationType carries toggle metadata — the dispatcher checks CenterAdmin-level toggles (DailyConcept, TeacherFlag resolved, StudyNote) and Student-level toggle (inactivity reminder) before sending. Transports are injected as dependencies for testability. WhatsApp routing only attempted if the CoachingCenter has WhatsApp enabled.

**ScheduledTestGatekeeper**
Pure logic layer enforcing: (1) no new attempt can be started after the availability window closes; (2) submission is rejected if the window has closed at submission time; (3) correct answers are withheld from the Student response payload until the window closes. Attempt count tracked and enforced (default 1, Teacher-configurable). Timer expiry triggers auto-submit via a client-initiated call — server validates window state at receipt. No I/O dependency — deeply unit-testable against a mocked clock and mocked attempt repository.

### Schema Decisions

- All roles identified by mobile number. No separate username field. fastapi-users handles mobile + password and mobile + OTP flows.
- Student record carries: Class (CBSE grade), enrolled Subjects, CoachingCenter reference.
- ProficiencyLevel stored as a table keyed by (student_id, topic_id), defaulting to Beginner, written on first TimedTest completion for that Topic.
- ExplanationSession stores only the outcome (understood | teacher_flagged) and pass count at outcome time — not the full conversation.
- TimedTest attempt stores: student_id, topic_id, chosen_difficulty, score_pct, question_count, timestamp. Only written if at least one question was answered.
- ScheduledTest stores `question_type` field (currently always "mcq") to support future short-answer extension without schema migration.
- StudyNote metadata (uploader, assignment scope, optional topic/chapter tag, GCS object path) stored in Postgres. Binary stored in GCS (max 20 MB).
- TeacherFlag stores: student_id, topic_id, teacher_id, raised_at, resolved_at (nullable), resolution_note (nullable), is_resolved (boolean).
- DailyConcept stores: teacher_id, posted_date, list of topic_ids (up to 5). Unique constraint on (teacher_assignment_id, posted_date).
- NCERTCorpus chunks stored in pgvector with metadata: chunk_id, chunk_type, class_level, subject, chapter, section_id, heading, page_number, subject_id (FK → subjects.id), chapter_id (FK → chapters.id). HNSW index. Estimated 10,000–30,000 vectors. `subject_id` and `chapter_id` are the integer FK columns used by RAGService for filtering; the text `subject` and `chapter` columns are retained for display metadata in RetrievedPassage. A bm25s keyword index is built from the same chunks at ingestion time and serialized to disk for RAGService to load at startup.

### API Contracts (key endpoints)

- `POST /sessions/explanation` — initiates ExplanationSession, returns session_id and first Pass type.
- `POST /sessions/explanation/{session_id}/message` — sends student utterance; returns SSE stream of AI response and updated pass state.
- `POST /sessions/explanation/{session_id}/advance-pass` — advances to the next Pass; on exhaustion of Pass3, raises TeacherFlag and dispatches notifications before emitting the terminal done event.
- `POST /sessions/explanation/{session_id}/close` — records outcome (understood | teacher_flagged); does not trigger flag creation.
- `POST /tests/timed/start` — samples questions via QuestionBankSampler, returns question list; no server state until submit.
- `POST /tests/timed/submit` — validates at-least-one-answer rule; writes attempt; triggers ProficiencyEngine recalculation.
- `POST /tests/scheduled/{test_id}/start` — checked by ScheduledTestGatekeeper; returns question list.
- `POST /tests/scheduled/{test_id}/submit` — checked by ScheduledTestGatekeeper for window validity; writes attempt.
- `GET /performance/report/{student_id}` — returns PerformanceReport with AI narrative and Class Tests section.
- `POST /teacher/daily-concept` — posts DailyConcepts (idempotent per day per teacher_assignment_id).
- `POST /teacher/study-notes` — multipart upload; stores to GCS; triggers NotificationDispatcher.
- `GET /teacher/flags` — returns TeacherFlags scoped to caller's TeacherAssignment.
- `PATCH /teacher/flags/{flag_id}/resolve` — marks TeacherFlag resolved with optional note.

### Architectural Decisions

- **ADR 0001** — All AI responses grounded via RAG over NCERTCorpus in pgvector. System prompt enforces NCERT-only scope. No moderation middleware in v1 — slot reserved for future insertion.
- **ADR 0002** — Student app in React Native; TeacherPortal in React+Vite SPA; shared FastAPI backend.
- **ADR 0003** — In-portal notification is the primary, permanent TeacherFlag channel. WhatsApp nudge is secondary and toggled per CoachingCenter.
- **ADR 0004** — QuestionBank pre-generated offline by standalone CLI. Not generated at runtime. Sampled at test-start.
- **ADR 0005** — LiteLLM library (not proxy) for all LLM calls. Direct provider calls. Capable-tier model for ExplanationSession and PerformanceNarrativeGenerator; cheaper-tier for RevisionSession.
- **ADR 0006** — pgvector inside the same Postgres instance. HNSW index. Estimated vector count within single-instance limits at launch scale.
- **ADR 0007** — FastAPI + SQLAlchemy, async. fastapi-users for auth. SSE for streaming ExplanationSession responses.
- **ADR 0008** — MiniTest defaults to QuestionBank. Abstracted behind a configurable interface for future LLM swap.
- **ADR 0009** — Single e2-small VM on GCP Mumbai for DPDP data residency. FastAPI in Docker. Postgres native on VM. Daily pg_dump to GCS. Embedding and QuestionBank generation run as offline jobs on separate infrastructure.
- **ADR 0010** — React+Vite SPA built to static files, served by Nginx on the same VM as the FastAPI backend.
- **ADR 0011** — bm25s (Python library) used as the BM25 backend for keyword retrieval. Postgres FTS (tsvector) rejected due to non-standard scoring; Tantivy rejected due to Rust build dependency and lightly-maintained Python bindings.
- **ADR 0012** — Reranker (bge-reranker-base) runs as plain PyTorch on CPU at v1 launch. ONNX INT8 quantization and T4 GPU are documented upgrade paths triggered by profiling data.

---

## Testing Decisions

A good test verifies external, observable behavior — what the module returns or writes — not how it achieves it. Tests should not assert which internal methods were called or depend on implementation structure that is likely to change.

**Unit tests (no I/O)**

- **ProficiencyEngine**: Table-driven tests covering all 6 transition cells and both configurable threshold boundaries. Thresholds injected as parameters — no hardcoded constants in tests.
- **ScheduledTestGatekeeper**: Clock-mocked tests for window-open, window-closed, and at-boundary submission; attempt-count enforcement at 1 and n; answer-reveal suppression before and after window close.
- **PerformanceNarrativeGenerator signal aggregation**: Assert correct aggregation of TimedTest scores, pass counts, flag counts, and activity frequency from fixture data — without invoking any LLM.
- **ExplanationSessionOrchestrator state machine**: Unit tests for each Pass transition trigger, TeacherFlag trigger on Pass3 exhaustion, and premature close at any Pass.
- **NotificationDispatcher routing**: Mocked FCM, WhatsApp, and in-portal transports; assert correct transport invocation per NotificationType; assert toggle suppression for each type.

**Integration tests (with database)**

- **RAGService**: Seed fixture vectors into a pgvector test instance and a fixture bm25s index; assert top-k recall, subject_id filter correctness, chapter_id filter correctness (enabled vs disabled via filter_by_chapter), and RRF output cardinality.
- **QuestionBankSampler**: Fixture QuestionBank rows; assert sampling returns correct count, correct ProficiencyLevel, correct Topic; assert behavior when bank has fewer questions than requested count.
- **TimedTest submission pipeline**: End-to-end from submit through ProficiencyEngine recalculation to ProficiencyLevel row update.
- **ScheduledTest submission pipeline**: End-to-end through ScheduledTestGatekeeper to attempt record; assert window-closed rejection path writes no record.
- **TeacherFlag creation**: Assert in-portal notification record created; assert NotificationDispatcher called with correct payload; assert WhatsApp call suppressed when center toggle is off.

**End-to-end / contract tests**

- **SSE streaming**: Assert ExplanationSessionOrchestrator emits correctly formatted SSE events and that Pass state is reflected in event metadata.
- **StudyNote upload**: Multipart POST to GCS stub; assert metadata written to Postgres; assert push notification dispatched when CenterAdmin toggle is on.
- **PerformanceReport**: Assert correct section separation (AI learning vs. Class Tests); assert Class Tests section contains no AI narrative field.

---

## Out of Scope

- **Moderation middleware**: No content moderation layer in v1. Architecture slot reserved for future insertion.
- **LLM-generated MiniTest questions**: Questions come from QuestionBank in v1. The abstraction exists; the LLM source is not activated.
- **Short-answer questions in ScheduledTest**: `question_type` field is stored for future use. Only MCQ supported in v1.
- **Multiple CoachingCenters per Student**: A Student belongs to one CoachingCenter in v1.
- **Student self-registration**: Students are enrolled by CenterAdmin only. No self-signup flow.
- **Admin UI for NCERTCorpus ingestion**: Populated by a standalone CLI script pre-launch. No portal UI for corpus management in v1.
- **Languages other than English**: English-only in v1.
- **Offline mode for Student app**: Connectivity required. No offline content cache or offline test mode.
- **Classes below 8 or above 10**: Curriculum scope is CBSE Classes 8–10 only.
- **Parent role**: No parent-facing interface or notifications in v1.
- **Gradebook or cumulative GPA**: PerformanceReport provides narrative and TimedTest history only. No cumulative grading or class ranking.
- **In-app payments or subscription management**: Billing managed outside the platform in v1.
- **Teacher-to-Student direct messaging**: Communication mediated through TeacherFlags, DailyConcepts, and StudyNotes only.

---

## Further Notes

**Data residency**: The GCP Mumbai deployment is chosen explicitly to satisfy DPDP (Digital Personal Data Protection Act, India) data residency requirements. Any future multi-region expansion must re-evaluate this constraint before routing student data outside India.

**ProficiencyLevel and ScheduledTest independence**: ScheduledTest scores deliberately do not affect ProficiencyLevel. ProficiencyLevel is driven exclusively by TimedTests (student-initiated self-assessments). ScheduledTests are Teacher-owned assessments; their scores appear in the PerformanceReport "Class Tests" section as raw scores only. Conflating Teacher-graded and self-directed metrics would muddy both signals.

**WhatsApp as a secondary channel**: The WhatsApp nudge for TeacherFlags is a convenience channel, not a system-of-record. The in-portal notification is the authoritative, permanent record. WhatsApp is toggled per CoachingCenter to accommodate centers where Teachers are reliably in the portal versus those where a mobile nudge improves response time.

**Tiered LLM cost management**: The cheaper-tier model assigned to RevisionSession reflects that a RevisionSession is a single FirstPrinciples pass with no escalation — a lower-complexity generation task. The capable-tier model is reserved for ExplanationSession (multi-pass, nuanced pedagogical interaction) and PerformanceNarrativeGenerator (multi-signal narrative synthesis). This tiering should be revisited as usage data accumulates at scale.

**QuestionBank quality is a launch prerequisite**: All TimedTests, MiniTests, and ScheduledTest question pools depend on a pre-populated QuestionBank. The offline generation CLI and its review process must complete before any Student-facing test functionality is available. Topic coverage should be tracked as a launch readiness metric — a TimedTest for an uncovered Topic will fail at sampling time.

**Session outcome as the atomic unit of learning data**: Not persisting mid-session ExplanationSession state (only the outcome) keeps the data model simple at the cost of conversation replay. If Teacher review of specific conversations becomes a requirement, a conversation log table can be added without breaking the existing outcome-based reporting structure.

**NCERTCorpus as the trust boundary**: The quality of NCERTCorpus ingestion — completeness of chapter coverage, chunking strategy, embedding model choice — directly determines the quality of every AI interaction on the platform. Corpus ingestion should be treated as a first-class engineering task, not a pre-launch afterthought.
