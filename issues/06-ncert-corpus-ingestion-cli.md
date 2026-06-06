## NCERTCorpus Ingestion CLI

## What to build

A standalone CLI script that ingests NCERT PDF textbooks for Classes 8–10 using structure-aware chunking, generates embeddings, and stores vectors in pgvector. It also builds a bm25s keyword index serialized to disk. Both indexes are consumed by RAGService at runtime.

A manifest file (JSON) maps each PDF to its `class_level`, `subject`, and `chapter`. The CLI reads the manifest to inject these fields into every chunk — no reliance on PDF metadata or filename conventions.

### Chunk types

Six chunk types are extracted using font-signature classification:

| Type | Description |
|---|---|
| `narrative_paragraph` | Regular flowing body text |
| `activity` | Starts with bold green header "Activity \<number\>:" |
| `knowledge_box` | Colored box with a known header (e.g. "Think like a scientist", "Our scientific heritage", "Be a scientist", "Ever heard of", "Snapshots", "Discover, design, and debate", "Keep the curiosity alive") |
| `table_segment` | Group header row within a table (spans full width) |
| `table_row` | Single data row; always belongs to a parent `table_segment`; formatted as "\<segment heading\>. Column1: Value1. Column2: Value2. ..." |
| `bullet_narrative` | Bullet list merged with its introducing paragraph |

Section headings and sub-section headings set context (`section_id`, `heading`) but are not chunks themselves.

### Chunk schema (JSONL output)

```json
{
  "chunk_id": "ch<chapter>_<sequence>",
  "chunk_type": "narrative_paragraph | activity | knowledge_box | table_segment | table_row | bullet_narrative",
  "heading": "...",
  "section_id": "3.4.1",
  "class_level": 9,
  "subject": "Science",
  "chapter": "Matter in Our Surroundings",
  "content": "...",
  "page_number": 42,
  "is_complete": true,
  "confidence": 0.95,
  "flags": []
}
```

### Classification rules

Use font signatures to classify text:
- Section headings (large bold ~17pt): set `section_id` and `heading` context; not a chunk
- Sub-section headings (bold ~13pt black, matches `\d+\.\d+\.\d+`): set context; not a chunk
- Activity headers (bold ~15pt green accent): start an `activity` chunk
- Bold green sub-headings (~13pt green, does not match numbered pattern): finalize current chunk; start new `narrative_paragraph`
- Known knowledge box headers (bold ~13pt black, matches known header list): start a `knowledge_box` chunk
- Body text (serif ~12pt): append to current open chunk
- Bullet markers: reclassify current chunk as `bullet_narrative`
- Unrecognized bold lines: classify as `knowledge_box` with `confidence < 0.8`; add `"unrecognized_box_header"` to `flags`

### Cross-page continuity

Maintain `last_open_chunk` state across pages:
- First non-noise line on a new page is body/bullet text AND previous page left an open chunk → continuation: inherit `chunk_type`, `heading`, `section_id`; mark previous chunk `is_complete: false`
- First non-noise line is a structural element → not a continuation; start a new chunk

Incomplete chunks (`is_complete: false`) are merged with their continuation before indexing. Only complete chunks are written to pgvector and bm25s.

### Token ceiling

Maximum 512 tokens per chunk. If a merged chunk exceeds 512 tokens, split at the nearest sentence boundary with 50-token overlap. Both values are configurable constants.

### Confidence and indexing threshold

- 0.95: activities and known box headers
- 0.90: table chunks and recognized sub-headings
- 0.85: body narrative paragraphs
- 0.50–0.79: infographic titles, unrecognized box headers

Chunks with `confidence ≥ 0.8` are indexed in pgvector and bm25s. Chunks with `confidence < 0.8` are excluded from both indexes and written to a skipped-chunks report (JSONL) for human review (see issue #38).

### Table rules

- Table titles matching `Table \d+\.\d+` are absorbed into the next `table_segment`; no chunk created from title lines alone
- Cross-page table continuity: if previous page ended a table, reuse stored column headers; treat first row on new page as data, not headers
- If column count differs from stored headers, treat as a new table
- Skip exercise/data tables where more than half the column headers are pure digits

### Skip rules

- Decorative bulletin board pages (page 1 of chapters)
- Header/footer noise: lines matching "Chapter X.indd", "Reprint YYYY", "Chapter X — Title", "Curiosity — Textbook", standalone page numbers
- Figure/image references

### bm25s index contract

The serialized bm25s index is written to a path configurable via CLI argument (default: `./data/bm25s_index/`). RAGService loads from this path at FastAPI startup. The index is rebuilt from scratch on every ingestion run.

## Acceptance criteria

- [ ] CLI accepts `--pdf-dir` (directory of NCERT PDFs) and `--manifest` (JSON file mapping each PDF to `class_level`, `subject`, `chapter`)
- [ ] Structure-aware chunking extracts all 6 chunk types using font-signature classification rules
- [ ] Cross-page continuity is maintained; `is_complete: false` chunks are merged with their continuation before indexing
- [ ] Chunks with `confidence ≥ 0.8` are embedded with `bge-large-en-v1.5` and upserted into pgvector
- [ ] Each vector is stored with metadata: `chunk_id`, `chunk_type`, `class_level`, `subject`, `chapter`, `section_id`, `heading`, `page_number`
- [ ] HNSW index is created on the vector column
- [ ] All indexed chunks are added to a bm25s index serialized to the configured path
- [ ] Chunks with `confidence < 0.8` are excluded from both indexes and written to a skipped-chunks report (JSONL) at `--report-path`
- [ ] Any chunk with ambiguous classification has its `flags` array populated and is included in the skipped-chunks report
- [ ] Running the CLI twice is idempotent: vectors are upserted by `chunk_id`; bm25s index is rebuilt from scratch on each run
- [ ] Integration test: ingest a fixture PDF with manifest; assert vector count, metadata correctness, and bm25s index is non-empty

## Blocked by

- #1 Local dev environment
