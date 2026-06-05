## Anthropic prompt caching for ExplanationSession

## What to build

Enable Anthropic prompt caching for the NCERT context prefix in ExplanationSession LLM calls. The passages retrieved by RAGService for a given Topic are identical across all students. Caching the key-value attention states of this prefix means only the first call for a Topic within the cache TTL window pays full input token cost; subsequent calls pay ~10% for the cached portion.

This is a cost and latency optimisation — response quality is unaffected. Each student still receives a freshly generated, personalised response.

## Acceptance criteria

- [ ] ExplanationSession LLM calls mark the NCERT context prefix with the Anthropic prompt caching header
- [ ] Cache hit rate (cached input tokens vs. total input tokens) is logged per session via the existing LLM token usage logging (issue #29)

## Blocked by

- #8 ExplanationSession backend
- #29 LLM token usage logging
