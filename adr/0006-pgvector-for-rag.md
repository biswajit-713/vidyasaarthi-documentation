# pgvector inside Postgres is used for the NCERTCorpus vector store

The NCERTCorpus (Classes 8–10, all CBSE subjects) is vectorised and stored using the pgvector extension inside the same Postgres instance as the application database.

The corpus is small and bounded — NCERT textbooks for 3 classes across all subjects chunk into roughly 10,000–30,000 vectors. This corpus does not grow with user activity; it only changes when NCERT revises textbooks. pgvector with an HNSW index handles tens of millions of vectors with sub-10ms query latency, making this use case trivially within range. At the expected concurrent load (hundreds of simultaneous ExplanationSessions), standard connection pooling via PgBouncer is sufficient. A read replica can be added if vector query load becomes a bottleneck at scale.

We chose pgvector over dedicated vector stores because: (1) one fewer infrastructure component to operate and monitor; (2) student data never leaves our own database — no vector SaaS vendor in the data path; (3) the corpus size does not justify the per-vector cost or operational overhead of a managed service.

## Considered Options

- **Pinecone**: Fully managed, excellent at massive scale, but per-vector pricing and a third-party SaaS in the student data path. Unjustified for a 10,000–30,000 vector corpus.
- **Weaviate**: Self-hosted or managed, good at scale, but a separate service to operate with no advantage over pgvector at this corpus size.
- **pgvector (Postgres extension)** ✅: Handles the corpus size and concurrent load comfortably, eliminates a separate service, keeps data in-house.
