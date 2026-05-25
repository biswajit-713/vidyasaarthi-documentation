## CoachingCenter, Enrollment & TeacherAssignment

## What to build

Implement the organizational structure of the platform. PlatformAdmin creates CoachingCenters. CenterAdmin enrolls Students into specific Subjects at their CoachingCenter. CenterAdmin creates TeacherAssignments (Teacher → Subject + Class at a CoachingCenter).

Also includes CoachingCenter-level configuration toggles:
- WhatsApp notifications on/off
- Push notification types on/off (DailyConcept posted, TeacherFlag resolved, StudyNote shared)
- TimedTest configuration (question count, duration)

## Acceptance criteria

- [ ] PlatformAdmin can create a CoachingCenter
- [ ] CenterAdmin can enroll a Student into one or more Subjects at their CoachingCenter
- [ ] CenterAdmin can create a TeacherAssignment mapping a Teacher to a Subject + Class
- [ ] A Student's enrolled Subjects are retrievable from their profile
- [ ] TeacherAssignment determines which TeacherFlags, DailyConcepts, and Students are visible to a Teacher
- [ ] CenterAdmin can set and update WhatsApp notification toggle per CoachingCenter
- [ ] CenterAdmin can set and update push notification type toggles per CoachingCenter
- [ ] CenterAdmin can set TimedTest question count and duration per CoachingCenter
- [ ] CenterAdmin actions are scoped to their own CoachingCenter; cross-center access is rejected

## Blocked by

- #2 Authentication & identity
- #3 Curriculum structure
