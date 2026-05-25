# Infrastructure: single e2-small VM on GCP Mumbai, Docker for FastAPI, native Postgres

The application runs on a single e2-small VM (0.5 vCPU shared, 2 GB RAM, ~₹1,000/month) on GCP Mumbai (asia-south1) to satisfy DPDP data residency requirements. FastAPI runs as a Docker container (managed via systemd restart policy), enabling reproducible builds and a direct migration path to Cloud Run later. Postgres runs natively on the VM — not in Docker — to avoid accidental data loss from volume mismanagement.

Embedding generation (NCERTCorpus → pgvector) and QuestionBank generation are offline pre-launch jobs run separately, not on the application VM. This keeps the runtime memory footprint low (~1–1.4 GB), making e2-small viable at 100 users.

Daily pg_dump backups are uploaded to GCS from day one. When operational convenience warrants it, Postgres migrates to Cloud SQL (a half-day task: dump, restore, update connection string). When traffic demands auto-scaling, FastAPI migrates to Cloud Run using the same Docker image.

## Deployment workflow
`local build → push image to GCR → pull on VM → restart container`

## Considered Options

- **Cloud Run (serverless)**: Cold start latency of 2–5s is unacceptable for a student-facing app. min-instances=1 removes the cost benefit.
- **e2-medium (~₹2,000/month)**: Right choice once memory pressure is observed. Resize requires only a 2-minute VM restart.
- **e2-small (~₹1,000/month)** ✅: Sufficient for 100 users given offline-only embedding and question generation.
