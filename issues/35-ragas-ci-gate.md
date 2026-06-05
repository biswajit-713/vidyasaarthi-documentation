## RAGAS CI gate

## What to build

Integrate the RAGAS evaluation harness into the CI pipeline as a quality gate. The gate runs on pull requests that touch RAGService or the ingestion CLI and fails the build if Context Precision or Context Recall drops below configured thresholds.

This protects against regressions when the retrieval pipeline, chunking logic, or model configuration changes.

## Acceptance criteria

- [ ] CI pipeline runs the RAGAS evaluation script on pull requests touching RAGService or ingestion code
- [ ] Build fails if Context Precision or Context Recall drops below thresholds defined in `eval/ragas_thresholds.json`
- [ ] Thresholds file is updated by the engineering team after intentional pipeline changes that shift baseline metrics

## Blocked by

- #33 RAGAS evaluation — Context Precision and Context Recall
