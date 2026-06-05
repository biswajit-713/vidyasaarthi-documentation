## RAGAS evaluation — Answer Relevancy and Faithfulness

## What to build

Extend the RAGAS evaluation harness to measure Answer Relevancy and Faithfulness. These metrics require generating answers via the LLM and evaluating whether the answer addresses the question (relevancy) and whether it stays within the retrieved context (faithfulness).

This is a future extension of issue #33. The frozen evaluation dataset from #33 is reused.

## Acceptance criteria

- [ ] Evaluation harness generates answers for each eval question by calling the LLM with retrieved passages as context
- [ ] RAGAS measures Answer Relevancy and Faithfulness for each generated answer
- [ ] Metrics report extended to include all 4 RAGAS metrics: Context Precision, Context Recall, Answer Relevancy, Faithfulness

## Blocked by

- #33 RAGAS evaluation — Context Precision and Context Recall
- #8 ExplanationSession backend
