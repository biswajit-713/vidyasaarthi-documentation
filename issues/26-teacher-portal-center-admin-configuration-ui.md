## TeacherPortal — CenterAdmin configuration UI

## What to build

Implement the CenterAdmin-only configuration surfaces in the TeacherPortal. These screens are accessible only to users with the CenterAdmin or PlatformAdmin role.

**Enrollment management**: Add or remove Students from Subjects at the CoachingCenter.

**TeacherAssignment management**: Create or remove TeacherAssignments (Teacher → Subject + Class).

**CoachingCenter configuration**: TimedTest settings (question count, duration per test), push notification type toggles (DailyConcept posted, TeacherFlag resolved, StudyNote shared), WhatsApp notification toggle.

**PlatformAdmin only**: Create a new CoachingCenter.

## Acceptance criteria

- [ ] Enrollment screen lets CenterAdmin add a Student to one or more Subjects; enrolled Subjects shown per Student
- [ ] TeacherAssignment screen lets CenterAdmin assign a Teacher to a Subject + Class; existing assignments listed with a remove action
- [ ] Configuration screen shows TimedTest question count and duration as editable fields; changes persist
- [ ] Notification toggles (DailyConcept, TeacherFlag resolved, StudyNote) are shown as on/off toggles; state persists
- [ ] WhatsApp notification toggle is shown and persists
- [ ] All CenterAdmin screens are inaccessible to Teacher-role users (403 or hidden from navigation)
- [ ] PlatformAdmin sees an additional "Create CoachingCenter" form not visible to CenterAdmin

## Blocked by

- #22 TeacherPortal scaffold + auth
- #4 CoachingCenter, Enrollment & TeacherAssignment
