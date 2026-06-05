## RAGAS evaluation — Context Precision and Context Recall

## What to build

An on-demand CLI evaluation harness that measures RAGService retrieval quality using RAGAS Context Precision and Context Recall metrics. These metrics evaluate the retrieval pipeline directly — no LLM answer generation required.

### Evaluation dataset

The engineering team builds and owns a fixed evaluation dataset of ~100 (question, ground-truth passages) pairs:

1. Use Claude to generate ~200 candidate questions from the ingested NCERTCorpus chunks
2. Engineering team reviews, removes low-quality questions, and freezes ~100
3. Dataset stored in the repo as JSONL: `eval/ragas_retrieval_dataset.jsonl`

### Metrics

- **Context Precision**: fraction of retrieved passages that are relevant to the question
- **Context Recall**: fraction of ground-truth passages covered by the retrieved set

## Acceptance criteria

- [ ] A CLI script generates ~200 evaluation questions from NCERTCorpus chunks using Claude; output is JSONL at `eval/ragas_candidates.jsonl`
- [ ] Frozen evaluation dataset of ~100 reviewed questions stored at `eval/ragas_retrieval_dataset.jsonl`
- [ ] CLI evaluation script runs `RAGService.retrieve()` against every question in the frozen dataset and computes Context Precision and Context Recall via RAGAS
- [ ] Script prints a metrics report to stdout: overall scores and per-chunk-type breakdown
- [ ] Evaluation dataset path and metrics thresholds are configurable via CLI arguments

## Blocked by

- #6 NCERTCorpus ingestion CLI
- #32 RAGService hybrid retrieval pipeline
