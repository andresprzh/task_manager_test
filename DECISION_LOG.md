# Decision Log

## Format enforcement: `pre-commit`, `black` and `flake8`

To ensure consistent code formatting and linting, the project uses `pre-commit` hooks to run `black` and `flake8` before commits. This allow that this is enforced locally before code is pushed to the repository, avoiding style-related churn in reviews.

## Run & deployment: Docker with small Python base image

To run the aplication in development and deployment, the project uses Docker with a small official Python base image (Python slim). This ensures consistent runtime environments across machines and CI, while keeping images small and startup time reasonable.

## Source handling in containers: mount source as a volume (no COPY)

To handle the source code in the container, the project mounts the source code as a volume at runtime, however the `Dockerfile` still uses `COPY` to gurantee that the image is self-contained and can run without the source code mounted. This allows for a flexible development workflow where code changes on the host are reflected in the container without rebuilding the image, while still allowing for a standalone image for deployment.

## Database choice: SQLite and SQLAlchemy

For the database, the project uses SQLite for persistence and `SQLAlchemy` as the ORM. SQLite is a practical choice for the time-constrained technical assignment, as it is lightweight, requires no separate database server, and is sufficient for the small dataset and development workflow. `SQLAlchemy` was chosen as the ORM due to prior experience with it.

## Testing framework: `pytest` with coverage reports

The project uses `pytest` as the testing framework, with coverage reports generated in HTML and XML formats. The test are located outside the main source code directory, in a `tests` folder, to avoid accidental imports and to ensure that the tests are run in an environment similar to production. The test results are saved in a `test-results` folder, which can be used for further analysis or integration with CI/CD pipelines. The structure of `tests` folder is organized to mirror the main source code structure, making it easy to locate and maintain tests corresponding to specific modules or features.