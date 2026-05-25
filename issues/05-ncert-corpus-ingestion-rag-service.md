## NCERTCorpus ingestion CLI + RAGService

## What to build

A standalone CLI script that ingests NCERT PDF textbooks for Classes 8–10, chunks the text, generates embeddings, and stores vectors in pgvector with an HNSW index. This is a pre-launch offline job run by the engineering team — no admin UI.

Alongside the ingestion script, implement `RAGService` as a deep module with a single retrieval interface. This module is used by ExplanationSession and RevisionSession to ground every AI response in NCERT content.

`retrieve(query, class_level, subject, top_k)` performs a semantic nearest-neighbour search filtered by `class_level` and `subject` metadata, returning the top-k NCERT passages. No LLM dependency — retrieval is purely pgvector.

## Acceptance criteria

- [ ] CLI script accepts a directory of NCERT PDFs, chunks them, generates embeddings, and upserts vectors into pgvector
- [ ] Each vector is stored with metadata: class_level, subject, chapter, topic, source_page
- [ ] HNSW index is created on the vector column
- [ ] `RAGService.retrieve()` returns top-k passages filtered by class_level and subject
- [ ] Integration tests: fixture vectors seeded into pgvector test instance; assert top-k recall and metadata filter correctness
- [ ] Running the CLI script twice is idempotent (no duplicate vectors)

## Blocked by

- #1a Local dev environment
