# NCERT content is ingested into a vector store for RAG-grounded explanations

All AI explanations and tests are grounded by retrieving relevant passages from ingested NCERT textbooks (Classes 8–10, all CBSE subjects) stored in a vector database. The AI is not free to explain beyond what NCERT covers at the student's class level — retrieved passages constrain the response. We chose this over a prompt-only constraint ("stay within NCERT scope") because the boundary enforcement needed to be precise and auditable: a Class 9 student asking about motion must not receive a calculus-based explanation, and a parent or teacher must be able to verify the explanation is syllabus-aligned. NCERT content is government-published and freely available, which removes the copyright barrier.

## Considered Options

- **Prompt constraint only**: Instruct the LLM to stay within NCERT scope without storing any content. Cheaper to build, but scope enforcement is fuzzy and unauditable.
- **RAG with ingested NCERT text** ✅: Ingest NCERT PDFs into a vector store. Retrieve relevant passages per query. Harder to build, but enforces precise syllabus boundaries and is auditable.
