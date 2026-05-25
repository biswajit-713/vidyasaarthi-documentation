## Student app — scaffold + auth + curriculum navigation

## What to build

Scaffold the React Native Student app. Implement login and the curriculum browsing navigation that all other Student screens slot into.

The app's navigation structure is:
- Unauthenticated: Login screen (mobile + password / OTP)
- Authenticated root: tab or stack navigator covering the main Student surfaces (curriculum, DailyConcepts, PerformanceReport, settings)
- Curriculum drill-down: Subjects → Chapters → Topics → Topic detail (entry point for ExplanationSession, TimedTest)

The app must handle JWT storage, token refresh, and logout.

## Acceptance criteria

- [ ] Login screen supports mobile + password and mobile + OTP flows
- [ ] JWT is stored securely and attached to all API requests
- [ ] Logout clears the JWT and returns to the login screen
- [ ] Student can browse their enrolled Subjects, drill into Chapters, and drill into Topics
- [ ] Navigation skeleton is in place for all other Student screens (screens can be empty stubs at this stage)
- [ ] App points to local backend URL via environment config; URL is not hardcoded

## Blocked by

- #2 Authentication & identity
- #3 Curriculum structure
