## TeacherPortal — scaffold + auth

## What to build

Scaffold the React+Vite Teacher/Admin web portal. Implement login and role-aware routing. The portal is a static SPA served by Nginx — no SSR.

Two role views:
- **Teacher**: DailyConcept posting, StudyNote upload, ScheduledTest authoring, TeacherFlag list, Student cohort monitoring
- **CenterAdmin**: Enrollment management, TeacherAssignment management, CoachingCenter configuration, plus all Teacher views

The scaffold establishes the navigation shell and authenticated routing. Individual feature screens are implemented in subsequent issues.

## Acceptance criteria

- [ ] Login screen supports mobile + password and mobile + OTP
- [ ] JWT stored in browser (httpOnly cookie or localStorage); attached to all API requests
- [ ] Logout clears credentials and redirects to login
- [ ] Teacher role sees Teacher navigation only; CenterAdmin role sees CenterAdmin navigation (superset)
- [ ] Navigation skeleton is in place for all portal sections (screens can be empty stubs at this stage)
- [ ] Vite build produces static files; Nginx config serves them correctly
- [ ] Portal URL and API base URL are environment-variable-configured; not hardcoded

## Blocked by

- #3 Authentication & identity
