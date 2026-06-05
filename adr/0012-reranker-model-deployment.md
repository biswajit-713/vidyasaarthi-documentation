# Reranker runs as plain PyTorch on CPU; GPU and ONNX are staged upgrade paths

The hybrid retrieval pipeline reranks top-N candidates using `BAAI/bge-reranker-base` (cross-encoder, ~278M parameters). For v1 we load the model via `sentence-transformers` in plain PyTorch on the same e2-small VM as the application.

Estimated latency for top-15 candidates on 2-vCPU CPU: ~400–800ms. This is acceptable because retrieval always precedes an LLM streaming call (2–10s); the reranker does not add a perceptible wait for the student.

## Considered Options

- **Plain PyTorch on CPU (e2-small)** ✅: No extra dependencies, acceptable latency for v1 load, ~1.1GB RAM for model weights.
- **ONNX INT8 on CPU**: 2–4x faster (~120–250ms for top-15), model weights shrink to ~280MB (meaningful on e2-small). Overhead: `optimum[onnxruntime]` dependency, one-time export step at ingestion time. Defer until CPU latency or RAM pressure is measured as a real constraint in production.
- **T4 GPU VM**: Sub-5ms per pair, any model size. Cost jumps from ~₹1,000/month to ~₹7,000–8,000/month. Appropriate when concurrent session volume justifies it.

## Upgrade path

1. If profiling shows reranker latency is a bottleneck: export `bge-reranker-base` to ONNX INT8 via `optimum`. No architecture change required — swap the model loader in the retrieval service.
2. If concurrent load grows beyond what a single CPU VM handles: migrate VM to include a T4 GPU. The same PyTorch model loads on GPU without code changes.
