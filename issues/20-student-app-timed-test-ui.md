## Student app — TimedTest UI

## What to build

Implement the TimedTest screen in the React Native app.

Before starting, the Student sees their current ProficiencyLevel for the Topic pre-selected as difficulty; they can override it. On start, questions are fetched and the countdown timer begins. The Student can freely navigate between questions and change answers at any time within the timer window. Answers are held entirely client-side until submission. The Student submits explicitly or the timer triggers auto-submit. If the network is unavailable at submission time, the attempt is discarded with a clear message.

## Acceptance criteria

- [ ] Pre-start screen shows current ProficiencyLevel as default difficulty with an override option
- [ ] Timer is visible and counting down throughout the test
- [ ] Student can navigate freely between questions and change any answer before submission
- [ ] Answers are not sent to the server until explicit submit or timer expiry
- [ ] Timer expiry triggers automatic submission
- [ ] Network failure at submission shows a clear discard message; no partial attempt is recorded
- [ ] Post-submit screen shows score and updated ProficiencyLevel

## Blocked by

- #18 Student app scaffold + auth + curriculum navigation
- #11 ProficiencyEngine + TimedTest backend
