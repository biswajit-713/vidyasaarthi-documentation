## MiniTest backend

## What to build

Implement the MiniTest — an ungraded, untimed post-ExplanationSession self-check. After a Student declares understanding and closes an ExplanationSession, they are offered a MiniTest on that Topic.

Questions are drawn from the QuestionBank via QuestionBankSampler at the Student's current ProficiencyLevel for the Topic. No score is recorded — the MiniTest is purely for the Student's own self-check.

The Student can ask the AI to explain any individual question further. Each such explanation is a single SSE call grounded in NCERTCorpus via RAGService — not a new ExplanationSession.

## Acceptance criteria

- [ ] MiniTest is only available after a closed ExplanationSession with outcome `understood`
- [ ] Questions are sampled via QuestionBankSampler at the Student's current ProficiencyLevel for the Topic
- [ ] MiniTest has no timer, no score, and no database record written on completion
- [ ] `POST /minitests/{topic_id}/explain-question` accepts a question_id and streams an AI explanation via SSE, grounded in NCERTCorpus
- [ ] Per-question explanation does not start a new ExplanationSession
- [ ] Unit tests: verify sampler is called with correct topic_id and proficiency_level

## Blocked by

- #8 ExplanationSession backend
- #7 QuestionBank generation CLI + QuestionBankSampler
- #32 RAGService hybrid retrieval pipeline
- #29 LLM token usage logging
- #30 Student activity event log
