# Ecoplay Backend

This repository contains the FastAPI backend that powers the Ecoplay platform. The code lives inside the `api/` package and exposes authentication, catalog, equipes, and tarefas routes while loading all secrets from `api/.env`.

## Local development checklist
1. Always activate the project-level virtual environment before running anything:
   ```powershell
   C:/Users/joao/Desktop/backend/.venv/Scripts/activate
   ```
2. Install the pinned dependencies:
   ```powershell
   pip install -r api/requirements.txt
   ```
3. Copy the sample environment file and fill in real credentials (do not commit the populated `.env`):
   ```powershell
   copy api\.env.example api\.env
   ```
4. Start the API server locally from the repo root so the `frontend/` discovery works correctly:
   ```powershell
   uvicorn api.main:app --reload
   ```

## Preparing for Render deployment
1. **Main branch:** Render looks for `main` by default. If your primary branch has another name, rename it before connecting the repository:
   ```powershell
   git branch -M main
   git push -u origin main
   ```
2. **Connect the repo:** On Render, create a new **Web Service** using this repository and let it read the `render.yaml` at the root. The service already runs `pip install -r api/requirements.txt` and starts `uvicorn api.main:app --host 0.0.0.0 --port $PORT` for you.
3. **Environment variables:** Populate the following secrets through the Render dashboard (they are marked `sync: false` in `render.yaml`, meaning Render does not store them in the repo):
   - `DATABASE_URL`: MySQL connection string for production.
   - `SECRET_KEY`: Random string used for JWT/session signing.
   - `ALGORITHM`: Usually `HS256`.
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token lifetime in minutes (e.g. `30`).

## Repository hygiene
- `.gitignore` already ignores `.env`, virtual environments, compiled files, and log/database artifacts so secrets stay local.
- Use `api/.env.example` as the template when onboarding other developers or machines.
- `render.yaml` pins the Render configuration so redeploying from the same branch reproduces the service.

## Tips
- Keep migrations in sync with `alembic/` when you change models.
- If you ever delete or recreate the local `.env`, run step 3 again before starting the server.
