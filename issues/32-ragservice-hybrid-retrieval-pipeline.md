## RAGService — hybrid retrieval pipeline

## What to build

Implement `RAGService` as a deep module with a single retrieval interface used by ExplanationSession, RevisionSession, and the QuestionBank generation CLI.

`retrieve(query, class_level, subject, top_k=5)` executes a 4-stage hybrid pipeline and returns the top-k NCERT passages most relevant to the query.

### Pipeline

| Stage | Method | Input → Output |
|---|---|---|
| 1a | BM25 keyword search | query → top-50 matches from bm25s index |
| 1b | Semantic search | query embedding (bge-large-en-v1.5) → top-50 ANN matches from pgvector filtered by `class_level` and `subject` |
| 2 | RRF merge | two lists of 50 → top-20 merged candidates |
| 3 | Cross-encoder reranking | bge-reranker-base (plain PyTorch) scores top-20 → top-k passages |
| 4 | Return | top-k passages with metadata to caller |

Stage cardinalities are configurable constants: `BM25_TOP_N=50`, `SEMANTIC_TOP_N=50`, `RRF_TOP_N=20`.

### Model loading

Both `bge-large-en-v1.5` (query embedding) and `bge-reranker-base` (reranking) are loaded once at FastAPI startup. The bm25s index is also loaded from disk at startup. None of these are reloaded per request.

### Connection pool

RAGService uses the application's existing SQLAlchemy connection pool for all pgvector queries. No new database connection is opened per retrieval call.

## Acceptance criteria

- [ ] `RAGService.retrieve(query, class_level, subject, top_k)` returns top-k passages filtered by `class_level` and `subject`
- [ ] Stage 1a: BM25 search returns top-50 candidates from the bm25s index loaded at startup
- [ ] Stage 1b: semantic search embeds the query with `bge-large-en-v1.5` and returns top-50 ANN matches from pgvector filtered by `class_level` and `subject`
- [ ] Stage 2: RRF merges both candidate lists and outputs top-20
- [ ] Stage 3: `bge-reranker-base` (plain PyTorch) scores the top-20 candidates and returns top-k
- [ ] `bge-large-en-v1.5`, `bge-reranker-base`, and the bm25s index are loaded once at FastAPI startup; not reloaded per request
- [ ] RAGService uses the application's existing SQLAlchemy connection pool — no new connection per retrieval call
- [ ] `BM25_TOP_N`, `SEMANTIC_TOP_N`, and `RRF_TOP_N` are configurable constants
- [ ] Integration tests: fixture vectors seeded into pgvector test instance and bm25s index; assert top-k recall, metadata filter correctness, and RRF output cardinality

## Blocked by

- #6 NCERTCorpus ingestion CLI
