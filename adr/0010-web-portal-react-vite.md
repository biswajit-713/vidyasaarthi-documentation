# Teacher/Admin web portal is built with React + Vite, served via Nginx

The Teacher/Admin portal is a React SPA built with Vite, served as static files via Nginx on the same VM as the FastAPI backend. The portal is an internal tool — only Teachers and CenterAdmins access it. It has no public-facing pages and no SEO requirements, so Next.js SSR adds complexity with no benefit. Static files served by Nginx require no separate hosting and add negligible resource usage on the VM.
