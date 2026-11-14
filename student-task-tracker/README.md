# Student Task Tracker

A small, working Flask web application for teaching Python web apps, Docker, and GitHub Actions.

## Features
- Add, complete/undo, and delete tasks
- SQLite storage
- JSON endpoint: `/api/tasks`
- Container health endpoints: `/health`, `/live`, `/ready`
- Pytest tests
- Non-root Docker container
- GitHub Actions tests, builds, and publishes to GitHub Container Registry (GHCR)

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Run with Docker

```bash
docker build -t student-task-tracker:local .
docker run --rm -p 5000:5000 -v task-data:/data --name student-task-tracker student-task-tracker:local
```

Open http://localhost:5000. The named volume keeps SQLite data when the container is replaced.

Check health:

```bash
docker inspect --format='{{.State.Health.Status}}' student-task-tracker
```

Stop it with `docker stop student-task-tracker`.

## GitHub Actions demo

1. Create a GitHub repository and push these files to its `main` branch.
2. The workflow runs pytest for pushes and pull requests.
3. After tests pass on a push to `main` (or manual dispatch), it builds and pushes:
   - `ghcr.io/OWNER/REPOSITORY:latest`
   - `ghcr.io/OWNER/REPOSITORY:COMMIT_SHA`
4. In the repository, open **Actions** to watch the jobs.

The workflow uses the built-in `GITHUB_TOKEN` and `packages: write`; no personal access token is required. If publishing fails due to package/repository visibility or permissions, check the repository's Actions settings and the package access settings in GitHub.

To pull and run the published image:

```bash
docker pull ghcr.io/OWNER/REPOSITORY:latest
docker run --rm -p 5000:5000 -v task-data:/data ghcr.io/OWNER/REPOSITORY:latest
```

Replace `OWNER/REPOSITORY` with your lowercase GitHub owner and repository name.

## Teaching flow
1. Explain Flask routes and HTML form submissions in `app.py`.
2. Explain `requirements.txt` and reproducible dependency installation.
3. Build and run the image locally with Docker.
4. Explain Dockerfile layers, port exposure, non-root user, health check, and volume.
5. Open `.github/workflows/ci-cd.yml`: checkout → Python setup → dependency install → tests → Docker build/push.
6. Break a test intentionally and show that `needs: test` prevents publishing.
