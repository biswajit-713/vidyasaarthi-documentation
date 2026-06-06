# Architecture

```mermaid
flowchart TB
    subgraph Clients["Client Layer"]
        SA["📱 Student App\nReact Native / Expo"]
        TP["🖥️ Teacher Portal\nReact + Vite"]
    end

    subgraph GCP["GCP Mumbai · asia-south1 · e2-small VM (~₹1,000/month)"]
        subgraph DockerContainer["Docker Container"]
            FA["FastAPI\nfastapi-users · SQLAlchemy\nLiteLLM · streaming SSE"]
        end
        subgraph NativePostgres["Native (no Docker)"]
            PG["Postgres 16\n+ pgvector\nHNSW index · 10k–30k vectors"]
        end
    end

    subgraph AILayer["AI Layer"]
        LLM["LiteLLM library\n(direct provider calls)"]
        CL["Claude\nExplanationSession\nPerformanceReport narrative"]
        GPT["GPT-4\nfallback / lightweight tasks"]
        LLM --> CL
        LLM --> GPT
    end

    subgraph ExternalServices["External Services"]
        FCM["Firebase FCM\n4 notification types"]
        WA["WhatsApp Business API\nTeacherFlag nudge"]
        GCS["GCS Bucket\nStudyNote PDFs\nDaily pg_dump backups"]
        GCR["Google Container Registry\ndocker pull on deploy"]
    end

    subgraph OfflineJobs["Offline Pre-launch Jobs (run once, not on VM)"]
        IC["NCERTCorpus Ingestion CLI\nPDF → chunks → embeddings → pgvector + bm25s index"]
        QB["QuestionBank Generation CLI\nNCERT chunks → MCQs → Postgres"]
    end

    SA -- "HTTPS · REST + streaming SSE" --> FA
    TP -- "HTTPS · REST" --> FA
    FA <-- "SQLAlchemy ORM" --> PG
    FA -- "LiteLLM library\n(no 3rd-party proxy)" --> LLM
    FA -- "StudyNote upload/download" --> GCS
    FA -- "inactivity / DailyConcept /\nStudyNote / Flag resolved" --> FCM
    FA -- "TeacherFlag raised" --> WA
    FCM -- "push" --> SA
    IC -- "vectors + metadata" --> PG
    QB -- "MCQ questions" --> PG
    PG -- "daily pg_dump" --> GCS
    GCR -- "docker pull on deploy" --> DockerContainer

    classDef client fill:#dbeafe,stroke:#3b82f6,color:#1e3a5f
    classDef service fill:#dcfce7,stroke:#22c55e,color:#14532d
    classDef ai fill:#fef9c3,stroke:#eab308,color:#713f12
    classDef external fill:#f3e8ff,stroke:#a855f7,color:#3b0764
    classDef offline fill:#ffedd5,stroke:#f97316,color:#7c2d12
    classDef db fill:#fee2e2,stroke:#ef4444,color:#7f1d1d

    class SA,TP client
    class FA service
    class PG db
    class LLM,CL,GPT ai
    class FCM,WA,GCS,GCR external
    class IC,QB offline
```

## Key decisions

| Decision | Choice | Reason |
|---|---|---|
| Backend | FastAPI | Async-native; first-class LLM streaming support |
| ORM | SQLAlchemy | Standard Python ORM; works with FastAPI |
| Auth | fastapi-users | Mobile number + password / OTP |
| LLM abstraction | LiteLLM (library) | Direct provider calls; no 3rd-party in student data path |
| Vector store | pgvector in Postgres | Corpus is small (10k–30k vectors); no extra service to operate |
| Student frontend | React Native / Expo | Mobile-first; interactive AI sessions |
| Teacher frontend | React + Vite | Desktop-optimized teacher/admin workflows |
| Infrastructure | GCP e2-small VM | ~₹1,000/month; DPDP data residency (Mumbai); migrates to Cloud Run via same Docker image |
| Teacher notifications | WhatsApp Business API | Higher open rate than SMS in India; disableable per-center |
| Push notifications | Firebase FCM | 4 types: DailyConcept, TeacherFlag resolved, StudyNote shared, inactivity reminder |
| Object storage | GCS | StudyNote PDFs (≤20MB) + daily DB backups |
| BM25 keyword index | bm25s (Python library) | True BM25 scoring; Postgres FTS rejected (non-standard scoring); Tantivy rejected (Rust build dependency, stale Python bindings) |
| Reranker | bge-reranker-base, plain PyTorch on CPU | ~400–800ms for top-20 on e2-small; ONNX INT8 and T4 GPU are documented upgrade paths |
```
