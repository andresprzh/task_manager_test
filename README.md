# Task Manager 

Simple Task Management API with JWT authentication, built with FastAPI and SQLAlchemy.

### Folder Organization

```
task_manager/
├── app/
│   ├── __init__.py
│   └── main.py                 # FastAPI app initialization and router setup
├── application/
│   ├── __init__.py
│   ├── schemas/                # Pydantic models for request/response
│   └── use_cases/              # Business logic orchestrators
│       ├── __init__.py
│       └── task.py             # TaskUseCase, ListTaskUseCase
├── domain/
│   ├── __init__.py
│   ├── models/                 # Domain entities (Task, ListTask)
│   │   ├── __init__.py
│   │   └── task.py
│   └── repositories/           # Repository interfaces
│       ├── __init__.py
│       └── base.py
└── infrastructure/
    ├── __init__.py
    ├── api/                    # FastAPI router functions
    │   ├── __init__.py
    │   └── task.py             # API endpoints for tasks/lists
    └── repositories/           # Repository implementations (SQLAlchemy)
        ├── __init__.py
        └── task.py             # SQLAlchemyTaskRepository, SQLAlchemyListTaskRepository

tests/                          # Mirror of source structure with corresponding tests
├── application/
├── domain/
├── infrastructure/
└── conftest.py                 # Pytest fixtures
```


## Quickstart (Docker Compose)

1. Build and start the service using Docker Compose (recommended):

```bash
docker compose build
```

```bash
docker compose up -d
```

2. View logs or follow them:

```bash
docker compose logs -f
```

3. Stop and remove containers:

```bash
docker compose down
```

4. Open the app at: http://127.0.0.1:8000/

## Pre-commit installation

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

## Testing

This project uses `pytest` for testing. To run the tests:

```bash
docker compose run --rm web pytest
```

The test result are saved in the `test-results` folder, including coverage reports in HTML or XML formats.