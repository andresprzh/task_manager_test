"""Repository interfaces the domain requires, one module per feature.

These are abstract on purpose: the domain declares what it needs, and
``task_manager.infrastructure.repositories`` supplies the implementations.
"""

from task_manager.domain.repositories.task import ListTaskRepository, TaskRepository

__all__ = ["ListTaskRepository", "TaskRepository"]
