# TimedTest questions are drawn from a pre-generated bank, not generated at runtime

Questions for each Topic + difficulty level combination are generated in bulk upfront and stored in a question bank. At test-start, the required number of questions is sampled from the bank for that Topic and difficulty. We chose this over on-demand generation because runtime latency matters — a student waiting for questions to generate before a timed test is a poor experience. Repeat exposure is acceptable at early scale given the small concurrent student population per Topic. The intent is to migrate to a hybrid model (bank + periodic background refresh) when scale demands it.

## Considered Options

- **Fresh generation at runtime**: Unique every time, but adds latency and LLM cost at test-start.
- **Pre-generated bank** ✅: Fast at runtime, cost incurred offline. Acceptable repeat risk at early scale.
- **Hybrid (bank + refresh)**: Target state at scale — not the starting point.
