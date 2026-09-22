# Decision Log

## Format enforcement: `pre-commit`, `black` and `flake8`

Decision: use `pre-commit` to ensure code formatting with `black` and run `flake8` linting before commits.

Rationale: Running `black` automatically via a git hook guarantees a consistent code style across the team and avoids style-related churn in reviews. Running `flake8` via the same hooks enforces rules and common error checks before code is committed. The `.pre-commit-config.yaml` includes both the `black` and `flake8` hooks so formatting and lint checks happen locally before commit.

## Run & deployment: Docker with small Python base image

Decision: run the application inside Docker for development and deployment, building images from a small official Python base image (Python slim).

Rationale: Containerizing the app ensures consistent runtime environments across machines and CI. Using a slim Python base keeps images small and startup time reasonable while still supporting required OS-level packages.

## Source handling in containers: mount source as a volume (no COPY)

Decision: mount the project source into the container at runtime using a Docker volume (or a bind mount) rather than copying the code into the image at build time.

Rationale: Mounting the source avoids rebuilding the image for code changes during development, enables host-side editing and persistence of the SQLite database file, and keeps the image generic; the container provides the runtime environment while the host supplies editable source code.

## Database choice: SQLite and SQLAlchemy

Decision: use SQLite for persistence and `SQLAlchemy` as the ORM for this project.

Rationale: For the time-constrained technical assignment, SQLite is a practical choice — it's lightweight, requires no separate database server, and is sufficient for the small dataset and development workflow. I chose `SQLAlchemy` as the ORM because of prior experience with it.

