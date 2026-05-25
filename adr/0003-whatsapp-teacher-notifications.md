# TeacherFlag notifications use WhatsApp, not SMS

When a TeacherFlag is raised, the Teacher receives an in-portal notification (primary record) and a WhatsApp message (immediate nudge). We chose WhatsApp over SMS because WhatsApp has significantly higher open rates and engagement in India, and the target Teacher population is already on WhatsApp. WhatsApp notification can be disabled per-center or per-teacher via a platform setting — useful for centers that prefer to manage communication their own way. The integration requires the WhatsApp Business API.

## Considered Options

- **In-portal only**: No out-of-band notification. Teacher sees flags only when they log in — too passive for time-sensitive student support.
- **SMS**: Universal but lower engagement than WhatsApp in the Indian context.
- **WhatsApp + in-portal** ✅: High engagement, disableable, fits the Teacher's existing communication habits.
