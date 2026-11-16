# 3-Tier Todo App (Dockerfiles only)

| Tier     | Tech              | Folder      | Image name suffix |
|----------|-------------------|-------------|-------------------|
| Frontend | HTML/JS + Nginx   | `frontend/` | `-frontend`       |
| Backend  | Node.js + Express | `backend/`  | `-backend`        |
| Database | PostgreSQL 16     | `db/`       | `-db`             |

Nginx serves the UI and proxies `/api/*` to the backend (`BACKEND_URL`), which connects to PostgreSQL.

## Build images locally
    docker build -t todo-db       ./db
    docker build -t todo-backend  ./backend
    docker build -t todo-frontend ./frontend

## Run locally (plain docker commands)
    docker network create todo-net

    docker run -d --name db --network todo-net \
      -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=todos \
      -v todo-pgdata:/var/lib/postgresql/data \
      todo-db

    docker run -d --name backend --network todo-net \
      -e DB_HOST=db -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=todos \
      todo-backend

    docker run -d --name frontend --network todo-net -p 8080:80 \
      -e BACKEND_URL=http://backend:3000 \
      todo-frontend

Open http://localhost:8080

## Environment variables
- **db**: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- **backend**: `DB_HOST`, `DB_PORT` (5432), `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `PORT` (3000)
- **frontend**: `BACKEND_URL` (default `http://backend:3000`)

## GitHub Actions
`.github/workflows/ci-cd.yml`:
- **test**: runs backend unit tests
- **build-and-push**: builds all three Dockerfiles in parallel. On pull requests it only builds; on pushes to `main` it also pushes to GitHub Container Registry:
  - `ghcr.io/<owner>/<repo>-frontend:latest` and `:<commit-sha>`
  - `ghcr.io/<owner>/<repo>-backend:latest` and `:<commit-sha>`
  - `ghcr.io/<owner>/<repo>-db:latest` and `:<commit-sha>`

No secrets needed; the built-in `GITHUB_TOKEN` is used. To push to Docker Hub or AWS ECR instead, change the login step and the `IMAGE_PREFIX`.
