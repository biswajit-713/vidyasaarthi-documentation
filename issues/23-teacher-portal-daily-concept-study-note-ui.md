## TeacherPortal — DailyConcept + StudyNote UI

## What to build

Implement the DailyConcept posting interface and StudyNote management in the TeacherPortal.

**DailyConcept**: A Topic picker scoped to the Teacher's TeacherAssignment. Teacher selects up to 5 Topics for today's class and posts them. The interface is idempotent — re-posting for the same day replaces the previous selection. Today's posted DailyConcepts are shown after posting.

**StudyNote**: An upload form accepting a PDF (max 20 MB) with a required title, an optional Topic or Chapter tag, and scope selection (all Students in TeacherAssignment or a named subset). A list of previously uploaded StudyNotes with a delete action.

## Acceptance criteria

- [ ] DailyConcept Topic picker is scoped to the Teacher's TeacherAssignment (correct Subject + Class)
- [ ] Maximum 5 Topics selectable; UI enforces this constraint
- [ ] Posting DailyConcepts for a day already posted replaces the previous selection
- [ ] Today's current DailyConcepts are displayed after posting
- [ ] StudyNote upload form accepts PDF only, enforces 20 MB limit with a client-side error
- [ ] Title is required; Topic and Chapter tag fields are optional
- [ ] Scope selector allows "all Students in TeacherAssignment" or selecting specific Students
- [ ] StudyNote list shows all uploaded notes with title, tag, date, and a delete button
- [ ] Delete action removes the note and it no longer appears in the Student app

## Blocked by

- #22 TeacherPortal scaffold + auth
- #11 DailyConcept + RevisionSession backend
- #13 StudyNote backend
