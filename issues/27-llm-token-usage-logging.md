## LLM token usage logging

## What to build

Implement `LLMUsageLogger` — a thin wrapper around LiteLLM calls that captures token counts and estimated cost from every LLM response and writes a row to the `llm_usage_log` table. This is the foundation for unit-economics tracking as usage scales.

`llm_usage_log` table columns:
- `id`, `created_at`
- `source` — enum: `explanation_session` | `revision_session` | `mini_test_explanation` | `performance_narrative` | `question_bank_generation`
- `student_id` — nullable; null for offline CLI jobs (QuestionBank generation), non-null for all student-facing calls
- `topic_id` — nullable
- `model_tier` — enum: `capable` | `fast`
- `model_id` — the actual provider model string (e.g. `claude-3-5-sonnet-20241022`); records the exact model even if the tier mapping changes
- `prompt_tokens`, `completion_tokens`, `total_tokens`
- `estimated_cost_usd` — computed at write time from a configurable pricing table (model_id → input $/1k tokens, output $/1k tokens); the pricing table lives in app config, not hardcoded

For streaming SSE calls, LiteLLM's `stream_options={"include_usage": True}` surfaces token counts in the final chunk. `LLMUsageLogger` captures this from the stream tail after the last chunk is sent to the client, so the write does not add latency to the student-facing response.

`LLMUsageLogger` is injected as a dependency into `ExplanationSessionOrchestrator`, `RevisionSession`, the MiniTest per-question explanation handler, `PerformanceNarrativeGenerator`, and the QuestionBank generation CLI.

Two PlatformAdmin-only read endpoints are added:
- `GET /admin/llm-usage` — paginated rows; filterable by `start_date`, `end_date`, `student_id`, `source`, `model_tier`
- `GET /admin/llm-usage/summary` — per-day, per-source aggregates: `total_prompt_tokens`, `total_completion_tokens`, `estimated_cost_usd`

No UI in v1. Both endpoints are intended for direct API access or export.

## Acceptance criteria

- [ ] `llm_usage_log` table exists with all specified columns; `source` and `model_tier` are Postgres enum types
- [ ] A row is written for every LiteLLM call in: `ExplanationSessionOrchestrator` (all three Passes), `RevisionSession`, MiniTest per-question explanation, `PerformanceNarrativeGenerator`, QuestionBank generation CLI
- [ ] Streaming calls use `stream_options={"include_usage": True}`; the final chunk's usage fields are captured and logged after the stream closes
- [ ] `estimated_cost_usd` is computed from a config-file pricing table keyed on `model_id`; changing pricing requires only a config update, not a code change
- [ ] `student_id` is null for QuestionBank generation CLI; non-null for all student-triggered calls
- [ ] `GET /admin/llm-usage` requires PlatformAdmin role; returns paginated rows with filter params `start_date`, `end_date`, `student_id`, `source`
- [ ] `GET /admin/llm-usage/summary` returns per-day, per-source rows with aggregated token counts and cost; accessible to PlatformAdmin only
- [ ] `LLMUsageLogger` is injected as a dependency; unit tests assert log writes using a mock logger — no real LLM calls in tests
- [ ] A failed log write (e.g. DB unavailable) is caught, logged to stderr, and does not raise an exception that interrupts the session or SSE stream

## Blocked by

- #1a Local dev environment
