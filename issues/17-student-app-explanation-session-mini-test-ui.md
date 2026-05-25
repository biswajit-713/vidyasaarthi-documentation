## Student app — ExplanationSession + MiniTest UI

## What to build

Implement the ExplanationSession and MiniTest screens in the React Native app.

The ExplanationSession screen is an SSE-driven chat interface. The Student sees the AI response stream in real time. A Pass indicator shows the current Pass (FirstPrinciples, Elaboration, Socratic). Two action buttons allow the Student to declare "I understand" or "I don't understand". On exhausting all Passes, the app shows the TeacherFlag message transparently.

On declaring "I understand", the app offers the option to start a MiniTest. The MiniTest screen shows a list of questions (ungraded, untimed). Each question has a "Explain this" action that opens an SSE-streamed explanation inline.

## Acceptance criteria

- [ ] ExplanationSession screen opens from a Topic detail and streams AI responses via SSE in real time
- [ ] Pass indicator is visible and updates as the session advances
- [ ] "I understand" and "I don't understand" buttons are always visible during an active session
- [ ] On TeacherFlag outcome, the Student sees the transparent message and the session screen closes
- [ ] On understanding outcome, the Student is offered a "Take MiniTest" option
- [ ] MiniTest screen shows questions without a timer or score
- [ ] Each MiniTest question has an "Explain this" action that streams an inline SSE explanation
- [ ] Closing the app mid-session and returning starts a fresh session (no resume state)

## Blocked by

- #16 Student app scaffold + auth + curriculum navigation
- #7 ExplanationSession backend
- #9 MiniTest backend
