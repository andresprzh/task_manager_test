"""SQLAlchemy repositories, one module per feature.

Import every feature module here. ``init_async_db`` calls ``create_all`` on the
shared metadata, and a table only exists in that metadata once the module
defining it has been imported — so a new feature module that is never imported
here would silently never get its table created.

Import from this package rather than from the modules directly, so that
guarantee holds for callers too.
"""

from task_manager.infrastructure.repositories.base import (
    Base,
    DEFAULT_DB_URL,
    enum_column,
    init_async_db,
    init_db_sync,
)
from task_manager.infrastructure.repositories.task import (
    ListTaskORM,
    SQLAlchemyListTaskRepository,
    SQLAlchemyTaskRepository,
    TaskORM,
)

__all__ = [
    "Base",
    "DEFAULT_DB_URL",
    "enum_column",
    "init_async_db",
    "init_db_sync",
    "ListTaskORM",
    "SQLAlchemyListTaskRepository",
    "SQLAlchemyTaskRepository",
    "TaskORM",
]
