## RAGService retrieval result caching

## What to build

Cache `RAGService.retrieve()` results in-process for a short TTL. The same passages are retrieved for every student querying the same Topic — the BM25 search, pgvector ANN search, RRF merge, and cross-encoder reranking do not need to run repeatedly for identical inputs.

Cache key: `(query, class_level, subject)`. Default TTL: 5 minutes.

## Acceptance criteria

- [ ] `RAGService.retrieve()` caches results in-process with a configurable TTL (default: 5 minutes)
- [ ] Cache key is `(query, class_level, subject)`
- [ ] Cache hit and miss events are logged

## Blocked by

- #32 RAGService hybrid retrieval pipeline
