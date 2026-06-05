# bm25s is used as the BM25 backend for keyword retrieval

The hybrid retrieval pipeline needs a BM25 index over NCERTCorpus passages (10k–30k entries) to complement pgvector semantic search. We chose `bm25s` (in-process Python library, serialized index on disk) over two alternatives:

- **Postgres full-text search (tsvector / ts_rank_cd)**: Zero new dependencies, but uses a cover-density scoring formula rather than true BM25. Term-frequency saturation and document-length normalisation are absent, which meaningfully degrades exact-keyword ranking for short student queries against variable-length NCERT passages.
- **Tantivy (`tantivy-py`)**: True BM25 and very fast (Rust internals), but requires the Rust toolchain at Docker build time, has lightly-maintained Python bindings (last major release 2023), and requires duplicating passage metadata into the Tantivy index or issuing a separate Postgres query for metadata filtering — disproportionate complexity for this corpus size.

`bm25s` gives true BM25 scoring with tunable `k1`/`b`, no new runtime service, a serialized index that loads at FastAPI startup, and RAM overhead well within the e2-small budget for this corpus size.
