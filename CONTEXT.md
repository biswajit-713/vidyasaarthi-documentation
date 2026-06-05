# Vidyasaarthi

An AI-powered learning platform for CBSE students in Classes 8–10, distributed through coaching centers. The AI tutors students on NCERT content, assesses their understanding, and reports progress to teachers.

## Platform constraints

**Language**: English only. All AI-generated content — explanations, questions, narratives — must use plain, accessible English: short sentences, minimal jargon, Indian-context examples (cricket, rupees, everyday objects). No regional language support in scope.

**Content safety**: All AI interactions are constrained to academic content via a system prompt. The LLM provider's built-in safety filters are the primary guardrail. A dedicated moderation layer (input/output classifier) is not in scope for v1 but is designed to slot in as FastAPI middleware later if real-world usage reveals gaps.

**Push notifications**: The Student app (React Native) uses FCM for four notification types: (1) DailyConcept posted — toggled by CenterAdmin; (2) TeacherFlag resolved — toggled by CenterAdmin; (3) new StudyNote shared — toggled by CenterAdmin; (4) inactivity reminder (student inactive for N days) — toggled by the Student. Each notification type has an independent feature toggle.

## Language

### Content

**Class**:
The CBSE grade a student is enrolled in (8, 9, or 10). Derived from the Student record — never chosen at session time.
_Avoid_: Grade, standard, year

**Subject**:
A top-level curriculum area within a Class (e.g., Mathematics, Science, Social Science).
_Avoid_: Course, paper

**Chapter**:
A named unit within a Subject, corresponding directly to an NCERT textbook chapter.
_Avoid_: Unit, module, section

**Topic**:
The smallest addressable unit of content within a Chapter. The atom of all student interactions — explanation, testing, and performance tracking all operate at this level.
_Avoid_: Concept (reserved — see Daily Concept), subtopic, lesson

### Explanation

**ExplanationSession**:
The interaction that begins when a Student selects a Topic to understand. Proceeds through up to three Passes; ends when the Student declares understanding, opts into a MiniTest, or exhausts all Passes and triggers a TeacherFlag. Always starts from Pass 1 — mid-session state is never persisted or resumed. Only the outcome (understood vs. TeacherFlag) is stored.
_Avoid_: Tutoring session, doubt session, clarification

**Pass**:
A single attempt by the AI to explain a Topic within an ExplanationSession. There are exactly three: FirstPrinciples (Q&A-led), Elaboration (relatable examples), and Socratic. The Q&A interaction is free-form text — the Student types responses, the AI evaluates them and continues. The Student explicitly declares "I don't understand" to move to the next Pass. The Student explicitly declares "I understand" to end the session and optionally start a MiniTest.
_Avoid_: Attempt, round, iteration, level

**TimedTest**:
A timed MCQ assessment on a single Topic drawn from the QuestionBank. Question count and total duration are configured by the CenterAdmin. The Student sees their current ProficiencyLevel as the pre-selected difficulty at start and may override it. All answers are held client-side until submission — the student may revisit and change any answer freely within the timer window. Submitted in a single call on explicit submit or timer expiry. If the network is unavailable at submission time, the test is discarded and the student may take a fresh attempt. Only recorded if at least one question was answered.
_Avoid_: Quiz, assessment, exam, test

**ScheduledTest**:
A Teacher-authored test assigned to all Students in a TeacherAssignment (Subject + Class at a CoachingCenter). The Teacher sets a start and end date/time (availability window) and a per-attempt duration. Students see a countdown timer; the test auto-submits on expiry or is discarded on network failure (same rules as TimedTest). Submissions after the window closes are not accepted. The number of allowed attempts is configured by the Teacher at creation time, defaulting to 1. Questions are MCQ in v1; question type is stored as an attribute (`question_type`) so short-answer grading can be added later without a schema migration. The Teacher provides correct answers. No LLM interaction — scoring is automatic, explanation is handled by the Teacher in a subsequent class. Score does not affect ProficiencyLevel. Students see their score immediately after submission; correct answers and per-question feedback are revealed only after the availability window closes. The Teacher sees full results — submission status and per-student, per-question scores — from the first submission onward, throughout and after the window. Results are stored at the test's chosen scope (Topic, Chapter, or Subject) and visible to Students in a dedicated "Class Tests" section within the PerformanceReport.
_Avoid_: Class test, teacher test, assigned test, exam

**MiniTest**:
An ungraded, untimed set of questions offered to a Student after they declare understanding in an ExplanationSession. Not used for performance assessment — purely for the Student's own self-check. Questions are drawn from the QuestionBank by default; the source is configurable to allow fresh LLM generation as a future option. The Student can ask the AI to explain any question further.
_Avoid_: Quiz, check, formative test

**DailyConcept**:
A Teacher's selection of up to 5 Topics from that day's class, posted once per day. Students use these as a revision entry point within a 7-day rolling window — concepts older than 7 days are no longer shown. A DailyConcept is always a pointer to an existing Topic — the Teacher authors nothing new.
_Avoid_: Daily update, class summary, lesson post

**StudyNote**:
A PDF uploaded by a Teacher through the TeacherPortal and shared with either all Students in a TeacherAssignment or a named subset. Free-form — requires only a title; optionally tagged to a Topic or Chapter. Maximum file size 20MB; stored in GCS. Students can download the PDF from the app in v1; in-app rendering is a planned future extension. A push notification is sent to eligible Students when a new StudyNote is shared, toggled by CenterAdmin. The Teacher can delete a StudyNote after sharing — it is removed from the app but Students who already downloaded it retain their local copy.
_Avoid_: Notes, material, resource, handout

