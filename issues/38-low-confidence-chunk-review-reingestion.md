## Low-confidence chunk review and re-ingestion

## What to build

A companion ingestion command that takes a human-reviewed version of the skipped-chunks report (produced by the main ingestion CLI, issue #6) and ingests the reviewed chunks into pgvector and bm25s.

The engineering team reviews the skipped-chunks JSONL, corrects `chunk_type` and `content` as needed, then runs this command to add the reviewed chunks to the existing indexes.

## Acceptance criteria

- [ ] CLI command accepts `--reviewed-chunks` (JSONL file in the same schema as the skipped-chunks report, with corrected `chunk_type` and `content`) and `--bm25s-index-path`
- [ ] Reviewed chunks are embedded with `bge-large-en-v1.5` and upserted into pgvector
- [ ] bm25s index is rebuilt to include the reviewed chunks alongside all previously indexed chunks
- [ ] Running the command twice is idempotent: vectors are upserted by `chunk_id`

## Blocked by

- #6 NCERTCorpus ingestion CLI
