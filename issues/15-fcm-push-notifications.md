## FCM push notifications — all four types

## What to build

Integrate Firebase Cloud Messaging (FCM) into the NotificationDispatcher and wire up all four notification types for the Student app.

The four types and their toggle owners:
1. **DailyConcept posted** — CenterAdmin toggle
2. **TeacherFlag resolved** — CenterAdmin toggle
3. **New StudyNote shared** — CenterAdmin toggle
4. **Inactivity reminder** (Student inactive for N days) — Student toggle

The Student app must register an FCM device token on login and send it to the backend. The NotificationDispatcher uses this token to target push notifications.

In dev, the FCM transport is stubbed; production uses real FCM credentials.

A Student settings endpoint allows toggling the inactivity reminder preference. The inactivity reminder requires a background job that identifies inactive Students and dispatches reminders.

## Acceptance criteria

- [ ] Student app registers FCM device token with the backend on login; token is stored per Student
- [ ] `PATCH /student/settings/notifications` allows the Student to toggle the inactivity reminder on or off
- [ ] All four notification types are dispatched via the NotificationDispatcher FCM transport
- [ ] CenterAdmin toggles suppress FCM dispatch for types 1–3 when off
- [ ] Student toggle suppresses FCM dispatch for type 4 when off
- [ ] Background job identifies Students inactive for N days and dispatches inactivity reminder (N is configurable)
- [ ] FCM transport is injected as a dependency; unit tests assert dispatch calls with mocked FCM client
- [ ] FCM credentials are environment-variable-configured; dev environment uses the stub transport

## Blocked by

- #8 TeacherFlag + NotificationDispatcher
