## QuestionBank generation CLI + QuestionBankSampler

## What to build

A standalone CLI script that generates MCQ questions for every Topic + ProficiencyLevel combination (Beginner, Intermediate, Expert) using an LLM grounded in NCERTCorpus. Questions are stored in the QuestionBank table. This is an offline pre-launch job — not run at request time.

Alongside the script, implement `QuestionBankSampler` as a deep module. The question source is abstracted behind a configurable interface so a future LLM-backed generator can replace the QuestionBank without changing callers.

`sample(topic_id, proficiency_level, count)` queries the QuestionBank and returns `count` random questions at the given level.

## Acceptance criteria

- [ ] CLI script generates MCQ questions per Topic + ProficiencyLevel and stores them in the QuestionBank table
- [ ] Each question record stores: topic_id, proficiency_level, question text, answer options, correct answer index
- [ ] `QuestionBankSampler.sample()` returns the requested count of questions for the given Topic and ProficiencyLevel
- [ ] Sampler handles the case where the bank has fewer questions than the requested count (returns all available)
- [ ] Question source is abstracted behind a configurable interface (QuestionBank is the default; interface allows LLM substitution)
- [ ] Unit tests: fixture rows in QuestionBank; assert correct sampling, correct level filtering, under-count edge case

## Blocked by

- #5 NCERTCorpus ingestion CLI + RAGService
- #27 LLM token usage logging
