## Student app — PerformanceReport + StudyNote UI

## What to build

Implement the PerformanceReport and StudyNote screens, plus the notification settings toggle.

**PerformanceReport**: Two sections. AI learning section shows last 5 TimedTest results across Topics with a Topic drill-down (up to 10 results per Topic) and the AI-generated narrative. Class Tests section shows ScheduledTest results as raw scores only with no narrative.

**StudyNote**: A list of StudyNotes shared with the Student. Tapping a note downloads or opens the PDF. The download uses a signed URL from the backend.

**Settings**: An inactivity reminder notification toggle.

## Acceptance criteria

- [ ] PerformanceReport screen has two clearly separated sections: AI learning and Class Tests
- [ ] AI learning section shows last 5 TimedTest results per Topic; tapping a Topic shows drill-down of up to 10 results
- [ ] AI narrative is displayed within the AI learning section
- [ ] Class Tests section shows ScheduledTest scores as raw numbers with no AI commentary
- [ ] StudyNote list shows all notes shared with the Student
- [ ] Tapping a StudyNote initiates a PDF download via signed URL
- [ ] Notification settings screen includes an inactivity reminder toggle that persists to the backend
- [ ] Empty states are handled for both PerformanceReport sections and the StudyNote list

## Blocked by

- #18 Student app scaffold + auth + curriculum navigation
- #16 PerformanceReport backend
- #15 StudyNote backend
- #17 FCM push notifications
