# Task Manager (Layered Architecture)

This sample FastAPI project demonstrates a simple layered architecture with:

- Domain: entities and repository interfaces
- Application: use-cases and DTOs (Pydantic schemas)
- Infrastructure: concrete repository implementation and HTTP adapters

Quickstart (Docker Compose)

1. Build and start the service using Docker Compose (recommended):

```bash
docker compose up --build --detach
```

2. View logs or follow them:

```bash
docker compose logs -f
```

3. Stop and remove containers:

```bash
docker compose down
```

4. Open the docs at: http://127.0.0.1:8000/

Pre-commit installation

This project uses `pre-commit` to run `black` on files before committing. To install and enable the git hook locally:

1. Install dev dependencies (includes `pre-commit`):

```bash
pip install -r requirements/dev.txt
```

2. Install the pre-commit hook into your git repo (run once):

```bash
pre-commit install
```

3. (Optional) Run all hooks against all files now:

```bash
pre-commit run --all-files
```

After installation, `pre-commit` will automatically format staged files with `black` when you commit.

Note: the pre-commit hooks include both `black` (formatting) and `flake8` (linting). To run the `flake8` or `black` hook across all files manually:

```bash
pre-commit run black --all-files
pre-commit run flake8 --all-files
```