**RevisionSession**:
A single-pass, first-principles interaction triggered when a Student selects a DailyConcept. Uses Pass 1 only. No escalation, no TeacherFlag. If the Student still has doubts after revision, they open a separate ExplanationSession on that Topic.
_Avoid_: Revision mode, concept review, daily session

**PerformanceReport**:
A hybrid view of a Student's learning activity with two sections. (1) AI learning section: a metrics panel showing the last 5 TimedTest results across any Topics (drill-down per Topic shows up to 10 historical results), plus an AI-generated narrative informed by four signals — TimedTest scores per Topic, ExplanationSession pass counts, TeacherFlags raised, and activity frequency. The narrative identifies strong Topics, weak Topics, a revision nudge for recently poor-performing Topics, and a comment on study consistency. (2) Class Tests section: historical ScheduledTest results as raw scores only — no AI commentary. ScheduledTest performance is intentionally excluded from the AI narrative because Chapter and Subject-scoped tests cannot be attributed to specific Topics.
_Avoid_: Dashboard, report card, progress report, analytics

**TeacherFlag**:
A signal raised when a Student exhausts all three Passes without declaring understanding. The Student is shown a transparent message ("We've let your teacher know you need help with this topic") and the flag is visible in their profile. The Teacher receives an in-portal notification (permanent record) and a WhatsApp nudge. A Teacher can mark a flag as resolved with an optional note (e.g., "Explained in class"). WhatsApp delivery is toggled on/off by the CenterAdmin for the entire center.
_Avoid_: Escalation, alert, notification

**ProficiencyLevel**:
A label (Beginner, Intermediate, Expert) stored per Student per Topic. Defaults to Beginner until the first TimedTest on that Topic is completed. Reassessed after every TimedTest using a score-based rule (chosen difficulty + percentage score): Beginner ≥80% → Intermediate; Intermediate ≥80% → Expert; Expert ≥80% → Expert; Intermediate/Expert 40–79% → stays at chosen level; Expert <40% → Intermediate; Intermediate/Beginner <40% → Beginner. Thresholds are configurable by PlatformAdmin. Influences: (1) language register of Pass 1 in an ExplanationSession — passes are never skipped; (2) pre-selected difficulty when starting a TimedTest — Student can override; (3) tone and focus of the PerformanceReport narrative.
_Avoid_: Level, difficulty, skill level, rank

**QuestionBank**:
A pre-generated store of MCQ questions organised by Topic + ProficiencyLevel. Populated offline from the NCERTCorpus. Sampled at TimedTest-start. Refreshed periodically in the background once scale demands it.
_Avoid_: Question pool, test bank, question store

**NCERTCorpus**:
The ingested text of NCERT textbooks for Classes 8–10. The authoritative source that grounds all AI-generated explanations and test questions. Populated by a standalone CLI script run by the engineering team before launch — no admin UI for ingestion in v1. Script is designed to be wrappable in an upload UI in future.
_Avoid_: Knowledge base, content library, syllabus

### People

**Identity**:
All roles (Student, Teacher, CenterAdmin, PlatformAdmin) are identified by their mobile number. Authentication supports two methods: mobile number + password, or mobile number + OTP. No separate username — the mobile number is the username.
_Avoid_: Username, login ID, account ID

**Student**:
A learner enrolled in a Class at a CoachingCenter, with their own login. The Student record carries their Class, the specific Subjects they are enrolled in at that center, and their ProficiencyLevel per Topic.
_Avoid_: User, learner, child

**Enrollment**:
The CenterAdmin's act of registering a Student into specific Subjects at a CoachingCenter. Determines which DailyConcepts the Student sees, which TeacherAssignments can raise TeacherFlags for them, and which Subjects appear in their PerformanceReport.
_Avoid_: Registration, admission, subscription

**CenterAdmin**:
A role responsible for configuring a CoachingCenter on the platform: onboarding Teachers, enrolling Students, assigning Classes, and setting TimedTest configuration. Initially this role is performed by the PlatformAdmin; the intent is to delegate it to a staff member at each CoachingCenter over time.
_Avoid_: Admin, manager, coordinator

**PlatformAdmin**:
A Vidyasaarthi operator with super-admin access. Bootstraps new CoachingCenters and performs the CenterAdmin role until a dedicated CenterAdmin is in place.
_Avoid_: Super admin, system admin

**Teacher**:
A staff member at a CoachingCenter assigned to one or more Subject + Class combinations (e.g., Science for Class 9, Science for Class 10). Receives TeacherFlags only for Topics within their assigned Subject + Class. Posts DailyConcepts scoped to their assignment.
_Avoid_: Tutor, instructor, coach

**TeacherAssignment**:
The mapping of a Teacher to a specific Subject + Class at a CoachingCenter. Set by the CenterAdmin during onboarding. Determines TeacherFlag routing, DailyConcept visibility, and which Students appear in the Teacher's portal view.
_Avoid_: Role, allocation, subject ownership

**TeacherPortal**:
The web interface used by Teachers and CenterAdmins. For Teachers: shows all Students mapped to them via TeacherAssignment (not just those who raised TeacherFlags), with read-only TimedTest scores and TeacherFlag history per student; also the DailyConcept posting interface. For CenterAdmins: enrollment, TeacherAssignment management, and CoachingCenter configuration.
_Avoid_: Admin panel, dashboard, teacher app

**CoachingCenter**:
The partner institution through which Students and Teachers access the platform. Defines the organizational boundary — a Teacher belongs to one CoachingCenter, Students are enrolled through one.
_Avoid_: Institute, center, school
