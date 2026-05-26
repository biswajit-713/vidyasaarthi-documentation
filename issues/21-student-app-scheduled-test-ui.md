## Student app — ScheduledTest UI

## What to build

Implement the ScheduledTest screens in the React Native app.

A Student sees their assigned ScheduledTests with availability window, per-attempt duration, and remaining attempts. Within the window, they can start an attempt. The test behaves like TimedTest (countdown timer, free navigation, client-side answers) but with the additional constraint that the server enforces the availability window. Auto-submit on timer expiry. Network failure at submission discards the attempt. After submission, the Student sees their score but not the correct answers — those appear only after the availability window closes.

## Acceptance criteria

- [ ] ScheduledTest list shows availability window, duration, and remaining attempts for each test
- [ ] Tests with closed windows are shown as unavailable; start is disabled
- [ ] Timer is visible and counting down throughout the attempt
- [ ] Auto-submit fires on timer expiry
- [ ] Network failure at submission shows a clear discard message
- [ ] Post-submit screen shows score only; correct answers are not displayed
- [ ] After the availability window closes, revisiting the result shows correct answers and per-question feedback
- [ ] Attempt count remaining is reflected in the UI; start is disabled when limit is reached

## Blocked by

- #18 Student app scaffold + auth + curriculum navigation
- #14 ScheduledTestGatekeeper
