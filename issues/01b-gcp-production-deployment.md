## GCP production deployment

## What to build

Deploy the application to a GCP e2-small VM in the Mumbai region (asia-south1) to satisfy DPDP data residency requirements. This is deferred until there is reasonable progress on core features and the platform is ready for real users.

The deployment must include:
- GCP e2-small VM (asia-south1), FastAPI running as a Docker container managed by a systemd restart policy
- Postgres running natively on the VM (not in Docker) to avoid accidental data loss from volume mismanagement
- Nginx serving the React+Vite TeacherPortal as static files and reverse-proxying API requests to FastAPI
- GCS bucket for StudyNote file storage
- Daily `pg_dump` uploaded to a separate GCS bucket
- Deployment workflow: local build → push image to GCR → pull on VM → restart container

## Acceptance criteria

- [ ] FastAPI container starts on VM boot via systemd and restarts on failure
- [ ] Postgres is running natively, not in Docker
- [ ] Nginx reverse-proxies `/api` to FastAPI and serves TeacherPortal static files
- [ ] GCS bucket created; MinIO connection string replaced with GCS credentials in production env
- [ ] Daily pg_dump cron job runs and uploads to GCS backup bucket
- [ ] Deployment workflow documented and verified end-to-end
- [ ] VM is in asia-south1 region

## Blocked by

Reasonable progress on core features (not a hard blocker on a specific issue number)
